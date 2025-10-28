# 🚀 Make.com Webhook Testing Instructions

## Overview

This guide walks you through testing the Make.com webhook connection to verify your recon automation bot is properly integrated.

## Prerequisites

- ✅ Python 3.12+ installed
- ✅ Virtual environment created
- ✅ Make.com account
- ✅ Google Cloud APIs configured
- ✅ Shodan API key

## Step 1: Get Your Make.com Webhook URL

### 1.1 Create Make.com Scenario

1. Go to [Make.com](https://make.com)
2. Click **Create a new scenario**
3. Search for **Custom Webhook**
4. Click to add as trigger

### 1.2 Copy Webhook URL

1. In the Custom Webhook module, click **Save**
2. Copy the webhook URL (looks like: `https://hook.make.com/abc123xyz`)
3. Keep this URL safe - you'll need it

### 1.3 Add Modules to Scenario

Add these modules to your Make.com scenario:

**Module 1: HTTP Request (Gemini API)**
- URL: `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent`
- Method: POST
- Headers: `Content-Type: application/json`
- Body: Gemini API request

**Module 2: Google Docs**
- Action: Create a document
- Title: `Recon Report - {{domain}} - {{timestamp}}`
- Content: HTML from Gemini response

**Module 3: Router (Optional)**
- For error handling

## Step 2: Configure Environment

### 2.1 Interactive Setup (Recommended)

```bash
# Activate virtual environment
cd C:\Users\Neeraja\Desktop\recon_bot_env
Scripts\activate

# Run interactive setup
cd C:\Users\Neeraja\Documents\augment-projects\bot
python setup_env.py
```

This will guide you through:
- ✅ Make.com webhook URL
- ✅ Google API keys
- ✅ Shodan API key
- ✅ Optional Censys configuration

### 2.2 Manual Setup

```bash
# Copy template
cp .env.example .env

# Edit .env with your editor
# Add your API keys and webhook URL
```

### 2.3 Verify Configuration

```bash
# Check .env file exists
ls -la .env

# Verify it's readable
cat .env | head -5
```

## Step 3: Run Webhook Test

### 3.1 Basic Test

```bash
# Activate virtual environment
cd C:\Users\Neeraja\Desktop\recon_bot_env
Scripts\activate

# Navigate to project
cd C:\Users\Neeraja\Documents\augment-projects\bot

# Run test
python test_webhook.py
```

### 3.2 Expected Output

```
======================================================================
  MAKE.COM WEBHOOK TEST SUITE
======================================================================

======================================================================
  Step 1: Environment Configuration Check
======================================================================
✅ MAKE_WEBHOOK_URL configured: https://hook.make.com/...
✅ GEMINI_API_KEY configured: AIza...
✅ GOOGLE_API_KEY configured: AIza...
✅ SHODAN_API_KEY configured: abc...

======================================================================
  Step 2: Basic Webhook Connection Test
======================================================================
ℹ️  Sending test payload to: https://hook.make.com/...
✅ HTTP Status: 200
✅ Webhook received successfully!
✅ Response: {...}

======================================================================
  Step 3: Webhook Test with Recon Files
======================================================================
ℹ️  Sending recon files to: https://hook.make.com/...
ℹ️  Files: 3 files
✅ HTTP Status: 200
✅ Webhook received files successfully!
✅ Google Doc created: https://docs.google.com/document/d/...

======================================================================
  TEST SUMMARY
======================================================================
✅ PASS: Environment Check
✅ PASS: Basic Webhook
✅ PASS: Webhook with Files
✅ PASS: Error Handling
✅ PASS: Performance
ℹ️  Passed: 5/5
✅ All tests passed!
```

## Step 4: Verify in Make.com

### 4.1 Check Execution History

1. Go to your Make.com scenario
2. Click **Execution history**
3. You should see recent executions
4. Click on an execution to see details

### 4.2 Check Google Doc

1. Go to [Google Drive](https://drive.google.com)
2. Look for document titled: `Recon Report - example.com - ...`
3. Open and verify content

### 4.3 Check Logs

1. In Make.com, click **Logs**
2. Review any errors or warnings
3. Check API response data

## Step 5: Manual Webhook Test

### 5.1 Using curl

```bash
# Basic test
curl -X POST https://hook.make.com/your_webhook_id \
  -H "Content-Type: application/json" \
  -d '{"target_domain": "example.com", "test": true}'

# With files
curl -X POST https://hook.make.com/your_webhook_id \
  -H "Content-Type: application/json" \
  -d '{
    "target_domain": "example.com",
    "files": [
      {
        "name": "amass_results.txt",
        "content": "example.com\nwww.example.com\napi.example.com"
      },
      {
        "name": "shodan_results.json",
        "content": "{\"example.com\": {\"ip\": \"1.2.3.4\", \"ports\": [80, 443]}}"
      },
      {
        "name": "nmap_results.txt",
        "content": "Port 80: http\nPort 443: https"
      }
    ]
  }'
```

### 5.2 Using Python

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

webhook_url = os.getenv('MAKE_WEBHOOK_URL')

# Basic test
payload = {
    'target_domain': 'example.com',
    'test': True
}

response = requests.post(webhook_url, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

## Step 6: Run Full Pipeline

### 6.1 Test Full Automation

```bash
# Run full pipeline
python recon_automation_bot.py example.com --output results.json
```

### 6.2 Expected Output

```
======================================================================
  RECON AUTOMATION BOT - FULL PIPELINE
======================================================================

Step 1: Enumerating subdomains...
✅ Found 15 subdomains

Step 2: Scanning with Shodan...
✅ Scanned 15 subdomains
✅ Found 45 services

Step 3: Scanning with Nmap...
✅ Scanned ports 1-1000
✅ Found 8 open ports

Step 4: Preparing files for Make.com...
✅ Created 3 recon files

Step 5: Sending to Make.com...
✅ Webhook received
✅ Google Doc created: https://docs.google.com/document/d/...

======================================================================
  RESULTS
======================================================================
Subdomains: 15
Services: 45
Open Ports: 8
Google Doc: https://docs.google.com/document/d/...
```

## Troubleshooting

### Issue: MAKE_WEBHOOK_URL not configured

**Solution:**
```bash
# Run setup
python setup_env.py

# Or manually edit .env
nano .env  # or use your editor
```

### Issue: Connection error

**Check:**
1. Webhook URL is correct
2. Internet connection is working
3. Firewall allows HTTPS

**Test:**
```bash
curl -I https://hook.make.com/your_id
```

### Issue: 404 error

**Check:**
1. Webhook URL is valid
2. Make.com scenario is active
3. Custom Webhook module is enabled

**Solution:**
1. Go to Make.com
2. Check scenario is active
3. Regenerate webhook URL if needed

### Issue: 500 error

**Check:**
1. Make.com scenario has errors
2. Gemini API key is valid
3. Google Docs API is enabled

**Solution:**
1. Check Make.com execution logs
2. Verify API keys in .env
3. Enable required APIs in Google Cloud

### Issue: Timeout

**Check:**
1. Webhook is processing asynchronously
2. Check Make.com execution history
3. Verify Google Doc was created

**Solution:**
1. Increase timeout in test_webhook.py
2. Check Make.com logs for processing status
3. Wait for async processing to complete

## Performance Benchmarks

| Operation | Expected Time |
|-----------|----------------|
| Webhook receive | < 1 second |
| Gemini analysis | 10-20 seconds |
| Google Docs create | 5 seconds |
| **Total** | **15-26 seconds** |

## Security Checklist

Before deploying to production:

- ✅ .env file is in .gitignore
- ✅ API keys are strong and unique
- ✅ Webhook URL is kept secret
- ✅ HTTPS is used (no HTTP)
- ✅ Input validation is enabled
- ✅ Error messages don't expose secrets
- ✅ Logging is enabled for audit
- ✅ Rate limiting is configured

## Next Steps

1. ✅ Configure .env file
2. ✅ Run test_webhook.py
3. ✅ Verify in Make.com
4. ✅ Check Google Doc
5. ✅ Run full pipeline
6. ✅ Deploy to production

## Support Resources

- **Setup Help:** MAKE_SETUP_GUIDE.md
- **Integration:** MAKE_INTEGRATION_GUIDE.md
- **Examples:** make_examples.py
- **Full Guide:** 00_MAKE_START_HERE.md

---

**Ready to test?**

```bash
# 1. Setup environment
python setup_env.py

# 2. Run webhook test
python test_webhook.py

# 3. Run full pipeline
python recon_automation_bot.py example.com
```

**Questions?** Check the troubleshooting section above.

