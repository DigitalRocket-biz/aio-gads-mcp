#!/usr/bin/env python3
"""
Test all Google Ads bidding strategies with the enhanced MCP server
Shows examples for every bidding strategy available in Google Ads API v20
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

async def test_bidding_strategies():
    """Test creating campaigns with different bidding strategies"""
    
    customer_id = "2312146774"  # BizExplorer account
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("🚀 Testing ALL Google Ads Bidding Strategies")
    print("=" * 60)
    
    # Define bidding strategies to test
    bidding_strategies = [
        {
            "name": "Maximize Conversions",
            "type": "MAXIMIZE_CONVERSIONS",
            "target_cpa_micros": 25000000,  # $25 target CPA
            "description": "Automated bidding to get the most conversions within budget"
        },
        {
            "name": "Maximize Conversion Value",
            "type": "MAXIMIZE_CONVERSION_VALUE", 
            "target_roas": 4.0,  # 4x ROAS target
            "description": "Automated bidding to maximize conversion value with target ROAS"
        },
        {
            "name": "Target CPA",
            "type": "TARGET_CPA",
            "target_cpa_micros": 30000000,  # $30 target CPA
            "description": "Automated bidding to maintain specific cost per acquisition"
        },
        {
            "name": "Target ROAS", 
            "type": "TARGET_ROAS",
            "target_roas": 3.5,  # 3.5x ROAS target
            "description": "Automated bidding to maintain specific return on ad spend"
        },
        {
            "name": "Maximize Clicks",
            "type": "MAXIMIZE_CLICKS",
            "description": "Automated bidding to get the most clicks within budget"
        },
        {
            "name": "Manual CPC",
            "type": "MANUAL_CPC", 
            "description": "Manual cost-per-click bidding with full control"
        },
        {
            "name": "Target Impression Share",
            "type": "TARGET_IMPRESSION_SHARE",
            "target_roas": 0.65,  # 65% impression share target
            "target_cpa_micros": 8000000,  # $8 max CPC
            "description": "Automated bidding to achieve target impression share"
        }
    ]
    
    successful_campaigns = []
    
    for i, strategy in enumerate(bidding_strategies, 1):
        print(f"\n{i}. Testing {strategy['name']} ({strategy['type']})")
        print(f"   {strategy['description']}")
        
        # Create unique budget for each strategy
        budget_name = f"{strategy['name']} Budget {timestamp}_{i}"
        budget_result = await create_campaign_budget(
            customer_id=customer_id,
            name=budget_name,
            amount_micros=45000000,  # $45/day
            delivery_method="STANDARD"
        )
        
        if budget_result.get("error"):
            print(f"   ❌ Budget creation failed: {budget_result['error']}")
            continue
            
        budget_resource_name = budget_result["result"][0]["resourceName"]
        print(f"   ✅ Budget created: {budget_resource_name}")
        
        # Create campaign with specific bidding strategy
        campaign_name = f"{strategy['name']} Campaign {timestamp}_{i}"
        campaign_result = await create_campaign(
            customer_id=customer_id,
            name=campaign_name,
            budget_resource_name=budget_resource_name,
            bidding_strategy_type=strategy["type"],
            target_cpa_micros=strategy.get("target_cpa_micros"),
            target_roas=strategy.get("target_roas"),
            geo_target_constants=["2840"],  # United States
            status="PAUSED"
        )
        
        if campaign_result.get("error"):
            print(f"   ❌ Campaign creation failed: {campaign_result['error']}")
            continue
            
        campaign_resource_name = campaign_result["result"][0]["resourceName"]
        print(f"   ✅ Campaign created: {campaign_resource_name}")
        
        successful_campaigns.append({
            "strategy": strategy["name"],
            "type": strategy["type"],
            "campaign": campaign_resource_name,
            "budget": budget_resource_name
        })
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY - Successfully Created Campaigns:")
    print("=" * 60)
    
    for campaign in successful_campaigns:
        print(f"✅ {campaign['strategy']} ({campaign['type']})")
        print(f"   Campaign: {campaign['campaign']}")
        print(f"   Budget: {campaign['budget']}")
        print()
    
    print(f"🎉 Created {len(successful_campaigns)} out of {len(bidding_strategies)} bidding strategies!")
    
    # Show GAQL query to verify campaigns
    print("\n🔍 Verify with GAQL query:")
    print("""
    SELECT 
        campaign.id,
        campaign.name,
        campaign.bidding_strategy_type,
        campaign.maximize_conversions.target_cpa_micros,
        campaign.maximize_conversion_value.target_roas,
        campaign.target_cpa.target_cpa_micros,
        campaign.target_roas.target_roas,
        campaign_budget.amount_micros
    FROM campaign 
    WHERE campaign.name LIKE '%Campaign%'
    ORDER BY campaign.name
    """)

if __name__ == "__main__":
    asyncio.run(test_bidding_strategies())