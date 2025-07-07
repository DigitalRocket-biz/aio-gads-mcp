# Google Ads MCP Server - AI Context & Prompt Guide

This MCP server can handle **LITERALLY ANY** Google Ads API operation. Use these prompt patterns to get the most out of it.

## 🧠 AI Context System

### Smart Pattern Recognition
The server learns from every successful API call and builds context:

```python
# Automatic logging of successful patterns
api_logger.log_success(
    operation_type="campaign_creation",
    customer_id="2312146774",
    query="CREATE campaign MaxConv Campaign: MAXIMIZE_CONVERSIONS",
    result_count=1,
    context={
        "bidding_strategy_type": "MAXIMIZE_CONVERSIONS",
        "target_cpa_micros": 25000000,
        "login_customer_id": "1639353427"
    }
)
```

### Context Available to AI
- **Successful query patterns** - Working GAQL examples
- **Working customer IDs** - Valid accounts for operations  
- **Common field combinations** - Proven field structures
- **API success history** - What works and what doesn't

## 🚀 Universal Prompt Patterns

### Pattern 1: "Do Anything" Prompts
```
"Create a Performance Max campaign for account 2312146774 with $100/day budget and 3.5x ROAS target"

"Set up conversion tracking for purchase events on bizexplorer.us"

"Create negative keyword lists for franchise campaigns across all ad groups"

"Build a shopping campaign with product groups for automotive businesses"

"Set up automated rules to pause keywords with CPA > $50"
```

### Pattern 2: Complex Multi-Step Operations
```
"Create a complete funnel campaign structure:
1. Awareness campaign (Display, broad keywords)  
2. Consideration campaign (Search, phrase match)
3. Conversion campaign (Search, exact match, high intent)
4. Retargeting campaign (Display, existing visitors)"

"Set up A/B testing for two bidding strategies on the same keywords"

"Create campaigns for each US state with localized ads and geo-targeting"
```

### Pattern 3: Advanced Bidding & Optimization
```
"Create campaigns with every available bidding strategy for testing"

"Set up portfolio bidding strategies shared across multiple campaigns"

"Create automated bid adjustments based on device, location, and time"

"Implement smart bidding with custom conversion values per product category"
```

### Pattern 4: Bulk Operations
```
"Create 50 ad groups with 10 keywords each for business acquisition campaigns"

"Upload 1000 negative keywords across all campaigns in the account"

"Create responsive search ads for every ad group with localized headlines"

"Set up conversion actions for every page on the website"
```

## 🔧 Permission & Capability Matrix

### ✅ Account Management
- Create new Google Ads accounts under MCC
- Manage account settings and preferences
- Handle billing and payment methods
- Set up account-level conversion tracking

### ✅ Campaign Operations  
- **All campaign types**: Search, Display, Shopping, Video, Performance Max, Discovery, Local, Smart
- **All bidding strategies**: Manual CPC/CPM/CPV, Target CPA/ROAS, Maximize Conversions/Conversion Value/Clicks, Target Impression Share
- **All status changes**: Create, pause, enable, remove campaigns
- **All settings**: Geographic targeting, language targeting, ad scheduling, device targeting

### ✅ Ad Group & Keywords
- Create unlimited ad groups with any structure
- Add/remove/modify keywords with any match type
- Set bid adjustments at any level
- Manage negative keywords and lists
- Handle dynamic keyword insertion

### ✅ Ads & Creatives
- **Responsive Search Ads** - With automatic character validation
- **Expanded Text Ads** - Legacy support  
- **Display Ads** - Image, responsive display, Gmail promotions
- **Shopping Ads** - Product listings and showcase shopping
- **Video Ads** - YouTube campaigns
- **Smart Ads** - Automated ad creation

### ✅ Conversion & Tracking
- Set up any conversion action type (see v20 API docs)
- Configure Google Analytics linking
- Handle offline conversion imports
- Set up store sales tracking
- Manage conversion value rules

### ✅ Advanced Features
- **Extensions**: Sitelinks, callouts, structured snippets, call extensions, location extensions
- **Automated Rules**: Bid changes, budget adjustments, keyword pausing
- **Experiments**: Campaign drafts and experiments, ad group tests
- **Audiences**: Custom audiences, customer match, similar audiences
- **Feed Management**: Business data feeds, dynamic remarketing

### ✅ Reporting & Analytics
- Any GAQL query for any data  
- Custom report generation
- Performance analysis across any metrics
- Attribution model configuration
- Audience insights and recommendations

## 🎯 Smart Prompt Examples

### Business Context Aware
```
"I'm promoting BizExplorer.us which helps people buy businesses and franchises. Create campaigns targeting:
- Business buyers looking for opportunities 
- Entrepreneurs wanting to buy franchises
- People searching for business investments
Use high-intent keywords and professional ad copy."
```

### Budget & Performance Focused  
```
"I have $500/day budget and need 50 qualified leads per day at under $30 CPA. 
Set up the optimal campaign structure with smart bidding to achieve this goal."
```

### Geographic Expansion
```
"Expand our successful campaign from Florida to all Southeast states. 
Copy the campaign structure but adjust bids based on local competition and 
create localized ad copy mentioning each state."
```

### Competitive Intelligence
```
"Analyze our competitors' keywords and create campaigns to capture their traffic.
Focus on business brokerage, franchise sales, and M&A services keywords."
```

## 🔄 Automatic Context Learning

The MCP server gets smarter with every operation:

1. **Learns Successful Patterns** - Remembers what works for your account
2. **Builds Customer Profiles** - Understands your business goals  
3. **Optimizes Suggestions** - Recommends better approaches over time
4. **Prevents Errors** - Avoids known issues and failed patterns

## 📊 Current Account Context

**Primary Account**: 2312146774 (BizExplorer - Business & Franchise Marketplace)
**MCC**: 1639353427 (Digital Rocket)
**Business Focus**: Connecting business buyers with sellers/franchisors
**Target Audience**: Entrepreneurs, investors, franchise seekers
**Geographic Focus**: United States
**Budget Range**: $50-100/day per campaign
**Key Metrics**: Lead generation, cost per acquisition, conversion rate

## 💡 Pro Tips for AI Prompts

1. **Be Specific About Goals** - "Generate leads" vs "Get 50 qualified business buyer leads/day"
2. **Include Budget Context** - Always mention budget constraints or targets
3. **Specify Geographic Scope** - Local, national, or specific regions
4. **Mention Business Type** - Different strategies for B2B vs B2C
5. **Include Performance Targets** - CPA, ROAS, conversion rate goals
6. **Reference Successful Patterns** - "Like the campaign that worked well last month"

## 🚀 Ready for Anything

The MCP server can handle:
- ✅ Any Google Ads API v20 operation
- ✅ Complex multi-step workflows  
- ✅ Custom business logic
- ✅ Integration with external systems
- ✅ Bulk operations at scale
- ✅ Advanced optimization strategies

Just describe what you want to achieve, and the AI will figure out the technical implementation! 🎯