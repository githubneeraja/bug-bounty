# Amass Quick Reference Card

## 🚀 Quick Start (30 seconds)

```bash
# 1. Install Amass
choco install amass  # Windows
brew install amass   # macOS
apt-get install amass # Linux

# 2. Verify
amass -version

# 3. Test Python module
python amass_subdomain_enum.py example.com
```

## 📝 Basic Usage

### Simple Function
```python
from amass_subdomain_enum import enumerate_subdomains

subdomains = enumerate_subdomains('example.com')
for sub in subdomains:
    print(sub)
```

### With Details
```python
from amass_subdomain_enum import AmassEnumerator

enumerator = AmassEnumerator()
results = enumerator.enumerate_subdomains_json('example.com')

for r in results:
    print(f"{r['name']} ({r['source']})")
```

## 🎯 Common Tasks

### Task 1: Get Subdomains
```python
subdomains = enumerate_subdomains('example.com')
print(f"Found {len(subdomains)} subdomains")
```

### Task 2: Export to CSV
```python
import csv
from amass_subdomain_enum import AmassEnumerator

results = AmassEnumerator().enumerate_subdomains_json('example.com')
with open('out.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, ['name', 'source', 'type'])
    w.writeheader()
    w.writerows(results)
```

### Task 3: Export to JSON
```python
import json
from amass_subdomain_enum import AmassEnumerator

results = AmassEnumerator().enumerate_subdomains_json('example.com')
with open('out.json', 'w') as f:
    json.dump(results, f, indent=2)
```

### Task 4: Pandas Analysis
```python
import pandas as pd
from amass_subdomain_enum import AmassEnumerator

results = AmassEnumerator().enumerate_subdomains_json('example.com')
df = pd.DataFrame(results)
print(df['source'].value_counts())
```

### Task 5: Send to Make.com
```python
import requests
from amass_subdomain_enum import enumerate_subdomains

subs = enumerate_subdomains('example.com')
requests.post('https://hook.make.com/path', json={
    'domain': 'example.com',
    'subdomains': subs,
    'count': len(subs)
})
```

### Task 6: Multiple Domains
```python
from amass_subdomain_enum import enumerate_subdomains

for domain in ['example.com', 'google.com']:
    try:
        subs = enumerate_subdomains(domain)
        print(f"{domain}: {len(subs)}")
    except Exception as e:
        print(f"{domain}: Error - {e}")
```

### Task 7: Error Handling
```python
from amass_subdomain_enum import enumerate_subdomains

try:
    subs = enumerate_subdomains('example.com')
except ValueError as e:
    print(f"Invalid domain: {e}")
except RuntimeError as e:
    print(f"Amass error: {e}")
```

### Task 8: Custom Timeout
```python
from amass_subdomain_enum import AmassEnumerator

enumerator = AmassEnumerator()
subs = enumerator.enumerate_subdomains(
    'example.com',
    timeout=600  # 10 minutes
)
```

## 🔧 Command Line

```bash
# Basic enumeration
python amass_subdomain_enum.py example.com

# Run tests
python test_amass_enum.py

# Run examples
python amass_examples.py
```

## 📊 Output Formats

### Text (Default)
```
api.example.com
blog.example.com
www.example.com
```

### JSON
```json
{
  "name": "api.example.com",
  "source": "Shodan",
  "type": "CNAME",
  "addresses": ["192.0.2.1"]
}
```

### CSV
```
name,source,type,addresses
api.example.com,Shodan,CNAME,192.0.2.1
```

## 🎛️ Options

### Passive Mode (Default)
```python
enumerator.enumerate_subdomains(
    'example.com',
    passive_only=True  # Stealthier
)
```

### Active Mode
```python
enumerator.enumerate_subdomains(
    'example.com',
    passive_only=False  # Faster, more intrusive
)
```

### Custom Timeout
```python
enumerator.enumerate_subdomains(
    'example.com',
    timeout=300  # seconds
)
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "amass: command not found" | Install Amass: `choco install amass` |
| No subdomains found | Try active mode: `passive_only=False` |
| Timeout error | Increase timeout: `timeout=600` |
| Permission denied | Make executable: `chmod +x amass` |
| Amass not in PATH | Use full path: `AmassEnumerator("/path/to/amass")` |

## 📚 Files

| File | Purpose |
|------|---------|
| `amass_subdomain_enum.py` | Main module |
| `amass_examples.py` | 8 usage examples |
| `test_amass_enum.py` | Unit tests |
| `AMASS_README.md` | Full API reference |
| `AMASS_SETUP_GUIDE.md` | Installation guide |
| `AMASS_INTEGRATION_GUIDE.md` | Integration patterns |

## 🔗 API Summary

```python
# Main function
enumerate_subdomains(domain: str) -> List[str]

# Class
AmassEnumerator(amass_path: str = "amass")
  .verify_amass_installed() -> bool
  .enumerate_subdomains(domain, passive_only=True, timeout=300) -> List[str]
  .enumerate_subdomains_json(domain, passive_only=True, timeout=300) -> List[Dict]
```

## 💡 Pro Tips

1. **Use passive mode** for stealth
2. **Configure API keys** for more sources
3. **Set appropriate timeout** for large domains
4. **Use JSON output** for detailed analysis
5. **Batch process** multiple domains
6. **Log results** for compliance
7. **Test with examples** first
8. **Check documentation** for advanced usage

## 🔐 Security

- ✅ Only test authorized domains
- ✅ Use passive mode by default
- ✅ Store API keys in `.env`
- ✅ Log all activities
- ✅ Respect rate limits
- ✅ Follow local laws

## 📞 Quick Help

```bash
# Show version
amass -version

# Show help
amass -help

# Show enum help
amass enum -help

# Run tests
python test_amass_enum.py

# Run examples
python amass_examples.py
```

## 🎓 Learning Path

1. Read `AMASS_README.md` - Understand the API
2. Run `amass_examples.py` - See it in action
3. Try `test_amass_enum.py` - Verify installation
4. Use `enumerate_subdomains()` - Start simple
5. Use `AmassEnumerator` class - Advanced usage
6. Integrate with Make.com - Automation

---

**Quick Reference v1.0** | October 26, 2025

