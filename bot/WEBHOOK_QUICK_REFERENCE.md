# ⚡ Webhook Testing - Quick Reference

## 🚀 Quick Start (5 minutes)

```bash
# 1. Setup environment
python setup_env.py

# 2. Test webhook
python test_webhook.py

# 3. Check results
# - Look for ✅ PASS messages
# - Verify Google Doc was created
```

## 📋 Webhook URL

Get from Make.com:
1. Create scenario
2. Add Custom Webhook trigger
3. Copy URL: `https://hook.make.com/your_id`

## 🔧 Configuration

### Quick Setup
```bash
python setup_env.py
```

### Manual Setup
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Required Keys
```
MAKE_WEBHOOK_URL=https://hook.make.com/...
GEMINI_API_KEY=your_key
GOOGLE_API_KEY=your_key
SHODAN_API_KEY=your_key
```

## 🧪 Test Commands

### Run Full Test Suite
```bash
python test_webhook.py
```

### Test with curl
```bash
# Basic test
curl -X POST https://hook.make.com/your_id \
  -H "Content-Type: application/json" \
  -d '{"target_domain": "example.com", "test": true}'

# With files
curl -X POST https://hook.make.com/your_id \
  -H "Content-Type: application/json" \
  -d '{
    "target_domain": "example.com",
    "files": [
      {"name": "results.txt", "content": "data..."}
    ]
  }'
```

### Test with Python
```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()
webhook_url = os.getenv('MAKE_WEBHOOK_URL')

payload = {
    'target_domain': 'example.com',
    'files': [{'name': 'test.txt', 'content': 'test'}]
}

response = requests.post(webhook_url, json=payload)
print(response.status_code)
print(response.json())
```

## ✅ Success Indicators

```
✅ HTTP Status: 200 or 202
✅ Webhook received successfully!
✅ Response time: < 5 seconds
✅ Google Doc created: [URL]
```

## ❌ Common Issues

| Issue | Fix |
|-------|-----|
| MAKE_WEBHOOK_URL not set | Run `python setup_env.py` |
| Connection error | Check webhook URL is correct |
| 404 error | Verify webhook URL in Make.com |
| 500 error | Check Make.com scenario for errors |
| Timeout | Webhook may be processing async |

## 📊 Test Scenarios

### Test 1: Environment Check
```bash
python test_webhook.py
# Verifies .env configuration
```

### Test 2: Basic Connection
```bash
python test_webhook.py
# Sends simple test payload
```

### Test 3: With Files
```bash
python test_webhook.py
# Sends realistic recon data
```

### Test 4: Error Handling
```bash
python test_webhook.py
# Tests edge cases
```

### Test 5: Performance
```bash
python test_webhook.py
# Measures response time
```

## 🔍 Verify Results

### In Make.com
1. Go to scenario
2. Click **Execution history**
3. Check recent executions
4. Review logs for errors

### In Google Drive
1. Go to [Google Drive](https://drive.google.com)
2. Look for: `Recon Report - example.com - ...`
3. Open and verify content

## 📝 Webhook Payload Format

### Basic
```json
{
  "target_domain": "example.com",
  "test": true,
  "timestamp": "2025-10-26T10:00:00"
}
```

### With Files
```json
{
  "target_domain": "example.com",
  "files": [
    {
      "name": "amass_results.txt",
      "content": "subdomains..."
    },
    {
      "name": "shodan_results.json",
      "content": "{...}"
    },
    {
      "name": "nmap_results.txt",
      "content": "ports..."
    }
  ]
}
```

## 🎯 Full Pipeline Test

```bash
# Run complete automation
python recon_automation_bot.py example.com --output results.json

# Expected output:
# ✅ Found 15 subdomains
# ✅ Found 45 services
# ✅ Found 8 open ports
# ✅ Google Doc created: [URL]
```

## 🔐 Security

- ✅ Keep .env file secret
- ✅ Don't commit .env to git
- ✅ Use HTTPS only
- ✅ Rotate API keys regularly
- ✅ Monitor API usage

## 📚 Documentation

| File | Purpose |
|------|---------|
| WEBHOOK_TESTING_INSTRUCTIONS.md | Full guide |
| WEBHOOK_TEST_GUIDE.md | Setup guide |
| MAKE_SETUP_GUIDE.md | Make.com setup |
| MAKE_INTEGRATION_GUIDE.md | Integration patterns |

## ⏱️ Performance

| Operation | Time |
|-----------|------|
| Webhook receive | < 1s |
| Gemini analysis | 10-20s |
| Google Docs | 5s |
| **Total** | **15-26s** |

## 🚀 Next Steps

1. Run `python setup_env.py`
2. Run `python test_webhook.py`
3. Check Make.com execution history
4. Verify Google Doc created
5. Run `python recon_automation_bot.py example.com`

## 💡 Tips

- **Slow response?** Check Make.com logs
- **No Google Doc?** Verify Google APIs enabled
- **Connection error?** Test with curl first
- **Need help?** Check WEBHOOK_TESTING_INSTRUCTIONS.md

## 🆘 Troubleshooting

### Webhook not receiving
```bash
# Test with curl
curl -X POST https://hook.make.com/your_id \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Check Make.com logs
1. Go to Make.com scenario
2. Click **Logs**
3. Review error messages

### Verify API keys
```bash
# Check .env file
cat .env | grep -E "MAKE_|GEMINI_|GOOGLE_|SHODAN_"
```

---

**Ready?** Run: `python test_webhook.py`

