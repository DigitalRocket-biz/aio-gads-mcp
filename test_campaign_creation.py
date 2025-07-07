#!/usr/bin/env python3
"""
Test script for the enhanced Google Ads MCP server
Tests the complete campaign creation workflow
"""

import asyncio
import json
from datetime import datetime
from mcp_server import (
    create_campaign_budget,
    create_campaign, 
    create_ad_group,
    create_keywords,
    create_responsive_search_ad
)

async def test_complete_campaign_creation():
    """Test the complete campaign creation workflow"""
    
    customer_id = "2312146774"  # BizExplorer account
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("🚀 Testing Complete Campaign Creation Workflow")
    print("=" * 50)
    
    # Step 1: Create Campaign Budget
    print("\n1. Creating Campaign Budget...")
    budget_result = await create_campaign_budget(
        customer_id=customer_id,
        name=f"Buy Business & Franchise - Budget {timestamp}",
        amount_micros=65000000,  # $65/day
        delivery_method="STANDARD"
    )
    print(f"Budget Result: {json.dumps(budget_result, indent=2)}")
    
    if budget_result.get("error"):
        print("❌ Budget creation failed, stopping test")
        return
    
    budget_resource_name = budget_result.get("result", [{}])[0].get("resourceName")
    if not budget_resource_name:
        print("❌ No budget resource name returned, stopping test")
        return
    
    print(f"✅ Budget created: {budget_resource_name}")
    
    # Step 2: Create Campaign
    print("\n2. Creating Search Campaign...")
    campaign_result = await create_campaign(
        customer_id=customer_id,
        name=f"Buy Business & Franchise - Search {timestamp}",
        budget_resource_name=budget_resource_name,
        bidding_strategy_type="MANUAL_CPC",
        geo_target_constants=["2840"],  # United States
        status="PAUSED"
    )
    print(f"Campaign Result: {json.dumps(campaign_result, indent=2)}")
    
    if campaign_result.get("error"):
        print("❌ Campaign creation failed, stopping test")
        return
    
    campaign_resource_name = campaign_result.get("result", [{}])[0].get("resourceName")
    if not campaign_resource_name:
        print("❌ No campaign resource name returned, stopping test")
        return
    
    print(f"✅ Campaign created: {campaign_resource_name}")
    
    # Step 3: Create Ad Groups
    print("\n3. Creating Ad Groups...")
    
    ad_groups = [
        {"name": "Buy Business - Exact", "cpc_bid_micros": 3500000},
        {"name": "Buy Franchise - Exact", "cpc_bid_micros": 4000000},
        {"name": "Business Acquisition - Phrase", "cpc_bid_micros": 3000000},
        {"name": "Franchise Opportunities - Phrase", "cpc_bid_micros": 3500000}
    ]
    
    ad_group_resources = []
    
    for ad_group in ad_groups:
        print(f"  Creating ad group: {ad_group['name']}")
        ag_result = await create_ad_group(
            customer_id=customer_id,
            campaign_resource_name=campaign_resource_name,
            name=ad_group["name"],
            cpc_bid_micros=ad_group["cpc_bid_micros"],
            status="ENABLED"
        )
        
        if ag_result.get("error"):
            print(f"❌ Ad group creation failed: {ag_result['error']}")
            continue
        
        ag_resource_name = ag_result.get("result", [{}])[0].get("resourceName")
        if ag_resource_name:
            ad_group_resources.append({
                "name": ad_group["name"],
                "resource_name": ag_resource_name
            })
            print(f"✅ Ad group created: {ag_resource_name}")
    
    # Step 4: Create Keywords
    print("\n4. Creating Keywords...")
    
    keyword_sets = [
        {
            "ad_group": "Buy Business - Exact",
            "keywords": [
                {"text": "buy a business", "match_type": "EXACT"},
                {"text": "businesses for sale", "match_type": "EXACT"},
                {"text": "business for sale near me", "match_type": "EXACT"}
            ]
        },
        {
            "ad_group": "Buy Franchise - Exact",
            "keywords": [
                {"text": "buy a franchise", "match_type": "EXACT"},
                {"text": "franchise opportunities", "match_type": "EXACT"},
                {"text": "franchises for sale", "match_type": "EXACT"}
            ]
        },
        {
            "ad_group": "Business Acquisition - Phrase",
            "keywords": [
                {"text": "business acquisition services", "match_type": "PHRASE"},
                {"text": "acquiring a business", "match_type": "PHRASE"},
                {"text": "how to buy a business", "match_type": "PHRASE"}
            ]
        },
        {
            "ad_group": "Franchise Opportunities - Phrase",
            "keywords": [
                {"text": "best franchise opportunities", "match_type": "PHRASE"},
                {"text": "franchise business opportunities", "match_type": "PHRASE"},
                {"text": "available franchises", "match_type": "PHRASE"}
            ]
        }
    ]
    
    for keyword_set in keyword_sets:
        # Find matching ad group
        ag_resource = next((ag for ag in ad_group_resources if ag["name"] == keyword_set["ad_group"]), None)
        if not ag_resource:
            print(f"❌ Ad group not found: {keyword_set['ad_group']}")
            continue
        
        print(f"  Creating keywords for: {keyword_set['ad_group']}")
        kw_result = await create_keywords(
            customer_id=customer_id,
            ad_group_resource_name=ag_resource["resource_name"],
            keywords=keyword_set["keywords"]
        )
        
        if kw_result.get("error"):
            print(f"❌ Keywords creation failed: {kw_result['error']}")
        else:
            print(f"✅ Created {len(keyword_set['keywords'])} keywords")
    
    # Step 5: Create Responsive Search Ads
    print("\n5. Creating Responsive Search Ads...")
    
    headlines = [
        "Find Your Perfect Business",      # 26 chars
        "Businesses For Sale",            # 19 chars
        "Buy A Business Today",           # 21 chars
        "Franchise Opportunities",        # 24 chars
        "Business Ownership Journey",     # 27 chars
        "Available Franchises",           # 21 chars
        "Expert Business Help",           # 21 chars
        "Browse 1000s Businesses",        # 24 chars
        "Explore. Compare. Own.",         # 23 chars
        "Start Your Journey",             # 19 chars
        "Business Listings",              # 18 chars
        "Find Businesses",                # 16 chars
        "Your Next Business",             # 19 chars
        "Business Marketplace",           # 21 chars
        "Own Your Future"                 # 15 chars
    ]
    
    descriptions = [
        "Explore businesses and franchises for sale. Expert guidance included.",        # 76 chars
        "Find the perfect business opportunity. Browse by location and type.",         # 73 chars
        "Ready to be a business owner? Discover franchises and businesses now.",       # 74 chars
        "From automotive to retail - find your ideal business match today."           # 72 chars
    ]
    
    for ag_resource in ad_group_resources:
        print(f"  Creating ad for: {ag_resource['name']}")
        ad_result = await create_responsive_search_ad(
            customer_id=customer_id,
            ad_group_resource_name=ag_resource["resource_name"],
            headlines=headlines,
            descriptions=descriptions,
            final_urls=["https://bizexplorer.us/"],
            path1="buy-business",
            path2="opportunities"
        )
        
        if ad_result.get("error"):
            print(f"❌ Ad creation failed: {ad_result['error']}")
        else:
            print(f"✅ Responsive search ad created")
    
    print("\n🎉 Campaign Creation Test Complete!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_complete_campaign_creation())