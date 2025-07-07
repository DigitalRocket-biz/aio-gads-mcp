#!/usr/bin/env python3
"""
Google Ads MCP Server
A Model Context Protocol server for Google Ads API operations
"""

from __future__ import annotations

import asyncio
import json
import sys
import os
from typing import Any, Dict, List, Optional
import requests
from pathlib import Path
from datetime import datetime, timedelta
import hashlib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Initialize the MCP server
server = Server("google-ads-mcp")

# Google Ads API configuration from environment variables
GOOGLE_ADS_PROXY_URL = os.getenv("GOOGLE_ADS_PROXY_URL", "https://google-ads.theaio.co/api/google-ads")
GOOGLE_ADS_API_VERSION = os.getenv("GOOGLE_ADS_API_VERSION", "v20")
GOOGLE_ADS_ORG_ID = os.getenv("GOOGLE_ADS_ORG_ID", "f76a9096-db82-4506-b451-61474ea4b5e7")
GOOGLE_ADS_LINKED_ACCOUNT_ID = os.getenv("GOOGLE_ADS_LINKED_ACCOUNT_ID", "e9c9e1ea-cf54-4011-9785-fde0cd32d05f")
ROOT_MCC = os.getenv("GOOGLE_ADS_MCC_ID", "1639353427")  # Top-level manager customer ID

# API Success Logging
API_LOG_FILE = Path(__file__).parent / "api_success_log.json"

class APISuccessLogger:
    """Enhanced learning system that captures ALL successful operations and builds smart context"""
    
    def __init__(self):
        self.log_file = API_LOG_FILE
        self.context_file = Path(__file__).parent / "ai_learning_context.json"
        self._ensure_log_file()
        self._ensure_context_file()
    
    def _ensure_log_file(self):
        """Create log file if it doesn't exist"""
        if not self.log_file.exists():
            self._save_log([])
    
    def _ensure_context_file(self):
        """Create AI context file if it doesn't exist"""
        if not self.context_file.exists():
            self._save_context({
                "learned_patterns": {},
                "successful_workflows": {},
                "customer_preferences": {},
                "optimal_configurations": {},
                "error_prevention": {},
                "last_updated": datetime.now().isoformat()
            })
    
    def _load_log(self) -> List[Dict]:
        """Load existing log entries"""
        try:
            with open(self.log_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_log(self, entries: List[Dict]):
        """Save log entries to file"""
        with open(self.log_file, 'w') as f:
            json.dump(entries, f, indent=2, default=str)
    
    def _load_context(self) -> Dict:
        """Load AI learning context"""
        try:
            with open(self.context_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "learned_patterns": {},
                "successful_workflows": {},
                "customer_preferences": {},
                "optimal_configurations": {},
                "error_prevention": {},
                "last_updated": datetime.now().isoformat()
            }
    
    def _save_context(self, context: Dict):
        """Save AI learning context"""
        context["last_updated"] = datetime.now().isoformat()
        with open(self.context_file, 'w') as f:
            json.dump(context, f, indent=2, default=str)
    
    def log_success(self, operation_type: str, customer_id: str, query: str, 
                   result_count: int, context: Dict = None):
        """Log a successful API call and learn from it"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation_type": operation_type,
            "customer_id": customer_id,
            "query": query,
            "query_hash": hashlib.md5(query.encode()).hexdigest()[:8],
            "result_count": result_count,
            "context": context or {},
            "success": True
        }
        
        # Save to log
        entries = self._load_log()
        entries.append(entry)
        
        # Keep only last 1000 entries
        if len(entries) > 1000:
            entries = entries[-1000:]
        
        self._save_log(entries)
        
        # Learn from this success
        self._learn_from_success(entry)
    
    def _learn_from_success(self, entry: Dict):
        """Extract learnings from successful operation"""
        ai_context = self._load_context()
        
        operation_type = entry["operation_type"]
        customer_id = entry["customer_id"]
        context_data = entry.get("context", {})
        
        # Learn patterns for this operation type
        if operation_type not in ai_context["learned_patterns"]:
            ai_context["learned_patterns"][operation_type] = {
                "success_count": 0,
                "common_parameters": {},
                "working_examples": [],
                "best_practices": []
            }
        
        pattern = ai_context["learned_patterns"][operation_type]
        pattern["success_count"] += 1
        
        # Track common parameters
        for key, value in context_data.items():
            if key not in pattern["common_parameters"]:
                pattern["common_parameters"][key] = {}
            
            value_str = str(value)
            if value_str not in pattern["common_parameters"][key]:
                pattern["common_parameters"][key][value_str] = 0
            pattern["common_parameters"][key][value_str] += 1
        
        # Keep best working examples
        pattern["working_examples"].append({
            "query": entry["query"],
            "context": context_data,
            "result_count": entry["result_count"],
            "timestamp": entry["timestamp"]
        })
        
        # Keep only last 10 examples per operation type
        if len(pattern["working_examples"]) > 10:
            pattern["working_examples"] = pattern["working_examples"][-10:]
        
        # Learn customer preferences
        if customer_id not in ai_context["customer_preferences"]:
            ai_context["customer_preferences"][customer_id] = {
                "successful_operations": {},
                "preferred_settings": {},
                "business_context": {}
            }
        
        customer_prefs = ai_context["customer_preferences"][customer_id]
        if operation_type not in customer_prefs["successful_operations"]:
            customer_prefs["successful_operations"][operation_type] = 0
        customer_prefs["successful_operations"][operation_type] += 1
        
        # Learn optimal configurations
        if operation_type == "campaign_creation":
            bidding_strategy = context_data.get("bidding_strategy_type")
            if bidding_strategy:
                if "campaign_bidding" not in ai_context["optimal_configurations"]:
                    ai_context["optimal_configurations"]["campaign_bidding"] = {}
                if bidding_strategy not in ai_context["optimal_configurations"]["campaign_bidding"]:
                    ai_context["optimal_configurations"]["campaign_bidding"][bidding_strategy] = 0
                ai_context["optimal_configurations"]["campaign_bidding"][bidding_strategy] += 1
        
        # Save updated context
        self._save_context(ai_context)
    
    def get_patterns(self, operation_type: str = None) -> Dict:
        """Get successful patterns for AI context"""
        entries = self._load_log()
        
        if operation_type:
            entries = [e for e in entries if e.get("operation_type") == operation_type]
        
        # Group by common patterns
        patterns = {
            "successful_queries": [],
            "common_fields": {},
            "working_customer_ids": set(),
            "query_templates": []
        }
        
        for entry in entries[-50:]:  # Last 50 successful calls
            patterns["successful_queries"].append({
                "query": entry["query"],
                "customer_id": entry["customer_id"],
                "result_count": entry["result_count"],
                "operation": entry["operation_type"]
            })
            patterns["working_customer_ids"].add(entry["customer_id"])
        
        patterns["working_customer_ids"] = list(patterns["working_customer_ids"])
        
        return patterns
    
    def get_ai_context(self, customer_id: str = None, operation_type: str = None) -> Dict:
        """Get comprehensive AI context for smart recommendations"""
        ai_context = self._load_context()
        
        # Filter context if specific customer or operation requested
        if customer_id and customer_id in ai_context["customer_preferences"]:
            customer_context = ai_context["customer_preferences"][customer_id]
        else:
            customer_context = {}
        
        if operation_type and operation_type in ai_context["learned_patterns"]:
            operation_context = ai_context["learned_patterns"][operation_type]
        else:
            operation_context = {}
        
        return {
            "customer_context": customer_context,
            "operation_context": operation_context,
            "optimal_configurations": ai_context["optimal_configurations"],
            "all_patterns": ai_context["learned_patterns"],
            "last_updated": ai_context["last_updated"]
        }
    
    def suggest_optimal_settings(self, operation_type: str, customer_id: str = None) -> Dict:
        """Suggest optimal settings based on learned patterns"""
        ai_context = self._load_context()
        
        suggestions = {
            "recommended_settings": {},
            "reasoning": [],
            "confidence": "medium"
        }
        
        # Get patterns for this operation type
        if operation_type in ai_context["learned_patterns"]:
            pattern = ai_context["learned_patterns"][operation_type]
            
            # Suggest most common successful parameters
            for param, values in pattern["common_parameters"].items():
                if values:
                    # Get most successful value
                    best_value = max(values.items(), key=lambda x: x[1])
                    suggestions["recommended_settings"][param] = best_value[0]
                    suggestions["reasoning"].append(f"{param}: {best_value[0]} (used successfully {best_value[1]} times)")
        
        # Add customer-specific preferences if available
        if customer_id and customer_id in ai_context["customer_preferences"]:
            customer_prefs = ai_context["customer_preferences"][customer_id]
            if operation_type in customer_prefs["successful_operations"]:
                suggestions["confidence"] = "high"
                suggestions["reasoning"].append(f"Customer {customer_id} has {customer_prefs['successful_operations'][operation_type]} successful {operation_type} operations")
        
        return suggestions

# Global logger instance
api_logger = APISuccessLogger()

def get_access_token() -> Optional[str]:
    """Get access token from environment variable (permanent) or CLI session file (fallback)"""
    try:
        # First, try permanent JWT token from environment
        permanent_token = os.getenv('PERMANENT_JWT_TOKEN')
        if permanent_token:
            return permanent_token
            
        # Fallback to CLI session file
        session_path = Path("/mnt/c/Users/willi/OneDrive/Desktop/aio-v2/aio-cli/.aio-cli-session.json")
        if session_path.exists():
            with open(session_path, 'r') as f:
                session_data = json.load(f)
                return session_data.get('access_token')
        return None
    except Exception as e:
        print(f"Error reading authentication: {e}", file=sys.stderr)
        return None

def make_google_ads_request(endpoint: str, data: dict = None, method: str = "POST", login_customer_id: Optional[str] = None, operation_type: str = "custom_api_call") -> dict:
    """Make a request to the Google Ads proxy API with optional login customer ID and automatic learning"""
    access_token = get_access_token()
    if not access_token:
        return {"error": "No access token available. Please run 'aio-cli auth login' first."}
    
    url = f"{GOOGLE_ADS_PROXY_URL}/p/{GOOGLE_ADS_API_VERSION}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "x-org-id": GOOGLE_ADS_ORG_ID,
        "x-linked-account-id": GOOGLE_ADS_LINKED_ACCOUNT_ID,
        "Accept": "*/*"
    }
    
    # Add login customer ID if provided
    if login_customer_id:
        headers["login-customer-id"] = login_customer_id
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return {"error": f"Unsupported HTTP method: {method}"}
            
        response.raise_for_status()
        result = response.json()
        
        # LEARN FROM EVERY SUCCESS - Extract customer ID from endpoint or data
        customer_id = "unknown"
        if "customers/" in endpoint:
            try:
                customer_id = endpoint.split("customers/")[1].split("/")[0]
            except:
                pass
        
        # Log this successful custom API call for learning
        if result and not result.get("error"):
            result_count = 0
            if "results" in result:
                result_count = len(result["results"])
            elif isinstance(result, list):
                result_count = len(result)
            else:
                result_count = 1
            
            # Capture EVERYTHING for learning
            api_logger.log_success(
                operation_type=operation_type,
                customer_id=customer_id,
                query=f"{method} {endpoint}: {data}",
                result_count=result_count,
                context={
                    "endpoint": endpoint,
                    "method": method,
                    "data": data,
                    "login_customer_id": login_customer_id,
                    "response_keys": list(result.keys()) if isinstance(result, dict) else [],
                    "url": url,
                    "headers_used": {k: v for k, v in headers.items() if k != "Authorization"}
                }
            )
        
        return result
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available Google Ads tools"""
    return [
        types.Tool(
            name="search_campaigns",
            description="Search for Google Ads campaigns",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 10
                    }
                },
                "required": ["customer_id"]
            }
        ),
        types.Tool(
            name="run_gaql",
            description="Execute a Google Ads Query Language (GAQL) query",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID"
                    },
                    "query": {
                        "type": "string",
                        "description": "GAQL query to execute"
                    },
                    "parallel": {
                        "type": "boolean",
                        "description": "Whether to run query across all accessible customers",
                        "default": False
                    },
                    "login_customer_id": {
                        "type": "string",
                        "description": "Manager customer ID for authentication (auto-set to ROOT_MCC if omitted)"
                    }
                },
                "required": ["customer_id", "query"]
            }
        ),
        types.Tool(
            name="get_account_info",
            description="Get basic account information",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID"
                    }
                },
                "required": ["customer_id"]
            }
        ),
        types.Tool(
            name="mutate_campaign",
            description="Update campaign settings (e.g., ROAS targets, budgets)",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID"
                    },
                    "campaign_id": {
                        "type": "string",
                        "description": "Campaign ID to update"
                    },
                    "updates": {
                        "type": "object",
                        "description": "Campaign updates (e.g., target_roas, daily_budget_micros)"
                    }
                },
                "required": ["customer_id", "campaign_id", "updates"]
            }
        ),
        types.Tool(
            name="lookup_docs",
            description="Search Google Ads API documentation for field names and query examples",
            inputSchema={
                "type": "object", 
                "properties": {
                    "resource": {
                        "type": "string",
                        "description": "Resource to look up (e.g., 'campaign', 'ad_group', 'GoogleAdsService')"
                    }
                },
                "required": ["resource"]
            }
        ),
        types.Tool(
            name="get_ai_context",
            description="Get successful API patterns and examples for AI prompting context",
            inputSchema={
                "type": "object",
                "properties": {
                    "operation_type": {
                        "type": "string",
                        "description": "Filter by operation type (gaql_query, campaign_mutation, etc.)"
                    }
                }
            }
        ),
        types.Tool(
            name="api_call",
            description="Make any Google Ads API call - campaigns, ad groups, keywords, budgets, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "endpoint": {
                        "type": "string",
                        "description": "API endpoint path (e.g., 'customers/{customer_id}/campaigns:mutate', 'customers/{customer_id}/campaignBudgets:mutate')"
                    },
                    "method": {
                        "type": "string",
                        "description": "HTTP method",
                        "enum": ["GET", "POST", "PUT", "DELETE"],
                        "default": "POST"
                    },
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID"
                    },
                    "data": {
                        "type": "object",
                        "description": "Request payload/body for the API call"
                    },
                    "login_customer_id": {
                        "type": "string",
                        "description": "Manager customer ID for authentication (auto-set to ROOT_MCC if omitted for child accounts)"
                    }
                },
                "required": ["endpoint", "customer_id"]
            }
        ),
        types.Tool(
            name="create_campaign_budget",
            description="Create a new campaign budget",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "Budget name"
                    },
                    "amount_micros": {
                        "type": "integer",
                        "description": "Daily budget amount in micros (e.g., 50000000 = $50)"
                    },
                    "delivery_method": {
                        "type": "string",
                        "description": "Budget delivery method",
                        "enum": ["STANDARD", "ACCELERATED"],
                        "default": "STANDARD"
                    }
                },
                "required": ["customer_id", "name", "amount_micros"]
            }
        ),
        types.Tool(
            name="create_campaign",
            description="Create a new search campaign",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "Campaign name"
                    },
                    "budget_resource_name": {
                        "type": "string",
                        "description": "Budget resource name (from create_campaign_budget)"
                    },
                    "bidding_strategy_type": {
                        "type": "string",
                        "description": "Bidding strategy",
                        "enum": ["MAXIMIZE_CONVERSIONS", "MAXIMIZE_CLICKS", "TARGET_CPA", "TARGET_ROAS", "MANUAL_CPC"],
                        "default": "MAXIMIZE_CONVERSIONS"
                    },
                    "target_cpa_micros": {
                        "type": "integer",
                        "description": "Target CPA in micros (for TARGET_CPA strategy)"
                    },
                    "target_roas": {
                        "type": "number",
                        "description": "Target ROAS (for TARGET_ROAS strategy)"
                    },
                    "geo_target_constants": {
                        "type": "array",
                        "description": "Array of geo target constants (e.g., ['2840'] for United States)",
                        "items": {"type": "string"}
                    },
                    "status": {
                        "type": "string",
                        "description": "Campaign status",
                        "enum": ["ENABLED", "PAUSED"],
                        "default": "PAUSED"
                    }
                },
                "required": ["customer_id", "name", "budget_resource_name"]
            }
        ),
        types.Tool(
            name="create_ad_group",
            description="Create a new ad group within a campaign",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID"
                    },
                    "campaign_resource_name": {
                        "type": "string",
                        "description": "Campaign resource name"
                    },
                    "name": {
                        "type": "string",
                        "description": "Ad group name"
                    },
                    "cpc_bid_micros": {
                        "type": "integer",
                        "description": "Default CPC bid in micros (e.g., 3500000 = $3.50)"
                    },
                    "status": {
                        "type": "string",
                        "description": "Ad group status",
                        "enum": ["ENABLED", "PAUSED"],
                        "default": "ENABLED"
                    }
                },
                "required": ["customer_id", "campaign_resource_name", "name", "cpc_bid_micros"]
            }
        ),
        types.Tool(
            name="create_keywords",
            description="Create keywords in an ad group",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID"
                    },
                    "ad_group_resource_name": {
                        "type": "string",
                        "description": "Ad group resource name"
                    },
                    "keywords": {
                        "type": "array",
                        "description": "Array of keyword objects",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {
                                    "type": "string",
                                    "description": "Keyword text"
                                },
                                "match_type": {
                                    "type": "string",
                                    "description": "Keyword match type",
                                    "enum": ["EXACT", "PHRASE", "BROAD"]
                                }
                            },
                            "required": ["text", "match_type"]
                        }
                    }
                },
                "required": ["customer_id", "ad_group_resource_name", "keywords"]
            }
        ),
        types.Tool(
            name="create_responsive_search_ad",
            description="Create a responsive search ad",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID"
                    },
                    "ad_group_resource_name": {
                        "type": "string",
                        "description": "Ad group resource name"
                    },
                    "headlines": {
                        "type": "array",
                        "description": "Array of headline texts (3-15 required)",
                        "items": {"type": "string"},
                        "minItems": 3,
                        "maxItems": 15
                    },
                    "descriptions": {
                        "type": "array",
                        "description": "Array of description texts (2-4 required)",
                        "items": {"type": "string"},
                        "minItems": 2,
                        "maxItems": 4
                    },
                    "final_urls": {
                        "type": "array",
                        "description": "Array of final URLs",
                        "items": {"type": "string"}
                    },
                    "path1": {
                        "type": "string",
                        "description": "Display path 1"
                    },
                    "path2": {
                        "type": "string",
                        "description": "Display path 2"
                    }
                },
                "required": ["customer_id", "ad_group_resource_name", "headlines", "descriptions", "final_urls"]
            }
        ),
        types.Tool(
            name="get_smart_recommendations", 
            description="Get AI-powered recommendations based on successful patterns and account context",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID"
                    },
                    "goal": {
                        "type": "string", 
                        "description": "Business goal (e.g., 'increase leads', 'reduce CPA', 'expand to new markets')"
                    },
                    "context": {
                        "type": "string",
                        "description": "Additional context about business, budget, timeline, etc."
                    }
                },
                "required": ["customer_id", "goal"]
            }
        ),
        types.Tool(
            name="execute_any_operation",
            description="Execute ANY Google Ads API operation with intelligent assistance",
            inputSchema={
                "type": "object", 
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Google Ads customer ID"
                    },
                    "operation_description": {
                        "type": "string",
                        "description": "Natural language description of what you want to do"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Optional parameters like budget, targeting, etc."
                    }
                },
                "required": ["customer_id", "operation_description"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Handle tool calls"""
    if arguments is None:
        arguments = {}
    
    try:
        if name == "search_campaigns":
            result = await search_campaigns(
                customer_id=arguments["customer_id"],
                limit=arguments.get("limit", 10)
            )
        elif name == "run_gaql":
            result = await run_gaql(
                customer_id=arguments["customer_id"],
                query=arguments["query"],
                parallel=arguments.get("parallel", False),
                login_customer_id=arguments.get("login_customer_id")
            )
        elif name == "get_account_info":
            result = await get_account_info(
                customer_id=arguments["customer_id"]
            )
        elif name == "mutate_campaign":
            result = await mutate_campaign(
                customer_id=arguments["customer_id"],
                campaign_id=arguments["campaign_id"],
                updates=arguments["updates"]
            )
        elif name == "lookup_docs":
            result = await lookup_docs(
                resource=arguments["resource"]
            )
        elif name == "get_ai_context":
            result = await get_ai_context(
                operation_type=arguments.get("operation_type")
            )
        elif name == "api_call":
            result = await api_call(
                endpoint=arguments["endpoint"],
                customer_id=arguments["customer_id"],
                method=arguments.get("method", "POST"),
                data=arguments.get("data", {}),
                login_customer_id=arguments.get("login_customer_id")
            )
        elif name == "create_campaign_budget":
            result = await create_campaign_budget(
                customer_id=arguments["customer_id"],
                name=arguments["name"],
                amount_micros=arguments["amount_micros"],
                delivery_method=arguments.get("delivery_method", "STANDARD")
            )
        elif name == "create_campaign":
            result = await create_campaign(
                customer_id=arguments["customer_id"],
                name=arguments["name"],
                budget_resource_name=arguments["budget_resource_name"],
                bidding_strategy_type=arguments.get("bidding_strategy_type", "MAXIMIZE_CONVERSIONS"),
                target_cpa_micros=arguments.get("target_cpa_micros"),
                target_roas=arguments.get("target_roas"),
                geo_target_constants=arguments.get("geo_target_constants", []),
                status=arguments.get("status", "PAUSED")
            )
        elif name == "create_ad_group":
            result = await create_ad_group(
                customer_id=arguments["customer_id"],
                campaign_resource_name=arguments["campaign_resource_name"],
                name=arguments["name"],
                cpc_bid_micros=arguments["cpc_bid_micros"],
                status=arguments.get("status", "ENABLED")
            )
        elif name == "create_keywords":
            result = await create_keywords(
                customer_id=arguments["customer_id"],
                ad_group_resource_name=arguments["ad_group_resource_name"],
                keywords=arguments["keywords"]
            )
        elif name == "create_responsive_search_ad":
            result = await create_responsive_search_ad(
                customer_id=arguments["customer_id"],
                ad_group_resource_name=arguments["ad_group_resource_name"],
                headlines=arguments["headlines"],
                descriptions=arguments["descriptions"],
                final_urls=arguments["final_urls"],
                path1=arguments.get("path1"),
                path2=arguments.get("path2")
            )
        elif name == "get_smart_recommendations":
            result = await get_smart_recommendations(
                customer_id=arguments["customer_id"],
                goal=arguments["goal"],
                context=arguments.get("context", "")
            )
        elif name == "execute_any_operation":
            result = await execute_any_operation(
                customer_id=arguments["customer_id"],
                operation_description=arguments["operation_description"],
                parameters=arguments.get("parameters", {})
            )
        else:
            raise ValueError(f"Unknown tool: {name}")
        
        # Auto-inject AI context when there are errors or for guidance
        should_include_context = (
            "error" in result or 
            name in ["lookup_docs", "get_ai_context"] or
            (isinstance(result, dict) and not result.get("results"))
        )
        
        if should_include_context:
            ai_context = await get_ai_context()
            result["ai_guidance"] = {
                "proven_queries": ai_context["context"]["ai_guidance"]["proven_queries"][-3:],  # Last 3 successful
                "best_practices": ai_context["context"]["ai_guidance"]["best_practices"],
                "common_errors_to_avoid": ai_context["context"]["ai_guidance"]["common_errors_to_avoid"],
                "working_customer_ids": ai_context["context"]["successful_patterns"]["working_customer_ids"]
            }
        
        return [
            types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )
        ]
    except Exception as e:
        # Always include AI guidance when there's an exception
        ai_context = await get_ai_context()
        error_result = {
            "error": str(e),
            "ai_guidance": {
                "proven_queries": ai_context["context"]["ai_guidance"]["proven_queries"][-3:],
                "best_practices": ai_context["context"]["ai_guidance"]["best_practices"],
                "common_errors_to_avoid": ai_context["context"]["ai_guidance"]["common_errors_to_avoid"],
                "working_customer_ids": ai_context["context"]["successful_patterns"]["working_customer_ids"]
            }
        }
        
        return [
            types.TextContent(
                type="text",
                text=json.dumps(error_result, indent=2, ensure_ascii=False)
            )
        ]

async def search_campaigns(customer_id: str, limit: int = 10) -> dict[str, Any]:
    """Search for campaigns in the specified customer account"""
    query = f"""
        SELECT 
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros
        FROM campaign
        WHERE campaign.status != 'REMOVED'
        LIMIT {limit}
    """
    
    return await run_gaql(customer_id, query)

async def get_account_info(customer_id: str) -> dict[str, Any]:
    """Get basic account information"""
    query = """
        SELECT 
            customer.id,
            customer.descriptive_name,
            customer.currency_code,
            customer.time_zone,
            customer.auto_tagging_enabled,
            customer.pay_per_conversion_eligibility_failure_reasons
        FROM customer
        WHERE customer.id = customer.id
    """
    
    return await run_gaql(customer_id, query)

async def run_gaql(customer_id: str, query: str, parallel: bool = False, login_customer_id: Optional[str] = None) -> dict[str, Any]:
    """Execute a GAQL query with automatic retry for child account access"""
    data = {
        "query": query
    }
    
    # First attempt - use provided login_customer_id or none
    result = make_google_ads_request(f"customers/{customer_id}/googleAds:search", data, "POST", login_customer_id)
    
    # Check for 403 Forbidden error and retry with ROOT_MCC if accessing child account
    if "error" in result and "403" in str(result["error"]) and login_customer_id is None and customer_id != ROOT_MCC:
        print(f"Retrying with login_customer_id={ROOT_MCC} for child account {customer_id}", file=sys.stderr)
        result = make_google_ads_request(f"customers/{customer_id}/googleAds:search", data, "POST", ROOT_MCC)
    
    # Check if we got empty results and suggest documentation lookup
    results = result.get("results", [])
    error = result.get("error")
    
    # Log successful calls
    if not error and results:
        api_logger.log_success(
            operation_type="gaql_query",
            customer_id=customer_id,
            query=query,
            result_count=len(results),
            context={
                "parallel": parallel,
                "login_customer_id": login_customer_id or (ROOT_MCC if customer_id != ROOT_MCC else None)
            }
        )
    
    if not results and not error:
        result["suggestion"] = f"No rows returned. Check ai_guidance below for proven query patterns."
    
    # Always include minimal context for failed queries
    if error or not results:
        patterns = api_logger.get_patterns("gaql_query")
        if patterns["successful_queries"]:
            result["recent_successful_queries"] = [
                q["query"] for q in patterns["successful_queries"][-2:] 
                if q["customer_id"] == customer_id
            ]
    
    return {
        "customer_id": customer_id,
        "query": query,
        "parallel": parallel,
        "login_customer_id": login_customer_id or (ROOT_MCC if customer_id != ROOT_MCC else None),
        "results": results,
        "error": error,
        "suggestion": result.get("suggestion")
    }

async def mutate_campaign(customer_id: str, campaign_id: str, updates: dict) -> dict[str, Any]:
    """Update campaign settings like ROAS targets or budgets"""
    
    # Build the campaign mutation
    operation = {
        "update": {
            "resource_name": f"customers/{customer_id}/campaigns/{campaign_id}"
        }
    }
    
    # Build update mask based on provided updates
    update_mask_fields = []
    
    # Handle different ROAS field structures
    if "target_roas" in updates:
        # For standard bidding strategies using target_roas field
        operation["update"]["target_roas"] = {"target_roas": updates["target_roas"]}
        update_mask_fields.append("target_roas.target_roas")
    
    if "maximize_conversion_value" in updates:
        # For maximize conversion value bidding strategy
        operation["update"]["maximize_conversion_value"] = updates["maximize_conversion_value"]
        if "target_roas" in updates["maximize_conversion_value"]:
            update_mask_fields.append("maximize_conversion_value.target_roas")
    
    # Handle direct maximize_conversion_value target_roas updates
    if "mcv_target_roas" in updates:
        operation["update"]["maximize_conversion_value"] = {"target_roas": updates["mcv_target_roas"]}
        update_mask_fields.append("maximize_conversion_value.target_roas")
    
    if "daily_budget_micros" in updates:
        operation["update"]["campaign_budget"] = {"amount_micros": updates["daily_budget_micros"]}
        update_mask_fields.append("campaign_budget.amount_micros")
    
    if "status" in updates:
        operation["update"]["status"] = updates["status"]
        update_mask_fields.append("status")
    
    # Ensure we have an update mask
    if not update_mask_fields:
        return {
            "customer_id": customer_id,
            "campaign_id": campaign_id,
            "updates": updates,
            "error": "No valid fields provided for update. Use 'mcv_target_roas' for maximize conversion value campaigns."
        }
    
    operation["update_mask"] = ",".join(update_mask_fields)
    
    data = {
        "operations": [operation]
    }
    
    # Use ROOT_MCC if accessing child account
    login_customer_id = ROOT_MCC if customer_id != ROOT_MCC else None
    result = make_google_ads_request(f"customers/{customer_id}/campaigns:mutate", data, "POST", login_customer_id, "campaign_creation")
    
    # Log successful mutations
    if not result.get("error") and result.get("results"):
        api_logger.log_success(
            operation_type="campaign_mutation",
            customer_id=customer_id,
            query=f"UPDATE campaign {campaign_id}: {update_mask_fields}",
            result_count=len(result.get("results", [])),
            context={
                "campaign_id": campaign_id,
                "updates": updates,
                "update_mask": operation["update_mask"],
                "login_customer_id": login_customer_id
            }
        )
    
    return {
        "customer_id": customer_id,
        "campaign_id": campaign_id,
        "updates": updates,
        "operation": operation,
        "result": result.get("results", []),
        "error": result.get("error")
    }

async def lookup_docs(resource: str) -> dict[str, Any]:
    """Provide documentation links and field examples for Google Ads API resources"""
    
    docs_info = {
        "campaign": {
            "description": "Campaign resource for managing advertising campaigns",
            "common_fields": [
                "campaign.id", "campaign.name", "campaign.status", 
                "campaign.target_roas.target_roas", "campaign.maximize_conversion_value.target_roas",
                "campaign.bidding_strategy_type", "campaign.advertising_channel_type", "campaign.campaign_budget"
            ],
            "example_query": "SELECT campaign.id, campaign.name, campaign.maximize_conversion_value.target_roas FROM campaign WHERE campaign.status = 'ENABLED'",
            "mutation_examples": {
                "update_mcv_roas": {
                    "description": "Update ROAS for maximize conversion value campaigns",
                    "example": "mutate_campaign(customer_id='123', campaign_id='456', updates={'mcv_target_roas': 27.5})"
                },
                "update_standard_roas": {
                    "description": "Update ROAS for standard bidding strategies", 
                    "example": "mutate_campaign(customer_id='123', campaign_id='456', updates={'target_roas': 27.5})"
                },
                "update_maximize_conversion_value": {
                    "description": "Update maximize conversion value settings",
                    "example": "mutate_campaign(customer_id='123', campaign_id='456', updates={'maximize_conversion_value': {'target_roas': 27.5}})"
                }
            },
            "docs_url": "https://developers.google.com/google-ads/api/reference/rpc/v20/Campaign"
        },
        "customer": {
            "description": "Customer account information", 
            "common_fields": [
                "customer.id", "customer.descriptive_name", "customer.currency_code",
                "customer.time_zone", "customer.auto_tagging_enabled"
            ],
            "example_query": "SELECT customer.id, customer.descriptive_name FROM customer",
            "docs_url": "https://developers.google.com/google-ads/api/reference/rpc/v20/Customer"
        },
        "customer_client": {
            "description": "Manager-client relationship information",
            "common_fields": [
                "customer_client.id", "customer_client.descriptive_name", 
                "customer_client.status", "customer_client.level"
            ],
            "example_query": "SELECT customer_client.id, customer_client.descriptive_name FROM customer_client",
            "docs_url": "https://developers.google.com/google-ads/api/reference/rpc/v20/CustomerClient"
        },
        "GoogleAdsService": {
            "description": "Main service for querying Google Ads data",
            "methods": ["search", "searchStream", "mutate"],
            "gaql_reference": "https://developers.google.com/google-ads/api/docs/query/overview",
            "common_errors": {
                "403_forbidden": "Add login_customer_id header for child accounts",
                "400_bad_request": "Check GAQL syntax and field names",
                "empty_results": "Verify customer_id and query conditions"
            }
        }
    }
    
    if resource.lower() in docs_info:
        return {
            "resource": resource,
            "info": docs_info[resource.lower()],
            "status": "found"
        }
    else:
        return {
            "resource": resource,
            "error": f"No documentation found for '{resource}'",
            "available_resources": list(docs_info.keys()),
            "status": "not_found"
        }

async def get_ai_context(operation_type: str = None) -> dict[str, Any]:
    """Get AI context from successful API patterns"""
    
    patterns = api_logger.get_patterns(operation_type)
    
    # Build AI guidance based on successful patterns
    context = {
        "successful_patterns": patterns,
        "ai_guidance": {
            "proven_queries": [],
            "working_customer_ids": patterns["working_customer_ids"],
            "best_practices": [],
            "common_errors_to_avoid": []
        }
    }
    
    # Analyze successful queries for patterns
    for query_info in patterns["successful_queries"]:
        if query_info["result_count"] > 0:
            context["ai_guidance"]["proven_queries"].append({
                "template": query_info["query"],
                "customer_id": query_info["customer_id"],
                "operation": query_info["operation"],
                "result_count": query_info["result_count"]
            })
    
    # Add best practices based on learned patterns
    if operation_type == "gaql_query" or operation_type is None:
        context["ai_guidance"]["best_practices"].extend([
            "Use specific field names like 'campaign.maximize_conversion_value.target_roas' for MCV campaigns",
            "Always include WHERE clauses to filter results effectively", 
            "Use segments.date DURING YESTERDAY for date filtering",
            "Include login_customer_id for child account access",
            f"Known working customer IDs: {patterns['working_customer_ids']}"
        ])
        
        context["ai_guidance"]["common_errors_to_avoid"].extend([
            "Don't use 'segments.date = YESTERDAY' - use 'DURING YESTERDAY'",
            "Don't forget login_customer_id for child accounts (403 errors)",
            "Don't use complex JOINs in GAQL - keep queries simple",
            "Don't use campaign.target_roas.target_roas for MCV campaigns - use maximize_conversion_value.target_roas"
        ])
    
    if operation_type == "campaign_mutation" or operation_type is None:
        context["ai_guidance"]["best_practices"].extend([
            "Use 'maximize_conversion_value': {'target_roas': X} for MCV campaigns",
            "Always include proper update_mask: 'maximize_conversion_value.target_roas'",
            "Use mcv_target_roas shorthand for convenience"
        ])
        
        context["ai_guidance"]["common_errors_to_avoid"].extend([
            "Don't use 'target_roas': {'target_roas': X} for MCV campaigns",
            "Don't forget the update_mask - it's required for mutations",
            "Don't omit login_customer_id for child account mutations"
        ])
    
    return {
        "operation_type": operation_type or "all",
        "context": context,
        "summary": f"Found {len(patterns['successful_queries'])} successful patterns",
        "last_updated": datetime.now().isoformat()
    }

async def api_call(endpoint: str, customer_id: str, method: str = "POST", data: dict = None, login_customer_id: Optional[str] = None) -> dict[str, Any]:
    """Make any Google Ads API call - campaigns, ad groups, keywords, budgets, etc."""
    
    # Auto-set login_customer_id for child accounts if not provided
    if login_customer_id is None and customer_id != ROOT_MCC:
        login_customer_id = ROOT_MCC
    
    # Format endpoint with customer_id if it contains placeholder
    if "{customer_id}" in endpoint:
        endpoint = endpoint.replace("{customer_id}", customer_id)
    
    # Make the API request
    result = make_google_ads_request(endpoint, data or {}, method, login_customer_id)
    
    # Log successful API calls
    if not result.get("error"):
        operation_type = "api_call"
        if "mutate" in endpoint:
            operation_type = "mutation"
        elif "search" in endpoint:
            operation_type = "search"
        elif endpoint.endswith(":list") or method.upper() == "GET":
            operation_type = "list"
        
        # Create a query-like description for logging
        query_description = f"{method.upper()} {endpoint}"
        if data:
            query_description += f" with data: {json.dumps(data, separators=(',', ':'))[:100]}"
        
        api_logger.log_success(
            operation_type=operation_type,
            customer_id=customer_id,
            query=query_description,
            result_count=len(result.get("results", [])) if isinstance(result.get("results"), list) else (1 if result.get("results") else 0),
            context={
                "endpoint": endpoint,
                "method": method,
                "login_customer_id": login_customer_id,
                "has_data": bool(data)
            }
        )
    
    return {
        "customer_id": customer_id,
        "endpoint": endpoint,
        "method": method,
        "login_customer_id": login_customer_id,
        "data": data,
        "result": result.get("results", result),
        "error": result.get("error")
    }

async def create_campaign_budget(customer_id: str, name: str, amount_micros: int, delivery_method: str = "STANDARD") -> dict[str, Any]:
    """Create a new campaign budget"""
    
    data = {
        "operations": [{
            "create": {
                "name": name,
                "amount_micros": amount_micros,
                "delivery_method": delivery_method,
                "period": "DAILY",
                "explicitly_shared": False  # Required for smart bidding strategies
            }
        }]
    }
    
    # Use ROOT_MCC if accessing child account
    login_customer_id = ROOT_MCC if customer_id != ROOT_MCC else None
    result = make_google_ads_request(f"customers/{customer_id}/campaignBudgets:mutate", data, "POST", login_customer_id, "budget_creation")
    
    # Log successful creations
    if not result.get("error") and result.get("results"):
        api_logger.log_success(
            operation_type="budget_creation",
            customer_id=customer_id,
            query=f"CREATE budget {name}: {amount_micros} micros",
            result_count=len(result.get("results", [])),
            context={
                "name": name,
                "amount_micros": amount_micros,
                "delivery_method": delivery_method,
                "login_customer_id": login_customer_id
            }
        )
    
    return {
        "customer_id": customer_id,
        "budget_name": name,
        "amount_micros": amount_micros,
        "delivery_method": delivery_method,
        "result": result.get("results", []),
        "error": result.get("error")
    }

async def create_campaign(customer_id: str, name: str, budget_resource_name: str, 
                         bidding_strategy_type: str = "MANUAL_CPC",
                         target_cpa_micros: Optional[int] = None,
                         target_roas: Optional[float] = None,
                         geo_target_constants: list = None,
                         status: str = "PAUSED") -> dict[str, Any]:
    """Create a new search campaign"""
    
    campaign_data = {
        "name": name,
        "status": status,
        "advertising_channel_type": "SEARCH",
        "campaign_budget": budget_resource_name,
        "network_settings": {
            "target_google_search": True,
            "target_search_network": True,
            "target_partner_search_network": False,
            "target_content_network": False
        },
        "geo_target_type_setting": {
            "positive_geo_target_type": "PRESENCE_OR_INTEREST",
            "negative_geo_target_type": "PRESENCE"
        }
    }
    
    # Set bidding strategy - supports ALL Google Ads bidding strategies
    if bidding_strategy_type == "MAXIMIZE_CONVERSIONS":
        campaign_data["maximize_conversions"] = {}
        if target_cpa_micros:
            campaign_data["maximize_conversions"]["target_cpa_micros"] = target_cpa_micros
    elif bidding_strategy_type == "MAXIMIZE_CONVERSION_VALUE":
        campaign_data["maximize_conversion_value"] = {}
        if target_roas:
            campaign_data["maximize_conversion_value"]["target_roas"] = target_roas
    elif bidding_strategy_type == "MAXIMIZE_CLICKS":
        campaign_data["maximize_clicks"] = {}
        if target_cpa_micros:  # Daily budget cap for max clicks
            campaign_data["maximize_clicks"]["target_spend_micros"] = target_cpa_micros
    elif bidding_strategy_type == "TARGET_CPA":
        campaign_data["target_cpa"] = {"target_cpa_micros": target_cpa_micros or 50000000}
    elif bidding_strategy_type == "TARGET_ROAS":
        campaign_data["target_roas"] = {"target_roas": target_roas or 4.0}
    elif bidding_strategy_type == "TARGET_IMPRESSION_SHARE":
        campaign_data["target_impression_share"] = {
            "target_impression_share_micros": int((target_roas or 0.5) * 1000000),  # Use target_roas field for impression share %
            "cpc_bid_ceiling_micros": target_cpa_micros or 10000000,  # Max CPC bid
            "location": "SEARCH_PAGE_TOP"  # Default to top of search page
        }
    elif bidding_strategy_type == "TARGET_CPM":
        campaign_data["target_cpm"] = {"target_cpm_micros": target_cpa_micros or 5000000}
    elif bidding_strategy_type == "TARGET_SPEND":
        campaign_data["target_spend"] = {"target_spend_micros": target_cpa_micros or 50000000}
    elif bidding_strategy_type == "MANUAL_CPC":
        campaign_data["manual_cpc"] = {}
    elif bidding_strategy_type == "MANUAL_CPM":
        campaign_data["manual_cpm"] = {}
    elif bidding_strategy_type == "MANUAL_CPV":
        campaign_data["manual_cpv"] = {}
    elif bidding_strategy_type == "COMMISSION":
        campaign_data["commission"] = {"commission_rate_micros": int((target_roas or 0.05) * 1000000)}  # 5% default
    elif bidding_strategy_type == "PERCENT_CPC":
        campaign_data["percent_cpc"] = {"cpc_bid_ceiling_micros": target_cpa_micros or 10000000}
    else:
        # Default to Manual CPC if strategy not recognized
        campaign_data["manual_cpc"] = {}
    
    # Only create the campaign first, location targeting will be done separately
    data = {
        "operations": [{
            "create": campaign_data
        }]
    }
    
    # Use ROOT_MCC if accessing child account
    login_customer_id = ROOT_MCC if customer_id != ROOT_MCC else None
    result = make_google_ads_request(f"customers/{customer_id}/campaigns:mutate", data, "POST", login_customer_id, "campaign_creation")
    
    # Log successful creations
    if not result.get("error") and result.get("results"):
        api_logger.log_success(
            operation_type="campaign_creation",
            customer_id=customer_id,
            query=f"CREATE campaign {name}: {bidding_strategy_type}",
            result_count=len(result.get("results", [])),
            context={
                "name": name,
                "bidding_strategy_type": bidding_strategy_type,
                "budget_resource_name": budget_resource_name,
                "status": status,
                "login_customer_id": login_customer_id
            }
        )
    
    return {
        "customer_id": customer_id,
        "campaign_name": name,
        "bidding_strategy_type": bidding_strategy_type,
        "status": status,
        "result": result.get("results", []),
        "error": result.get("error")
    }

async def create_ad_group(customer_id: str, campaign_resource_name: str, name: str, 
                         cpc_bid_micros: int, status: str = "ENABLED") -> dict[str, Any]:
    """Create a new ad group"""
    
    data = {
        "operations": [{
            "create": {
                "name": name,
                "status": status,
                "campaign": campaign_resource_name,
                "cpc_bid_micros": cpc_bid_micros
            }
        }]
    }
    
    # Use ROOT_MCC if accessing child account
    login_customer_id = ROOT_MCC if customer_id != ROOT_MCC else None
    result = make_google_ads_request(f"customers/{customer_id}/adGroups:mutate", data, "POST", login_customer_id)
    
    # Log successful creations
    if not result.get("error") and result.get("results"):
        api_logger.log_success(
            operation_type="ad_group_creation",
            customer_id=customer_id,
            query=f"CREATE ad_group {name}: {cpc_bid_micros} micros",
            result_count=len(result.get("results", [])),
            context={
                "name": name,
                "campaign_resource_name": campaign_resource_name,
                "cpc_bid_micros": cpc_bid_micros,
                "status": status,
                "login_customer_id": login_customer_id
            }
        )
    
    return {
        "customer_id": customer_id,
        "ad_group_name": name,
        "campaign_resource_name": campaign_resource_name,
        "cpc_bid_micros": cpc_bid_micros,
        "status": status,
        "result": result.get("results", []),
        "error": result.get("error")
    }

async def create_keywords(customer_id: str, ad_group_resource_name: str, keywords: list) -> dict[str, Any]:
    """Create keywords in an ad group"""
    
    operations = []
    for keyword in keywords:
        operations.append({
            "create": {
                "ad_group": ad_group_resource_name,
                "status": "ENABLED",
                "keyword": {
                    "text": keyword["text"],
                    "match_type": keyword["match_type"]
                }
            }
        })
    
    data = {"operations": operations}
    
    # Use ROOT_MCC if accessing child account
    login_customer_id = ROOT_MCC if customer_id != ROOT_MCC else None
    result = make_google_ads_request(f"customers/{customer_id}/adGroupCriteria:mutate", data, "POST", login_customer_id)
    
    # Log successful creations
    if not result.get("error") and result.get("results"):
        api_logger.log_success(
            operation_type="keyword_creation",
            customer_id=customer_id,
            query=f"CREATE {len(keywords)} keywords in {ad_group_resource_name}",
            result_count=len(result.get("results", [])),
            context={
                "ad_group_resource_name": ad_group_resource_name,
                "keywords": keywords,
                "login_customer_id": login_customer_id
            }
        )
    
    return {
        "customer_id": customer_id,
        "ad_group_resource_name": ad_group_resource_name,
        "keywords_count": len(keywords),
        "result": result.get("results", []),
        "error": result.get("error")
    }

def validate_ad_text(headlines: list, descriptions: list) -> dict[str, list]:
    """Validate headlines and descriptions meet Google Ads character limits"""
    errors = []
    
    # Headlines max 30 characters
    for i, headline in enumerate(headlines):
        if len(headline) > 30:
            errors.append(f"Headline {i+1} too long ({len(headline)} chars): '{headline}'")
    
    # Descriptions max 90 characters  
    for i, description in enumerate(descriptions):
        if len(description) > 90:
            errors.append(f"Description {i+1} too long ({len(description)} chars): '{description}'")
    
    # Need at least 3 headlines and 2 descriptions
    if len(headlines) < 3:
        errors.append(f"Need at least 3 headlines, got {len(headlines)}")
    if len(descriptions) < 2:
        errors.append(f"Need at least 2 descriptions, got {len(descriptions)}")
        
    return {"valid": len(errors) == 0, "errors": errors}

async def create_responsive_search_ad(customer_id: str, ad_group_resource_name: str, 
                                     headlines: list, descriptions: list, final_urls: list,
                                     path1: Optional[str] = None, path2: Optional[str] = None) -> dict[str, Any]:
    """Create a responsive search ad"""
    
    # Validate text length
    validation = validate_ad_text(headlines, descriptions)
    if not validation["valid"]:
        return {
            "customer_id": customer_id,
            "ad_group_resource_name": ad_group_resource_name,
            "result": [],
            "error": f"Validation failed: {'; '.join(validation['errors'])}"
        }
    
    ad_data = {
        "ad_group": ad_group_resource_name,
        "status": "ENABLED",
        "ad": {
            "final_urls": final_urls,
            "responsive_search_ad": {
                "headlines": [{"text": headline} for headline in headlines],
                "descriptions": [{"text": description} for description in descriptions]
            }
        }
    }
    
    if path1:
        ad_data["ad"]["responsive_search_ad"]["path1"] = path1
    if path2:
        ad_data["ad"]["responsive_search_ad"]["path2"] = path2
    
    data = {
        "operations": [{
            "create": ad_data
        }]
    }
    
    # Use ROOT_MCC if accessing child account
    login_customer_id = ROOT_MCC if customer_id != ROOT_MCC else None
    result = make_google_ads_request(f"customers/{customer_id}/adGroupAds:mutate", data, "POST", login_customer_id)
    
    # Log successful creations
    if not result.get("error") and result.get("results"):
        api_logger.log_success(
            operation_type="ad_creation",
            customer_id=customer_id,
            query=f"CREATE responsive search ad in {ad_group_resource_name}",
            result_count=len(result.get("results", [])),
            context={
                "ad_group_resource_name": ad_group_resource_name,
                "headlines_count": len(headlines),
                "descriptions_count": len(descriptions),
                "final_urls": final_urls,
                "login_customer_id": login_customer_id
            }
        )
    
    return {
        "customer_id": customer_id,
        "ad_group_resource_name": ad_group_resource_name,
        "headlines_count": len(headlines),
        "descriptions_count": len(descriptions),
        "final_urls": final_urls,
        "result": result.get("results", []),
        "error": result.get("error")
    }

async def get_smart_recommendations(customer_id: str, goal: str, context: str = "") -> dict[str, Any]:
    """Get AI-powered recommendations based on successful patterns and account context"""
    
    # Get successful patterns from API log
    patterns = api_logger.get_patterns()
    
    # Get account information
    account_info = await get_account_info(customer_id)
    
    # Build context for recommendations
    recommendation_context = {
        "customer_id": customer_id,
        "goal": goal,
        "context": context,
        "successful_patterns": patterns["successful_queries"][-10:],  # Last 10 successful operations
        "working_customer_ids": patterns["working_customer_ids"],
        "account_info": account_info
    }
    
    # Analyze patterns and generate recommendations
    recommendations = []
    
    if "lead" in goal.lower() or "conversion" in goal.lower():
        recommendations.append({
            "strategy": "Maximize Conversions with Target CPA",
            "reason": "Best for lead generation goals",
            "implementation": "Use MAXIMIZE_CONVERSIONS bidding with target_cpa_micros based on your desired cost per lead"
        })
    
    if "roas" in goal.lower() or "revenue" in goal.lower():
        recommendations.append({
            "strategy": "Maximize Conversion Value with Target ROAS", 
            "reason": "Best for revenue optimization",
            "implementation": "Use MAXIMIZE_CONVERSION_VALUE bidding with target_roas based on your profit margins"
        })
    
    if "expand" in goal.lower() or "new market" in goal.lower():
        recommendations.append({
            "strategy": "Geographic Expansion Strategy",
            "reason": "Scale successful campaigns to new locations",
            "implementation": "Copy high-performing campaigns and adjust geo-targeting and bids for new markets"
        })
    
    return {
        "customer_id": customer_id,
        "goal": goal,
        "recommendations": recommendations,
        "context": recommendation_context,
        "next_steps": [
            "Review current campaign performance",
            "Identify top-performing keywords and ads",
            "Implement recommended bidding strategy",
            "Set up proper conversion tracking"
        ]
    }

async def execute_any_operation(customer_id: str, operation_description: str, parameters: dict = None) -> dict[str, Any]:
    """Execute ANY Google Ads API operation with intelligent assistance"""
    
    if parameters is None:
        parameters = {}
    
    # Parse the operation description to determine intent
    operation_lower = operation_description.lower()
    
    # Map common operations to API endpoints
    operation_mapping = {
        "create campaign": {"endpoint": "campaigns:mutate", "method": "POST"},
        "create ad group": {"endpoint": "adGroups:mutate", "method": "POST"},
        "create keywords": {"endpoint": "adGroupCriteria:mutate", "method": "POST"},
        "create ads": {"endpoint": "adGroupAds:mutate", "method": "POST"},
        "create budget": {"endpoint": "campaignBudgets:mutate", "method": "POST"},
        "create conversion": {"endpoint": "conversionActions:mutate", "method": "POST"},
        "update campaign": {"endpoint": "campaigns:mutate", "method": "POST"},
        "pause campaign": {"endpoint": "campaigns:mutate", "method": "POST"},
        "add negative keywords": {"endpoint": "campaignCriteria:mutate", "method": "POST"},
        "create audience": {"endpoint": "customAudiences:mutate", "method": "POST"},
        "create extension": {"endpoint": "extensionFeedItems:mutate", "method": "POST"},
        "upload conversions": {"endpoint": "conversionUploads:uploadClickConversions", "method": "POST"},
        "create shopping campaign": {"endpoint": "campaigns:mutate", "method": "POST"},
        "create performance max": {"endpoint": "campaigns:mutate", "method": "POST"},
        "create display campaign": {"endpoint": "campaigns:mutate", "method": "POST"}
    }
    
    # Determine the API endpoint
    endpoint_info = None
    for operation_key, endpoint_data in operation_mapping.items():
        if operation_key in operation_lower:
            endpoint_info = endpoint_data
            break
    
    if not endpoint_info:
        # Default to generic api_call for any unrecognized operation
        return {
            "customer_id": customer_id,
            "operation": operation_description,
            "error": "Operation not recognized. Please use the 'api_call' function with specific endpoint and data.",
            "suggestion": "Describe your goal in more detail or provide the specific API endpoint you want to use."
        }
    
    # Build the API call based on operation type
    endpoint = f"customers/{customer_id}/{endpoint_info['endpoint']}"
    
    # Generate intelligent operation data based on common patterns
    if "create campaign" in operation_lower:
        # Smart campaign creation with reasonable defaults
        budget_name = parameters.get("budget_name", f"Auto Budget {datetime.now().strftime('%Y%m%d_%H%M%S')}")
        campaign_name = parameters.get("campaign_name", f"Auto Campaign {datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        # First create budget if needed
        budget_result = await create_campaign_budget(
            customer_id=customer_id,
            name=budget_name,
            amount_micros=parameters.get("budget_micros", 50000000)  # Default $50/day
        )
        
        if budget_result.get("error"):
            return budget_result
            
        budget_rn = budget_result["result"][0]["resourceName"]
        
        # Then create campaign
        return await create_campaign(
            customer_id=customer_id,
            name=campaign_name,
            budget_resource_name=budget_rn,
            bidding_strategy_type=parameters.get("bidding_strategy", "MANUAL_CPC"),
            target_cpa_micros=parameters.get("target_cpa_micros"),
            target_roas=parameters.get("target_roas"),
            status=parameters.get("status", "PAUSED")
        )
    
    elif "conversion" in operation_lower and "create" in operation_lower:
        # Smart conversion action creation
        conversion_data = {
            "operations": [{
                "create": {
                    "name": parameters.get("name", "Auto Conversion Action"),
                    "category": parameters.get("category", "DEFAULT"),
                    "type": parameters.get("type", "WEBPAGE"),
                    "status": parameters.get("status", "ENABLED"),
                    "value_settings": {
                        "default_value": parameters.get("default_value", 1.0),
                        "default_currency_code": parameters.get("currency", "USD")
                    },
                    "counting_type": parameters.get("counting_type", "ONE_PER_CLICK")
                }
            }]
        }
        
        return await api_call(
            endpoint=endpoint,
            customer_id=customer_id,
            method=endpoint_info["method"],
            data=conversion_data
        )
    
    else:
        # For other operations, use the generic api_call with provided parameters
        return await api_call(
            endpoint=endpoint,
            customer_id=customer_id,
            method=endpoint_info["method"],
            data=parameters
        )

async def lookup_v20_docs(query: str) -> dict[str, Any]:
    """Look up Google Ads API v20 documentation for specific operations"""
    
    docs_path = Path("/mnt/c/Users/willi/OneDrive/Desktop/aio-v2/.ai/.docs/v20api")
    
    # Search through documentation files
    found_docs = []
    
    try:
        # Search HTML documentation
        html_path = docs_path / "google_ads_v20_docs" / "html"
        if html_path.exists():
            for html_file in html_path.glob("*.html"):
                if query.lower() in html_file.name.lower():
                    found_docs.append({
                        "file": str(html_file),
                        "type": "service_reference",
                        "service": html_file.stem
                    })
        
        # Search proto files for field definitions
        proto_path = docs_path / "google_ads_v20_docs" / "protos"
        if proto_path.exists():
            for proto_file in proto_path.rglob("*.proto"):
                try:
                    with open(proto_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if query.lower() in content.lower():
                            found_docs.append({
                                "file": str(proto_file),
                                "type": "proto_definition",
                                "relevant_content": content[:500] + "..." if len(content) > 500 else content
                            })
                except:
                    continue
        
        return {
            "query": query,
            "found_docs": found_docs[:10],  # Limit to top 10 results
            "docs_available": len(found_docs) > 0
        }
        
    except Exception as e:
        return {
            "query": query,
            "error": f"Error searching docs: {str(e)}",
            "docs_available": False
        }

async def main():
    """Main entry point for the MCP server"""
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="google-ads-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
