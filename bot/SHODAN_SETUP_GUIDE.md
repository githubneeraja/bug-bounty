# Shodan Scanner Setup Guide

## Overview

The Shodan Scanner module provides Python integration with the Shodan API to scan subdomains and retrieve information about services running on their resolved IP addresses.

## What is Shodan?

**Shodan** is a search engine for internet-connected devices. It scans the internet and indexes information about:
- Open ports and services
- Banners and version information
- Vulnerabilities
- Geographic location
- Organization information
- Operating systems

## Getting Started

### Step 1: Get a Shodan API Key

1. Visit https://www.shodan.io
2. Create a free account
3. Go to Account Settings
4. Copy your API key
5. Save it securely

**Free Account Limits:**
- 1 query per second
- Limited query credits
- Basic search functionality

**Paid Plans:**
- More query credits
- Higher rate limits
- Advanced features

### Step 2: Configure Environment

Create or update `.env` file:
```
SHODAN_API_KEY=your_api_key_here
```

Or set environment variable:
```bash
# Windows
set SHODAN_API_KEY=your_api_key_here

# Linux/macOS
export SHODAN_API_KEY=your_api_key_here
```

### Step 3: Verify Installation

```bash
# Activate virtual environment
C:\Users\Neeraja\Desktop\recon_bot_env\Scripts\activate

# Test the module
python shodan_scanner.py api.example.com
```

## API Reference

### Main Function

```python
def scan_with_shodan(
    subdomains: List[str],
    api_key: Optional[str] = None,
    resolve_ips: bool = True
) -> Dict[str, Any]
```

**Parameters:**
- `subdomains`: List of subdomains to scan
- `api_key`: Shodan API key (default: from SHODAN_API_KEY env var)
- `resolve_ips`: Whether to resolve subdomains to IPs (default: True)

**Returns:**
- Dictionary with scan results per subdomain

**Example:**
```python
from shodan_scanner import scan_with_shodan

subdomains = ['api.example.com', 'www.example.com']
results = scan_with_shodan(subdomains)

for subdomain, data in results['subdomains'].items():
    print(f"{subdomain}: {data['ip']}")
```

### ShodanScanner Class

```python
class ShodanScanner:
    def __init__(self, api_key: Optional[str] = None)
    def verify_api_key() -> bool
    def resolve_subdomain(subdomain: str) -> Optional[str]
    def scan_ip(ip: str) -> Dict[str, Any]
    def scan_subdomains(subdomains: List[str], resolve_ips: bool = True) -> Dict[str, Any]
```

## Output Format

### Result Structure

```python
{
    'timestamp': '2025-10-26T10:30:00',
    'total_subdomains': 2,
    'scanned_subdomains': 2,
    'subdomains': {
        'api.example.com': {
            'subdomain': 'api.example.com',
            'ip': '192.0.2.1',
            'resolved': True,
            'scan_data': {
                'ip': '192.0.2.1',
                'country': 'United States',
                'city': 'New York',
                'organization': 'Example Corp',
                'ports': [80, 443],
                'services': [
                    {
                        'port': 80,
                        'protocol': 'http',
                        'banner': 'HTTP/1.1 200 OK',
                        'product': 'Apache',
                        'version': '2.4.41'
                    }
                ],
                'vulnerabilities': []
            },
            'error': None
        }
    }
}
```

## Common Tasks

### Task 1: Scan Single Subdomain

```python
from shodan_scanner import scan_with_shodan

results = scan_with_shodan(['api.example.com'])
print(results['subdomains']['api.example.com'])
```

### Task 2: Scan Multiple Subdomains

```python
from shodan_scanner import scan_with_shodan

subdomains = ['api.example.com', 'www.example.com', 'mail.example.com']
results = scan_with_shodan(subdomains)

for subdomain, data in results['subdomains'].items():
    if data['resolved']:
        print(f"{subdomain}: {data['ip']}")
```

### Task 3: Export Results to JSON

```python
import json
from shodan_scanner import scan_with_shodan

results = scan_with_shodan(['api.example.com'])

with open('shodan_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)
```

### Task 4: Export Results to CSV

```python
import csv
from shodan_scanner import scan_with_shodan

results = scan_with_shodan(['api.example.com', 'www.example.com'])

with open('shodan_results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['Subdomain', 'IP', 'Country', 'Services'])
    writer.writeheader()
    
    for subdomain, data in results['subdomains'].items():
        if data['scan_data']:
            writer.writerow({
                'Subdomain': subdomain,
                'IP': data['ip'],
                'Country': data['scan_data'].get('country'),
                'Services': len(data['scan_data'].get('services', []))
            })
```

### Task 5: Analyze with Pandas

```python
import pandas as pd
from shodan_scanner import scan_with_shodan

results = scan_with_shodan(['api.example.com', 'www.example.com'])

data = []
for subdomain, info in results['subdomains'].items():
    if info['scan_data']:
        data.append({
            'Subdomain': subdomain,
            'IP': info['ip'],
            'Country': info['scan_data'].get('country'),
            'Services': len(info['scan_data'].get('services', []))
        })

df = pd.DataFrame(data)
print(df)
```

### Task 6: Integration with Amass

```python
from amass_subdomain_enum import enumerate_subdomains
from shodan_scanner import scan_with_shodan

# Enumerate subdomains
subdomains = enumerate_subdomains('example.com')

# Scan with Shodan
results = scan_with_shodan(subdomains[:10])  # Limit to first 10

print(f"Scanned: {results['scanned_subdomains']}/{results['total_subdomains']}")
```

## Troubleshooting

### Issue: "Shodan API key not provided"
**Solution:**
1. Set SHODAN_API_KEY environment variable
2. Or pass api_key parameter: `scan_with_shodan(subdomains, api_key='your_key')`

### Issue: "Invalid Shodan API key"
**Solution:**
1. Verify API key is correct
2. Check at https://www.shodan.io/account/profile
3. Regenerate if necessary

### Issue: "Could not resolve subdomain"
**Solution:**
1. Verify subdomain is valid
2. Check DNS resolution: `nslookup subdomain.com`
3. Try with resolve_ips=False if subdomain is already an IP

### Issue: Rate limit exceeded
**Solution:**
1. Add delays between requests
2. Upgrade to paid Shodan plan
3. Batch requests efficiently

## Best Practices

✅ **Security**
- Store API key in environment variables
- Never commit API key to version control
- Use .env file with .gitignore

✅ **Performance**
- Batch multiple subdomains in one call
- Cache results to avoid duplicate queries
- Implement rate limiting

✅ **Error Handling**
- Handle API errors gracefully
- Log all errors
- Implement retry logic

✅ **Data Management**
- Export results for analysis
- Store results in database
- Archive historical data

## API Limits

**Free Account:**
- 1 query per second
- Limited query credits
- Basic search

**Paid Plans:**
- Higher rate limits
- More query credits
- Advanced features

## Resources

- **Shodan Website:** https://www.shodan.io
- **API Documentation:** https://developer.shodan.io
- **Python Library:** https://github.com/achillean/shodan-python
- **Query Syntax:** https://www.shodan.io/search/filters

## Next Steps

1. Get Shodan API key
2. Configure environment variable
3. Test with `python shodan_scanner.py example.com`
4. Review examples in `shodan_examples.py`
5. Integrate into your workflow

---

**Last Updated:** October 26, 2025

