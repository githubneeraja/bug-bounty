# Make.com Integration Guide

## Overview

This guide explains how to integrate the recon automation bot with Make.com to create an automated pipeline that:
1. Accepts recon results via webhook
2. Processes with Google Gemini AI
3. Creates formatted Google Docs reports

## Architecture

```
Recon Bot (Python)
    ↓
Amass (Subdomains)
    ↓
Shodan (Services)
    ↓
Nmap (Ports/SSL)
    ↓
Make.com Webhook
    ↓
Gemini AI (Analysis)
    ↓
Google Docs (Report)
```

## Make.com Scenario Setup

### Scenario 1: Basic Webhook Processing

**Modules:**
1. Custom Webhook (Trigger)
2. HTTP Request (Gemini API)
3. Text Parser (Markdown to HTML)
4. Google Docs (Create Document)

**Flow:**
```
Webhook Input
    ↓
Parse Files
    ↓
Call Gemini API
    ↓
Convert to HTML
    ↓
Create Google Doc
    ↓
Return Document URL
```

### Scenario 2: Advanced with Error Handling

**Additional Modules:**
- Router (Error handling)
- Email (Notifications)
- Google Drive (File organization)

## Webhook Configuration

### Webhook URL Format

```
https://hook.make.com/[your-webhook-id]
```

### Expected Payload

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

## Gemini AI Integration

### API Endpoint

```
https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent
```

### Request Format

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Analyze these recon results..."
        }
      ]
    }
  ]
}
```

### Response Format

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "# Analysis Results\n\n## Critical Findings..."
          }
        ]
      }
    }
  ]
}
```

## Google Docs Integration

### Create Document Module

**Configuration:**
- **Drive:** Select target Google Drive
- **Title:** `Recon Report - {{domain}} - {{timestamp}}`
- **Content:** HTML formatted analysis

### Document Structure

```
Title: Recon Report - example.com - 2025-10-26 10:00:00

1. Executive Summary
2. Critical Findings
3. Services & Ports
4. Certificate Analysis
5. Recommendations
6. Appendix
```

## Python Integration

### Send Results to Make.com

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_to_make(domain, files):
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    
    payload = {
        'target_domain': domain,
        'files': files
    }
    
    response = requests.post(webhook_url, json=payload)
    return response.json()

# Usage
files = [
    {'name': 'amass_results.txt', 'content': 'subdomains...'},
    {'name': 'shodan_results.json', 'content': '{}'},
    {'name': 'nmap_results.txt', 'content': 'ports...'}
]

result = send_to_make('example.com', files)
print(result)
```

### Full Pipeline Integration

```python
from recon_automation_bot import ReconAutomationBot

bot = ReconAutomationBot()
results = bot.run_full_pipeline('example.com')

# Results include:
# - Subdomains found
# - Shodan scan results
# - Nmap scan results
# - Make.com document URL
```

## Environment Configuration

### .env File

```bash
# Make.com
MAKE_WEBHOOK_URL=https://hook.make.com/your_webhook_id

# Google APIs
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CREDENTIALS_FILE=google_credentials.json

# Recon Tools
SHODAN_API_KEY=your_shodan_api_key
CENSYS_API_ID=your_censys_id
CENSYS_API_SECRET=your_censys_secret
```

## Testing

### Test Webhook

```bash
curl -X POST https://hook.make.com/your_webhook_id \
  -H "Content-Type: application/json" \
  -d '{
    "target_domain": "example.com",
    "files": [
      {
        "name": "test.txt",
        "content": "test content"
      }
    ]
  }'
```

### Test Python Integration

```bash
python recon_automation_bot.py example.com --output results.json
```

### Verify Google Doc

1. Check Make.com execution history
2. Verify document was created in Google Drive
3. Review document content and formatting

## Troubleshooting

### Webhook Not Receiving Data

**Check:**
1. Webhook URL is correct
2. JSON payload format is valid
3. Make.com scenario is active
4. Network connectivity

**Solution:**
```bash
# Test webhook with curl
curl -X POST https://hook.make.com/your_id \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Gemini API Errors

**Common Issues:**
- Invalid API key
- API not enabled
- Quota exceeded
- Invalid request format

**Solution:**
1. Verify API key in Google Cloud Console
2. Check API is enabled
3. Review API quotas
4. Validate request format

### Google Docs Not Created

**Check:**
1. Google Docs API is enabled
2. OAuth credentials are valid
3. Drive has write permissions
4. Document title is valid

**Solution:**
1. Re-authenticate with Google
2. Check Drive permissions
3. Verify API credentials

## Performance Optimization

### Batch Processing

```python
# Process multiple domains
domains = ['example.com', 'test.com', 'sample.com']

for domain in domains:
    bot = ReconAutomationBot()
    results = bot.run_full_pipeline(domain)
```

### Rate Limiting

```python
import time

for domain in domains:
    bot = ReconAutomationBot()
    results = bot.run_full_pipeline(domain)
    time.sleep(60)  # Wait 60 seconds between scans
```

### Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor

def scan_domain(domain):
    bot = ReconAutomationBot()
    return bot.run_full_pipeline(domain)

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(scan_domain, domains))
```

## Security Best Practices

✅ **API Keys**
- Store in `.env` file
- Never commit to version control
- Rotate regularly
- Use environment variables

✅ **Webhook Security**
- Use HTTPS only
- Validate request signatures
- Implement rate limiting
- Add authentication tokens

✅ **Data Handling**
- Encrypt sensitive data
- Log all activities
- Implement access controls
- Archive results securely

## Advanced Features

### Custom Gemini Prompts

```python
custom_prompt = """
Analyze these recon results and provide:
1. Top 5 security risks
2. Recommended fixes
3. Compliance issues
4. Next steps
"""
```

### Multiple Document Formats

- Google Docs (formatted)
- PDF export
- Email summary
- Slack notification

### Scheduled Scans

```python
import schedule

def scheduled_scan():
    bot = ReconAutomationBot()
    bot.run_full_pipeline('example.com')

schedule.every().day.at("02:00").do(scheduled_scan)
```

## Monitoring & Logging

### Enable Detailed Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('recon_bot.log'),
        logging.StreamHandler()
    ]
)
```

### Monitor Make.com Execution

1. Go to Make.com scenario
2. Click "Execution history"
3. Review logs for each execution
4. Check for errors or warnings

## Next Steps

1. Set up Google Cloud APIs
2. Create Make.com scenario
3. Configure webhook
4. Test with sample data
5. Deploy to production
6. Monitor and optimize

---

**Last Updated:** October 26, 2025

