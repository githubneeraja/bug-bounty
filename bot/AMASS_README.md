# Amass Subdomain Enumeration Module

A comprehensive Python module for subdomain enumeration using OWASP Amass with passive reconnaissance capabilities.

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Testing](#testing)
- [Integration](#integration)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **Passive Subdomain Enumeration**: Uses only public data sources
- **Active Reconnaissance**: Optional active scanning capabilities
- **JSON Output**: Detailed metadata for each subdomain
- **CSV Export**: Easy data analysis and reporting
- **Pandas Integration**: Advanced data analysis capabilities
- **Error Handling**: Comprehensive error handling and logging
- **Make.com Compatible**: Webhook integration ready
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Installation

### Step 1: Install Amass

**Windows (Chocolatey):**
```bash
choco install amass
```

**Windows (Go):**
```bash
go install -v github.com/OWASP/Amass/v3/cmd/amass@latest
```

**macOS (Homebrew):**
```bash
brew install amass
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install amass
```

### Step 2: Verify Installation

```bash
amass -version
```

### Step 3: Python Module

The module is already included in your workspace:
- `amass_subdomain_enum.py` - Main module
- `amass_examples.py` - Usage examples
- `test_amass_enum.py` - Unit tests

## 🎯 Quick Start

### Basic Usage

```python
from amass_subdomain_enum import enumerate_subdomains

# Enumerate subdomains
subdomains = enumerate_subdomains('example.com')

# Print results
for subdomain in subdomains:
    print(subdomain)
```

### Command Line

```bash
# Activate virtual environment
C:\Users\Neeraja\Desktop\recon_bot_env\Scripts\activate

# Run enumeration
python amass_subdomain_enum.py example.com
```

## 📚 API Reference

### `enumerate_subdomains(domain: str) -> List[str]`

Main function for subdomain enumeration.

**Parameters:**
- `domain` (str): Target domain (e.g., 'example.com')

**Returns:**
- List of discovered subdomains

**Raises:**
- `ValueError`: If domain is invalid
- `RuntimeError`: If Amass execution fails

**Example:**
```python
subdomains = enumerate_subdomains('example.com')
print(f"Found {len(subdomains)} subdomains")
```

### `AmassEnumerator` Class

Advanced class for detailed enumeration control.

#### Methods

**`__init__(amass_path: str = "amass")`**
- Initialize enumerator with optional custom Amass path

**`verify_amass_installed() -> bool`**
- Verify Amass is installed and accessible

**`enumerate_subdomains(domain: str, passive_only: bool = True, timeout: int = 300) -> List[str]`**
- Enumerate subdomains with options
- Parameters:
  - `domain`: Target domain
  - `passive_only`: Use passive mode (default: True)
  - `timeout`: Command timeout in seconds (default: 300)

**`enumerate_subdomains_json(domain: str, passive_only: bool = True, timeout: int = 300) -> List[Dict]`**
- Enumerate with detailed JSON metadata
- Returns list of dictionaries with:
  - `name`: Subdomain name
  - `type`: DNS record type
  - `source`: Data source
  - `tag`: Classification tag
  - `addresses`: Resolved IP addresses

**Example:**
```python
from amass_subdomain_enum import AmassEnumerator

enumerator = AmassEnumerator()
results = enumerator.enumerate_subdomains_json('example.com')

for result in results:
    print(f"{result['name']} -> {result['addresses']}")
```

## 💡 Examples

### Example 1: Basic Enumeration

```python
from amass_subdomain_enum import enumerate_subdomains

subdomains = enumerate_subdomains('example.com')
print(f"Found {len(subdomains)} subdomains")
```

### Example 2: Save to CSV

```python
from amass_subdomain_enum import AmassEnumerator
import csv

enumerator = AmassEnumerator()
results = enumerator.enumerate_subdomains_json('example.com')

with open('subdomains.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'source', 'type'])
    writer.writeheader()
    for result in results:
        writer.writerow(result)
```

### Example 3: Pandas Analysis

```python
from amass_subdomain_enum import AmassEnumerator
import pandas as pd

enumerator = AmassEnumerator()
results = enumerator.enumerate_subdomains_json('example.com')

df = pd.DataFrame(results)
print(df['source'].value_counts())
```

### Example 4: Webhook Integration

```python
from amass_subdomain_enum import enumerate_subdomains
import requests
from datetime import datetime

subdomains = enumerate_subdomains('example.com')

payload = {
    "domain": "example.com",
    "timestamp": datetime.now().isoformat(),
    "total": len(subdomains),
    "subdomains": subdomains
}

requests.post('https://hook.make.com/your_webhook', json=payload)
```

### Example 5: Multiple Domains

```python
from amass_subdomain_enum import enumerate_subdomains

domains = ['example.com', 'google.com', 'github.com']

for domain in domains:
    try:
        subdomains = enumerate_subdomains(domain)
        print(f"{domain}: {len(subdomains)} subdomains")
    except Exception as e:
        print(f"{domain}: Error - {e}")
```

## 🧪 Testing

### Run Unit Tests

```bash
# Activate virtual environment
C:\Users\Neeraja\Desktop\recon_bot_env\Scripts\activate

# Run tests
python test_amass_enum.py
```

### Run Examples

```bash
# Activate virtual environment
C:\Users\Neeraja\Desktop\recon_bot_env\Scripts\activate

# Run all examples
python amass_examples.py
```

## 🔗 Integration

### Make.com Webhook

```python
import os
from dotenv import load_dotenv
from amass_subdomain_enum import enumerate_subdomains
import requests

load_dotenv()

def send_to_make(domain):
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    subdomains = enumerate_subdomains(domain)
    
    requests.post(webhook_url, json={
        "domain": domain,
        "subdomains": subdomains,
        "count": len(subdomains)
    })

send_to_make('example.com')
```

### Shodan/Censys Integration

Configure API keys in `.env`:
```
SHODAN_API_KEY=your_key
CENSYS_API_ID=your_id
CENSYS_API_SECRET=your_secret
```

## 🔧 Troubleshooting

### Issue: "amass: command not found"

**Solution:**
1. Verify installation: `amass -version`
2. Add to PATH if needed
3. Use full path: `AmassEnumerator("/path/to/amass")`

### Issue: No subdomains found

**Solution:**
1. Try active mode: `passive_only=False`
2. Verify domain spelling
3. Check internet connection
4. Configure API keys for more sources

### Issue: Timeout errors

**Solution:**
1. Increase timeout: `timeout=600`
2. Use passive mode only
3. Check network connectivity

### Issue: Permission denied

**Solution:**
1. Make executable: `chmod +x amass`
2. Run with appropriate permissions

## 📊 Output Formats

### Text Output
```
api.example.com
blog.example.com
www.example.com
```

### JSON Output
```json
{
  "name": "api.example.com",
  "type": "CNAME",
  "source": "Shodan",
  "tag": "cert",
  "addresses": ["192.0.2.1"]
}
```

### CSV Output
```
Subdomain,Source,Type,Tag,IP Addresses
api.example.com,Shodan,CNAME,cert,192.0.2.1
blog.example.com,Censys,A,cert,192.0.2.2
```

## 📝 Logging

The module includes comprehensive logging:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

from amass_subdomain_enum import enumerate_subdomains
subdomains = enumerate_subdomains('example.com')
```

## ⚠️ Security Considerations

- Only enumerate domains you own or have permission to test
- Use passive mode to avoid detection
- Respect rate limiting
- Log all activities for compliance
- Configure API keys securely

## 📚 Resources

- **Amass GitHub**: https://github.com/OWASP/Amass
- **OWASP Project**: https://owasp.org/www-project-amass/
- **Documentation**: https://github.com/OWASP/Amass/blob/master/README.md

## 📄 License

This module is provided as-is for educational and authorized security testing purposes.

---

**Version:** 1.0  
**Last Updated:** October 26, 2025  
**Python:** 3.11+  
**Dependencies:** subprocess (built-in), json (built-in), logging (built-in)

