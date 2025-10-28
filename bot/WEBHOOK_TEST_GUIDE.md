# 🧪 Make.com Webhook Test Guide

## Quick Start

### Step 1: Get Your Make.com Webhook URL

1. Go to [Make.com](https://make.com)
2. Create a new scenario or open existing one
3. Add **Custom Webhook** as trigger
4. Copy the webhook URL (looks like: `https://hook.make.com/abc123xyz`)

### Step 2: Configure .env File

```bash
# Copy the template
cp .env.example .env

# Edit .env and add your webhook URL
MAKE_WEBHOOK_URL=https://hook.make.com/your_webhook_id
```

### Step 3: Run Webhook Test

```bash
# Activate virtual environment
source recon_bot_env/bin/activate  # Linux/macOS
# or
recon_bot_env\Scripts\activate  # Windows

# Run the test
python test_webhook.py
```

## Test Scenarios

### Test 1: Environment Configuration Check
- Verifies .env file is configured
- Checks all required API keys
- Validates webhook URL format

### Test 2: Basic Webhook Connection
- Sends simple test payload
- Verifies webhook receives data
- Checks HTTP response status

### Test 3: Webhook with Recon Files
- Sends realistic recon data
- Tests file parsing
- Verifies Google Doc creation

### Test 4: Error Handling
- Tests empty files
- Tests missing domain
- Tests invalid JSON

### Test 5: Performance
- Measures response time
- Checks webhook latency
- Validates async processing

## Expected Results

### ✅ Success Indicators

```
✅ HTTP Status: 200 or 202
✅ Webhook received successfully!
✅ Response time: < 5 seconds
✅ Google Doc created: [URL]
```

### ❌ Common Issues

| Issue | Solution |
|-------|----------|
| MAKE_WEBHOOK_URL not configured | Add webhook URL to .env |
| Connection error | Check webhook URL is correct |
| Timeout | Webhook may be processing async |
| 404 error | Webhook URL may be invalid |
| 500 error | Make.com scenario may have error |

## Webhook Payload Format

### Basic Payload
```json
{
  "target_domain": "example.com",
  "test": true,
  "timestamp": "2025-10-26T10:00:00"
}
```

### Full Payload with Files
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
  ],
  "timestamp": "2025-10-26T10:00:00"
}
```

## Manual Webhook Test

### Using curl

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

### Using Python

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

webhook_url = os.getenv('MAKE_WEBHOOK_URL')

payload = {
    'target_domain': 'example.com',
    'files': [
        {'name': 'results.txt', 'content': 'test data'}
    ]
}

response = requests.post(webhook_url, json=payload)
print(response.status_code)
print(response.json())
```

## Make.com Scenario Setup

### Minimal Scenario

1. **Trigger:** Custom Webhook
   - Accept POST requests
   - Parse JSON payload

2. **Module 1:** HTTP Request (Gemini API)
   - Call Gemini API
   - Send recon content
   - Get analysis

3. **Module 2:** Google Docs
   - Create new document
   - Add analysis content
   - Save to Drive

4. **Output:** Return document URL

### Advanced Scenario

Add these modules:

1. **Router** - Error handling
2. **Email** - Send notifications
3. **Google Drive** - Organize files
4. **Slack** - Send alerts

## Troubleshooting

### Webhook Not Receiving Data

**Check:**
1. Webhook URL is correct
2. Make.com scenario is active
3. Firewall allows outbound HTTPS
4. JSON payload is valid

**Test:**
```bash
curl -X POST https://hook.make.com/your_id \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Webhook Receiving but Not Processing

**Check:**
1. Make.com scenario has no errors
2. Gemini API key is valid
3. Google Docs API is enabled
4. OAuth credentials are valid

**Debug:**
1. Check Make.com execution history
2. Review error logs
3. Verify API quotas

### Slow Response Time

**Optimize:**
1. Reduce file size
2. Simplify Gemini prompt
3. Use async processing
4. Implement caching

## Performance Benchmarks

| Operation | Time |
|-----------|------|
| Webhook receive | < 1s |
| Gemini analysis | 10-20s |
| Google Docs create | 5s |
| Total | 15-26s |

## Security Checklist

- ✅ .env file not committed
- ✅ API keys rotated regularly
- ✅ HTTPS only (no HTTP)
- ✅ Webhook URL kept secret
- ✅ Input validation enabled
- ✅ Error messages don't expose secrets
- ✅ Logging enabled for audit
- ✅ Rate limiting configured

## Next Steps

1. **Configure .env** - Add your webhook URL
2. **Run test_webhook.py** - Verify connection
3. **Check Make.com** - Review execution history
4. **Verify Google Doc** - Check created document
5. **Run full pipeline** - Execute recon_automation_bot.py

## Support

- **Setup help:** MAKE_SETUP_GUIDE.md
- **Integration:** MAKE_INTEGRATION_GUIDE.md
- **Examples:** make_examples.py
- **Full guide:** 00_MAKE_START_HERE.md

---

**Ready to test?** Run: `python test_webhook.py`

