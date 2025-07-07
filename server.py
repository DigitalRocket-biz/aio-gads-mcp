#!/usr/bin/env python3
# (Same content as generic-mcp-tool/server.py)

from __future__ import annotations

import asyncio
import html
import json
import pathlib
import sys
from typing import Any, Dict, List

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from tenacity import retry, stop_after_attempt, wait_random_exponential

DOC_CACHE = pathlib.Path(__file__).parent / "docs_cache"
DOC_CACHE.mkdir(parents=True, exist_ok=True)
DOC_BASE_URL = "https://developers.google.com/google-ads/api/reference/rpc/v20"


def _send(msg: Dict[str, Any]):
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _client() -> GoogleAdsClient:
    return GoogleAdsClient.load_from_storage()


async def _fetch(url: str) -> str:
    async with aiohttp.ClientSession(raise_for_status=True) as sess:
        async with sess.get(url, timeout=60) as r:
            return await r.text()


def _doc_html(service: str) -> str:
    cached = DOC_CACHE / f"{service}.html"
    if cached.exists():
        return cached.read_text("utf-8")
    html_txt = asyncio.run(_fetch(f"{DOC_BASE_URL}/{service}"))
    cached.write_text(html_txt, "utf-8")
    return html_txt


def _doc_snippet(service: str) -> str:
    soup = BeautifulSoup(_doc_html(service), "html.parser")
    body = soup.find("main") or soup
    return str(body)[:16000]


@retry(wait=wait_random_exponential(min=1, max=30), stop=stop_after_attempt(4))
def _gaql_stream(client: GoogleAdsClient, cid: str, q: str):
    svc = client.get_service("GoogleAdsService")
    return svc.search_stream(customer_id=cid, query=q)


async def _run_gaql(customer_id: str, gaql: str, parallel: bool = False):
    client = _client()

    async def _run(cid: str):
        rows = [row for resp in _gaql_stream(client, cid, gaql) for row in resp.results]
        return [json.loads(row.to_json()) for row in rows]

    if parallel:
        cust_svc = client.get_service("CustomerService")
        subs = [n.split("/")[-1] for n in cust_svc.list_accessible_customers().resource_names]
        tasks = [asyncio.to_thread(_run, cid) for cid in subs]
        res = await asyncio.gather(*tasks)
        flat: List[Dict[str, Any]] = [item for sub in res for item in sub]
        return flat

    return await asyncio.to_thread(_run, customer_id)


async def _dispatch(req):
    rid = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    try:
        if method == "lookup_docs":
            _send({"id": rid, "result": html.escape(_doc_snippet(params["service"]))})
        elif method == "run_gaql":
            res = await _run_gaql(params["customer_id"], params["gaql"], params.get("parallel", False))
            _send({"id": rid, "result": res})
        else:
            raise ValueError("unknown method")
    except GoogleAdsException as e:
        _send({"id": rid, "error": {"message": str(e), "details": e.failure.error_code}})
    except Exception as e:
        _send({"id": rid, "error": {"message": str(e)}})


async def main():
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    loop = asyncio.get_event_loop()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)

    while True:
        line = await reader.readline()
        if not line:
            break
        try:
            j = json.loads(line.decode())
        except json.JSONDecodeError:
            continue
        await _dispatch(j)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
