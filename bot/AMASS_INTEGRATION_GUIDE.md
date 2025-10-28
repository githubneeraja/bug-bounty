# Amass Integration Guide

Complete guide for integrating Amass subdomain enumeration into your recon automation workflow.

## 📦 Files Overview

### Core Module
- **`amass_subdomain_enum.py`** - Main module with `enumerate_subdomains()` function
  - `AmassEnumerator` class for advanced usage
  - Passive and active enumeration modes
  - JSON and text output support
  - Comprehensive error handling

### Documentation
- **`AMASS_README.md`** - Complete API reference and usage guide
- **`AMASS_SETUP_GUIDE.md`** - Installation and configuration guide
- **`AMASS_INTEGRATION_GUIDE.md`** - This file

### Examples & Tests
- **`amass_examples.py`** - 8 comprehensive usage examples
- **`test_amass_enum.py`** - Unit tests and integration tests

## 🔧 Setup Steps

### Step 1: Install Amass

**Windows:**
```bash
choco install amass
```

**macOS:**
```bash
brew install amass
```

**Linux:**
```bash
sudo apt-get install amass
```

### Step 2: Verify Installation

```bash
amass -version
```

### Step 3: Activate Virtual Environment

```bash
C:\Users\Neeraja\Desktop\recon_bot_env\Scripts\activate
```

### Step 4: Test the Module

```bash
python amass_subdomain_enum.py example.com
```

## 🚀 Integration Patterns

### Pattern 1: Simple Function Call

```python
from amass_subdomain_enum import enumerate_subdomains

# Get subdomains
subdomains = enumerate_subdomains('example.com')

# Process results
for subdomain in subdomains:
    print(subdomain)
```

### Pattern 2: Class-Based with Options

```python
from amass_subdomain_enum import AmassEnumerator

enumerator = AmassEnumerator()

# Passive enumeration
subdomains = enumerator.enumerate_subdomains(
    domain='example.com',
    passive_only=True,
    timeout=300
)

# Active enumeration (if needed)
subdomains = enumerator.enumerate_subdomains(
    domain='example.com',
    passive_only=False,
    timeout=600
)
```

### Pattern 3: Detailed JSON Results

```python
from amass_subdomain_enum import AmassEnumerator

enumerator = AmassEnumerator()
results = enumerator.enumerate_subdomains_json('example.com')

for result in results:
    print(f"Domain: {result['name']}")
    print(f"Source: {result['source']}")
    print(f"IPs: {result['addresses']}")
```

### Pattern 4: Data Export

```python
from amass_subdomain_enum import AmassEnumerator
import json
import csv

enumerator = AmassEnumerator()
results = enumerator.enumerate_subdomains_json('example.com')

# Export to JSON
with open('results.json', 'w') as f:
    json.dump(results, f, indent=2)

# Export to CSV
with open('results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'source', 'type'])
    writer.writeheader()
    writer.writerows(results)
```

### Pattern 5: Pandas Analysis

```python
from amass_subdomain_enum import AmassEnumerator
import pandas as pd

enumerator = AmassEnumerator()
results = enumerator.enumerate_subdomains_json('example.com')

df = pd.DataFrame(results)

# Analysis
print(f"Total subdomains: {len(df)}")
print(f"\nBy source:")
print(df['source'].value_counts())
print(f"\nBy type:")
print(df['type'].value_counts())

# Filter subdomains with resolved IPs
with_ips = df[df['addresses'].apply(lambda x: len(x) > 0)]
print(f"\nSubdomains with IPs: {len(with_ips)}")
```

### Pattern 6: Make.com Webhook

```python
from amass_subdomain_enum import enumerate_subdomains
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def send_to_make(domain):
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    
    try:
        subdomains = enumerate_subdomains(domain)
        
        payload = {
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
            "total_subdomains": len(subdomains),
            "subdomains": subdomains,
            "status": "success"
        }
        
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 200
    
    except Exception as e:
        payload = {
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "status": "failed"
        }
        requests.post(webhook_url, json=payload)
        return False

# Usage
send_to_make('example.com')
```

### Pattern 7: Batch Processing

```python
from amass_subdomain_enum import enumerate_subdomains
import json
from datetime import datetime

domains = ['example.com', 'google.com', 'github.com']
results = {}

for domain in domains:
    try:
        print(f"Enumerating {domain}...")
        subdomains = enumerate_subdomains(domain)
        results[domain] = {
            "status": "success",
            "count": len(subdomains),
            "subdomains": subdomains
        }
    except Exception as e:
        results[domain] = {
            "status": "failed",
            "error": str(e)
        }

# Save results
with open(f'batch_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
    json.dump(results, f, indent=2)
```

### Pattern 8: Error Handling

```python
from amass_subdomain_enum import enumerate_subdomains
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_enumerate(domain):
    try:
        subdomains = enumerate_subdomains(domain)
        logger.info(f"✓ Found {len(subdomains)} subdomains for {domain}")
        return subdomains
    
    except ValueError as e:
        logger.error(f"Invalid domain: {e}")
        return []
    
    except RuntimeError as e:
        logger.error(f"Amass error: {e}")
        return []
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []

# Usage
subdomains = safe_enumerate('example.com')
```

## 🔌 Make.com Workflow

### Setup Steps

1. **Create Make.com Account**
   - Visit https://www.make.com
   - Sign up and create new scenario

2. **Create Webhook**
   - Add "Webhooks" module
   - Copy webhook URL
   - Add to `.env` file:
     ```
     MAKE_WEBHOOK_URL=https://hook.make.com/your_webhook_path
     ```

3. **Configure Payload**
   - Expected payload structure:
     ```json
     {
       "domain": "example.com",
       "timestamp": "2025-10-26T10:30:00",
       "total_subdomains": 42,
       "subdomains": ["api.example.com", "www.example.com"],
       "status": "success"
     }
     ```

4. **Create Automation**
   - Add modules for data processing
   - Store results in database
   - Send notifications
   - Generate reports

## 📊 Output Examples

### Text Output
```
api.example.com
blog.example.com
cdn.example.com
dev.example.com
mail.example.com
www.example.com
```

### JSON Output
```json
{
  "domain": "example.com",
  "timestamp": "2025-10-26T10:30:00",
  "total_subdomains": 6,
  "subdomains": [
    {
      "name": "api.example.com",
      "source": "Shodan",
      "type": "CNAME",
      "tag": "cert",
      "addresses": ["192.0.2.1"]
    }
  ]
}
```

## 🧪 Testing

### Run Unit Tests
```bash
python test_amass_enum.py
```

### Run Examples
```bash
python amass_examples.py
```

### Manual Testing
```bash
python amass_subdomain_enum.py example.com
```

## 🔐 Security Best Practices

1. **Use Passive Mode**
   - Default behavior is passive
   - No active scanning by default
   - Stealthier reconnaissance

2. **Secure API Keys**
   - Store in `.env` file
   - Never commit to version control
   - Use environment variables

3. **Rate Limiting**
   - Respect API rate limits
   - Implement delays between requests
   - Monitor usage

4. **Logging & Monitoring**
   - Log all enumeration activities
   - Monitor for errors
   - Track results

5. **Legal Compliance**
   - Only test authorized domains
   - Document authorization
   - Comply with local laws

## 🐛 Troubleshooting

### Amass Not Found
```python
# Use full path
enumerator = AmassEnumerator("/usr/local/bin/amass")
```

### Timeout Issues
```python
# Increase timeout
subdomains = enumerator.enumerate_subdomains(
    domain='example.com',
    timeout=600  # 10 minutes
)
```

### No Results
```python
# Try active mode
subdomains = enumerator.enumerate_subdomains(
    domain='example.com',
    passive_only=False
)
```

## 📚 Next Steps

1. **Install Amass** - Follow installation guide
2. **Test Module** - Run `python amass_subdomain_enum.py example.com`
3. **Review Examples** - Check `amass_examples.py`
4. **Integrate** - Add to your recon workflow
5. **Configure Make.com** - Set up webhook integration
6. **Deploy** - Use in production automation

## 📞 Support

For issues or questions:
1. Check `AMASS_README.md` for API reference
2. Review `AMASS_SETUP_GUIDE.md` for installation
3. Check `amass_examples.py` for usage patterns
4. Run `test_amass_enum.py` for diagnostics

---

**Version:** 1.0  
**Last Updated:** October 26, 2025  
**Status:** Ready for Production

