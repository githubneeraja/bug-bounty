# Make.com Automation Setup Guide

## Overview

This guide walks you through setting up a Make.com automation pipeline that:
1. Accepts recon result files via webhook
2. Processes them with Google Gemini AI
3. Creates formatted Google Docs reports

## Prerequisites

- Make.com account (free tier available)
- Google Cloud account with Gemini API enabled
- Google Docs API credentials
- Python 3.11+ with required libraries

## Step 1: Set Up Google Cloud APIs

### 1.1 Enable Gemini API

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable the following APIs:
   - Generative Language API (Gemini)
   - Google Docs API
   - Google Drive API

### 1.2 Create API Keys

**For Gemini API:**
1. Go to APIs & Services → Credentials
2. Click "Create Credentials" → API Key
3. Copy the API key
4. Add to `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

**For Google Docs:**
1. Create OAuth 2.0 credentials (Desktop application)
2. Download the JSON file
3. Save as `google_credentials.json`
4. Add to `.env`:
   ```
   GOOGLE_API_KEY=your_api_key_here
   GOOGLE_CREDENTIALS_FILE=google_credentials.json
   ```

## Step 2: Set Up Make.com Scenario

### 2.1 Create New Scenario

1. Log in to [Make.com](https://make.com)
2. Click "Create a new scenario"
3. Name it: `Recon Automation Pipeline`

### 2.2 Add Webhook Trigger

1. Click the plus icon to add a module
2. Search for "Webhooks"
3. Select "Custom Webhook"
4. Click "Add"
5. Copy the webhook URL (you'll need this)

### 2.3 Configure Webhook

**Webhook Settings:**
- **Name:** Recon Results Webhook
- **Data structure:** Custom
- **Expected data:**
  ```json
  {
    "target_domain": "example.com",
    "files": [
      {
        "name": "amass_results.txt",
        "content": "file content here"
      },
      {
        "name": "shodan_results.json",
        "content": "file content here"
      },
      {
        "name": "nmap_results.txt",
        "content": "file content here"
      }
    ]
  }
  ```

## Step 3: Add Gemini AI Module

### 3.1 Add HTTP Request Module

1. Click plus icon after webhook
2. Search for "HTTP"
3. Select "Make an HTTP request"
4. Configure:

**URL:**
```
https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={{GEMINI_API_KEY}}
```

**Method:** POST

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Analyze these recon results:\n\n{{webhook_data}}"
        }
      ]
    }
  ]
}
```

## Step 4: Add Markdown to HTML Conversion

### 4.1 Add Text Parser

1. Click plus icon
2. Search for "Text Parser"
3. Select "Match Pattern"
4. Configure to convert Markdown to HTML

**Alternative:** Use a dedicated Markdown module if available

## Step 5: Add Google Docs Creation

### 5.1 Add Google Docs Module

1. Click plus icon
2. Search for "Google Docs"
3. Select "Create a Document"
4. Authorize with your Google account
5. Configure:

**Document Title:**
```
Recon Report - {{target_domain}} - {{now}}
```

**Content:**
```
{{gemini_analysis_html}}
```

## Step 6: Test the Workflow

### 6.1 Send Test Webhook

```bash
curl -X POST https://your-webhook-url \
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

### 6.2 Verify Results

1. Check Make.com execution history
2. Verify Google Doc was created
3. Review Gemini analysis output

## Step 7: Integrate with Python Scripts

### 7.1 Send Results from Python

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_recon_to_make(files, target_domain):
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    
    payload = {
        'target_domain': target_domain,
        'files': files
    }
    
    response = requests.post(webhook_url, json=payload)
    return response.json()

# Usage
files = [
    {'name': 'amass_results.txt', 'content': 'subdomains...'},
    {'name': 'shodan_results.json', 'content': 'services...'},
    {'name': 'nmap_results.txt', 'content': 'ports...'}
]

result = send_recon_to_make(files, 'example.com')
print(result)
```

### 7.2 Update .env File

```bash
# Make.com
MAKE_WEBHOOK_URL=https://hook.make.com/your_webhook_id

# Google APIs
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CREDENTIALS_FILE=google_credentials.json
```

## Step 8: Automate Full Pipeline

### 8.1 Create Master Script

```python
from amass_subdomain_enum import enumerate_subdomains
from shodan_scanner import scan_with_shodan
from nmap_scanner import scan_target
from make_automation import process_recon_results
import os
from dotenv import load_dotenv

load_dotenv()

def run_full_recon(domain):
    # Step 1: Enumerate subdomains
    subdomains = enumerate_subdomains(domain)
    
    # Step 2: Scan with Shodan
    shodan_results = scan_with_shodan(subdomains[:5])
    
    # Step 3: Nmap scan
    nmap_results = scan_target(domain, output_file=f'{domain}_nmap.txt')
    
    # Step 4: Prepare files for Make.com
    files = [
        {'name': 'amass_results.txt', 'content': '\n'.join(subdomains)},
        {'name': 'shodan_results.json', 'content': str(shodan_results)},
        {'name': 'nmap_results.txt', 'content': str(nmap_results)}
    ]
    
    # Step 5: Send to Make.com
    result = process_recon_results(files, domain)
    return result

# Usage
result = run_full_recon('example.com')
print(result)
```

## Troubleshooting

### Issue: Webhook not receiving data
**Solution:**
1. Verify webhook URL is correct
2. Check Make.com execution history
3. Ensure JSON format is valid

### Issue: Gemini API errors
**Solution:**
1. Verify API key is correct
2. Check API is enabled in Google Cloud
3. Review API quotas

### Issue: Google Docs not created
**Solution:**
1. Verify Google Docs API is enabled
2. Check OAuth credentials
3. Ensure proper permissions

## Security Best Practices

✅ **API Keys**
- Store in `.env` file (never commit)
- Use environment variables
- Rotate keys regularly

✅ **Webhook Security**
- Use HTTPS only
- Implement request validation
- Add authentication tokens

✅ **Data Handling**
- Encrypt sensitive data
- Log all activities
- Implement access controls

## Next Steps

1. Set up Google Cloud APIs
2. Create Make.com scenario
3. Configure webhook
4. Test with sample data
5. Integrate with Python scripts
6. Deploy to production

## Resources

- [Make.com Documentation](https://www.make.com/en/help)
- [Google Gemini API](https://ai.google.dev/)
- [Google Docs API](https://developers.google.com/docs)
- [Webhook Testing](https://webhook.site)

---

**Last Updated:** October 26, 2025

