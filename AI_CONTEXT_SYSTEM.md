# Auto-Context AI Learning System

## 🧠 How It Works

The MCP server now **automatically feeds AI context** in these situations:

### 1. **Always Auto-Inject When:**
- ❌ Any API call returns an error
- 📭 Query returns empty results 
- 📚 Using `lookup_docs` or `get_ai_context` tools
- 💥 Any exception occurs

### 2. **What Gets Injected:**
```json
{
  "result": "... normal response ...",
  "ai_guidance": {
    "proven_queries": ["SELECT customer_client.id...", "SELECT campaign.maximize_conversion_value..."],
    "best_practices": [
      "Use segments.date DURING YESTERDAY for dates",
      "Include login_customer_id for child accounts",
      "Use maximize_conversion_value.target_roas for MCV campaigns"
    ],
    "common_errors_to_avoid": [
      "Don't use segments.date = 'YESTERDAY'",
      "Don't forget update_mask for mutations"
    ],
    "working_customer_ids": ["1639353427", "5292473333"]
  }
}
```

### 3. **Learning Patterns:**
- ✅ **Every successful call** → logged automatically
- 🔄 **Failed query** → shows recent successful queries for same customer
- 📈 **Pattern recognition** → identifies what works vs what fails
- 🎯 **Context filtering** → only shows relevant patterns

## 🚀 Benefits

1. **AI learns from every interaction** - no manual pattern teaching needed
2. **Immediate context on failures** - AI sees what works when something breaks  
3. **Accumulating intelligence** - gets smarter over time
4. **Zero overhead on success** - only adds context when needed

## 📝 Example Auto-Context Response

When a GAQL query fails:
```json
{
  "error": "400 Bad Request",
  "ai_guidance": {
    "proven_queries": [
      "SELECT campaign.maximize_conversion_value.target_roas FROM campaign WHERE campaign.id = 21365703104"
    ],
    "working_customer_ids": ["5292473333"]
  },
  "recent_successful_queries": [
    "SELECT customer_client.id FROM customer_client WHERE customer_client.descriptive_name LIKE '%Harvest%'"
  ]
}
```

The AI immediately knows:
- ✅ What queries worked recently for this customer
- ✅ Proven field names and syntax patterns  
- ✅ Common mistakes to avoid
- ✅ Working customer IDs to reference

**Result: AI makes better decisions on retry attempts!**