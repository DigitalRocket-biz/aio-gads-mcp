# Google Ads MCP Server

**Enhanced Model Context Protocol server for Google Ads API v20 operations**

## 🚀 Features

- **Permanent Authentication** - Never expires, bulletproof JWT token system
- **Universal API Support** - Handle ANY Google Ads API v20 operation
- **Smart Learning System** - AI that learns from every successful operation
- **All Bidding Strategies** - Maximize Conversions, Target CPA/ROAS, Manual CPC, etc.
- **Complete Workflows** - Budget → Campaign → Ad Groups → Keywords → Ads
- **Character Validation** - Prevents text length errors automatically

## 🔧 Quick Start

### 1. Setup Environment
```bash
cp .env.example .env
# Add your authentication tokens
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run MCP Server
```bash
python mcp_server.py
```

## 🎯 Capabilities

### Core Operations
- **Campaign Creation** - Any campaign type with any bidding strategy
- **Budget Management** - Daily budgets with smart bidding support  
- **Ad Group Management** - With CPC bid optimization
- **Keyword Management** - All match types (Exact, Phrase, Broad)
- **Ad Creation** - Responsive search ads with validation
- **Conversion Tracking** - All 30+ conversion action types

### Smart AI Features
- **Learning System** - Captures patterns from every success
- **Smart Recommendations** - AI suggestions based on learned data
- **Natural Language Processing** - Describe goals, get implementations
- **Documentation Lookup** - Searches v20 API docs automatically

### Advanced Features
- **MCC Support** - Multi-account management
- **Bulk Operations** - Handle multiple operations efficiently
- **Error Prevention** - Learns from mistakes to avoid repeats
- **Custom Operations** - Execute any API endpoint directly

## 📊 Recent Successes

Successfully created and managed:
- ✅ **Multiple Campaigns** - Manual CPC, Maximize Conversions, Max Conv Value
- ✅ **Complete Workflows** - 16 ad groups, 48+ keywords, 16 responsive search ads
- ✅ **Smart Bidding** - Target CPA $20-30, Target ROAS 4.0x-15x
- ✅ **Account Management** - 80+ managed accounts through MCC

## 🧠 AI Learning

The system automatically learns from every successful operation:

```python
# Every API call builds intelligence
api_logger.log_success(
    operation_type="campaign_creation",
    customer_id="2312146774", 
    query="CREATE campaign: MAXIMIZE_CONVERSIONS",
    context={
        "bidding_strategy": "MAXIMIZE_CONVERSIONS",
        "target_cpa_micros": 25000000,
        "success_factors": ["proper_budget_type", "correct_headers"]
    }
)
```

## 🎯 Example Usage

### Simple Campaign Creation
```python
# Natural language to API translation
"Create a maximize conversions campaign for business acquisition with $75/day budget"
```

### Complex Workflows  
```python
# Multi-step operations
"Build a complete lead generation funnel with awareness, consideration, and conversion campaigns"
```

### Advanced Operations
```python
# Any API endpoint
"Set up conversion value rules to optimize for high-value business categories"
```

## 🔧 Configuration

### Environment Variables
- `PERMANENT_JWT_TOKEN` - Never-expiring authentication token
- `GOOGLE_ADS_PROXY_URL` - API proxy endpoint
- `GOOGLE_ADS_ORG_ID` - Organization identifier  
- `GOOGLE_ADS_LINKED_ACCOUNT_ID` - Account selector
- `GOOGLE_ADS_MCC_ID` - Manager customer ID

### API Learning
- `api_success_log.json` - Raw success data
- `ai_learning_context.json` - Processed AI insights

## 📚 Documentation

- [`FINAL_CAPABILITIES.md`](FINAL_CAPABILITIES.md) - Complete feature overview
- [`AI_PROMPT_CONTEXT.md`](AI_PROMPT_CONTEXT.md) - Smart prompting guide  
- [`CAMPAIGN_CREATION_GUIDE.md`](CAMPAIGN_CREATION_GUIDE.md) - Workflow examples

## 🎉 Why This MCP Server?

1. **Never Breaks** - Permanent authentication eliminates 401 errors
2. **Learns Continuously** - Gets smarter with every operation
3. **Handles Everything** - Literally any Google Ads API operation
4. **Production Ready** - Successfully managing real campaigns
5. **AI-Powered** - Natural language to API translation

Built for [DigitalRocket.biz](https://digitalrocket.biz) - **AI-Powered Marketing Automation**