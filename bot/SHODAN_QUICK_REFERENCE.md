# Shodan Scanner Quick Reference

## 🚀 Quick Start (2 minutes)

### 1. Get API Key
- Visit https://www.shodan.io
- Create account
- Copy API key

### 2. Configure
```bash
# Set environment variable
set SHODAN_API_KEY=your_api_key_here  # Windows
export SHODAN_API_KEY=your_api_key_here  # Linux/macOS

# Or create .env file
echo "SHODAN_API_KEY=your_api_key_here" > .env
```

### 3. Test
```bash
python shodan_scanner.py api.example.com
```

## 📝 Basic Usage

### Simple Scan
```python
from shodan_scanner import scan_with_shodan

results = scan_with_shodan(['api.example.com'])
```

### Multiple Subdomains
```python
subdomains = ['api.example.com', 'www.example.com']
results = scan_with_shodan(subdomains)
```

### With Custom API Key
```python
results = scan_with_shodan(subdomains, api_key='your_key')
```

## 🎯 Common Tasks

### Task 1: Get IP and Services
```python
from shodan_scanner import scan_with_shodan

results = scan_with_shodan(['api.example.com'])
data = results['subdomains']['api.example.com']

print(f"IP: {data['ip']}")
print(f"Services: {len(data['scan_data']['services'])}")
```

### Task 2: Export to JSON
```python
import json
from shodan_scanner import scan_with_shodan

results = scan_with_shodan(['api.example.com'])
with open('results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)
```

### Task 3: Export to CSV
```python
import csv
from shodan_scanner import scan_with_shodan

results = scan_with_shodan(['api.example.com'])
with open('results.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, ['Subdomain', 'IP', 'Country'])
    w.writeheader()
    for sub, data in results['subdomains'].items():
        w.writerow({
            'Subdomain': sub,
            'IP': data['ip'],
            'Country': data['scan_data'].get('country') if data['scan_data'] else 'N/A'
        })
```

### Task 4: Pandas Analysis
```python
import pandas as pd
from shodan_scanner import scan_with_shodan

results = scan_with_shodan(['api.example.com', 'www.example.com'])
data = []
for sub, info in results['subdomains'].items():
    if info['scan_data']:
        data.append({
            'Subdomain': sub,
            'IP': info['ip'],
            'Services': len(info['scan_data'].get('services', []))
        })
df = pd.DataFrame(data)
print(df)
```

### Task 5: Find Vulnerabilities
```python
from shodan_scanner import scan_with_shodan

results = scan_with_shodan(['api.example.com'])
for sub, data in results['subdomains'].items():
    if data['scan_data']:
        vulns = data['scan_data'].get('vulnerabilities', [])
        if vulns:
            print(f"{sub}: {len(vulns)} vulnerabilities")
```

### Task 6: Integrate with Amass
```python
from amass_subdomain_enum import enumerate_subdomains
from shodan_scanner import scan_with_shodan

# Get subdomains
subs = enumerate_subdomains('example.com')

# Scan with Shodan
results = scan_with_shodan(subs[:5])
print(f"Scanned: {results['scanned_subdomains']}")
```

## 🔧 Command Line

```bash
# Single subdomain
python shodan_scanner.py api.example.com

# Multiple subdomains
python shodan_scanner.py api.example.com www.example.com mail.example.com

# Run tests
python test_shodan_scanner.py

# Run examples
python shodan_examples.py
```

## 📊 Output Structure

```python
{
    'timestamp': '2025-10-26T10:30:00',
    'total_subdomains': 1,
    'scanned_subdomains': 1,
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
                'services': [...],
                'vulnerabilities': [...]
            },
            'error': None
        }
    }
}
```

## 🎛️ Options

### Resolve IPs
```python
# Resolve subdomains to IPs (default: True)
results = scan_with_shodan(subdomains, resolve_ips=True)

# Assume subdomains are IPs
results = scan_with_shodan(ips, resolve_ips=False)
```

### Custom API Key
```python
results = scan_with_shodan(subdomains, api_key='your_key')
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not provided" | Set SHODAN_API_KEY env var |
| "Invalid API key" | Check key at shodan.io |
| "Could not resolve" | Verify subdomain is valid |
| "Rate limit exceeded" | Upgrade plan or add delays |

## 📚 API Reference

```python
# Main function
scan_with_shodan(subdomains, api_key=None, resolve_ips=True) -> Dict

# Class
ShodanScanner(api_key=None)
  .verify_api_key() -> bool
  .resolve_subdomain(subdomain) -> Optional[str]
  .scan_ip(ip) -> Dict
  .scan_subdomains(subdomains, resolve_ips=True) -> Dict
```

## 💡 Pro Tips

1. **Batch requests** - Scan multiple subdomains at once
2. **Cache results** - Avoid duplicate queries
3. **Handle errors** - Implement retry logic
4. **Export data** - Save results for analysis
5. **Monitor credits** - Check API usage
6. **Use filters** - Narrow down results
7. **Combine tools** - Use with Amass for full recon

## 🔐 Security

- ✅ Store API key in .env
- ✅ Never commit API key
- ✅ Use environment variables
- ✅ Rotate keys regularly
- ✅ Monitor API usage

## 📞 Quick Help

```bash
# Show version
python -c "import shodan; print(shodan.__version__)"

# Test API key
python shodan_scanner.py test.com

# Run examples
python shodan_examples.py

# Run tests
python test_shodan_scanner.py
```

## 🎓 Learning Path

1. Get API key (5 min)
2. Configure environment (2 min)
3. Run basic scan (2 min)
4. Review examples (10 min)
5. Integrate with Amass (10 min)

## 📋 Files

| File | Purpose |
|------|---------|
| `shodan_scanner.py` | Main module |
| `shodan_examples.py` | 9 usage examples |
| `test_shodan_scanner.py` | Unit tests |
| `SHODAN_SETUP_GUIDE.md` | Setup guide |
| `SHODAN_QUICK_REFERENCE.md` | This file |

## 🔗 Resources

- **Shodan:** https://www.shodan.io
- **API Docs:** https://developer.shodan.io
- **Python Lib:** https://github.com/achillean/shodan-python
- **Filters:** https://www.shodan.io/search/filters

---

**Quick Reference v1.0** | October 26, 2025

