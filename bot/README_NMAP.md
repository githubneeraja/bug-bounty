# Nmap Scanner Module

A comprehensive Python module for performing port scans and SSL/TLS analysis via Docker. Integrates seamlessly with Amass and Shodan for complete reconnaissance automation.

## 🚀 Quick Start (5 minutes)

### 1. Install Docker
```bash
# Windows/macOS: Download Docker Desktop from https://docker.com
# Linux: sudo apt-get install docker.io
```

### 2. Pull Nmap Image
```bash
docker pull nmap/nmap:latest
```

### 3. Use
```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.port_scan('example.com', ports='1-1000')
print(f"Open Ports: {results['open_ports']}")
```

## 📦 What's Included

### Core Module
- **`nmap_scanner.py`** - Main Nmap scanning module (300 lines)
  - `NmapScanner` class - Main scanner
  - `port_scan()` - Port enumeration
  - `ssl_tls_scan()` - SSL/TLS analysis
  - `full_scan()` - Combined scan
  - `scan_target()` - Convenience function

### Examples & Tests
- **`nmap_examples.py`** - 9 usage examples (300 lines)
- **`test_nmap_scanner.py`** - Unit tests (300 lines)

### Documentation
- **`NMAP_QUICK_REFERENCE.md`** - Quick reference (5 min read)
- **`NMAP_SETUP_GUIDE.md`** - Setup & configuration (15 min read)
- **`NMAP_INTEGRATION_GUIDE.md`** - 10 integration patterns (25 min read)

## 🎯 Main Functions

### Port Scan
```python
def port_scan(
    target: str,
    ports: str = "1-1000",
    service_detection: bool = True
) -> Dict[str, Any]
```

### SSL/TLS Scan
```python
def ssl_tls_scan(
    target: str,
    port: int = 443
) -> Dict[str, Any]
```

### Full Scan
```python
def full_scan(
    target: str,
    ports: str = "1-1000",
    ssl_port: int = 443
) -> Dict[str, Any]
```

## 📊 Output Example

```python
{
    'target': 'example.com',
    'timestamp': '2025-10-26T10:00:00',
    'open_ports': [80, 443],
    'closed_ports': [22],
    'filtered_ports': [],
    'services': {
        80: 'http',
        443: 'https'
    }
}
```

## 💻 Usage Examples

### Basic Port Scan
```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.port_scan('example.com')
print(f"Open Ports: {results['open_ports']}")
```

### SSL/TLS Analysis
```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.ssl_tls_scan('example.com', port=443)
print(f"SSL/TLS Enabled: {results['ssl_enabled']}")
print(f"Protocols: {results['protocols']}")
```

### Full Scan with Output
```python
from nmap_scanner import scan_target

results = scan_target(
    'example.com',
    ports='1-1000',
    ssl_port=443,
    output_file='nmap_results.txt'
)
```

### Multiple Targets
```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
targets = ['example.com', 'google.com', 'github.com']

for target in targets:
    results = scanner.port_scan(target, ports='80,443')
    print(f"{target}: {results['open_ports']}")
```

### Export to JSON
```python
import json
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.full_scan('example.com')

with open('results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)
```

### Amass + Shodan + Nmap Pipeline
```python
from amass_subdomain_enum import enumerate_subdomains
from shodan_scanner import scan_with_shodan
from nmap_scanner import NmapScanner

# Enumerate subdomains
subs = enumerate_subdomains('example.com')

# Scan with Shodan
shodan_results = scan_with_shodan(subs[:5])

# Port scan with Nmap
scanner = NmapScanner()
for sub in subs[:5]:
    nmap_results = scanner.port_scan(sub, ports='80,443')
```

## 🧪 Testing

### Run Tests
```bash
python test_nmap_scanner.py
```

### Run Examples
```bash
python nmap_examples.py
```

### Command Line
```bash
# Basic scan
python nmap_scanner.py example.com

# Save to file
python nmap_scanner.py example.com results.txt
```

## 🔧 Configuration

### Docker Image
```python
scanner = NmapScanner(docker_image='nmap/nmap:7.92')
```

### Port Ranges
```python
# Specific ports
ports='80,443,8080'

# Range
ports='1-1000'

# All ports
ports='1-65535'
```

## 📚 Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| `NMAP_QUICK_REFERENCE.md` | Quick reference card | 5 min |
| `NMAP_SETUP_GUIDE.md` | Installation & setup | 15 min |
| `NMAP_INTEGRATION_GUIDE.md` | Integration patterns | 25 min |

## 🎓 Learning Path

1. **Start Here** - Read `NMAP_QUICK_REFERENCE.md` (5 min)
2. **Setup** - Follow `NMAP_SETUP_GUIDE.md` (15 min)
3. **Learn API** - Review `nmap_scanner.py` (15 min)
4. **Try Examples** - Run `nmap_examples.py` (20 min)
5. **Integrate** - Follow `NMAP_INTEGRATION_GUIDE.md` (30 min)

## 🔐 Security

- ✅ Docker isolation
- ✅ Input validation
- ✅ Error handling
- ✅ Logging for audit
- ✅ Timeout management
- ✅ Only scan authorized targets

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Docker not installed" | Install Docker Desktop |
| "Docker daemon not running" | Start Docker |
| "Nmap image not found" | `docker pull nmap/nmap:latest` |
| "Permission denied" | `sudo usermod -aG docker $USER` |
| "Scan timeout" | Reduce port range |

## 📞 Support

- **Quick Help:** `NMAP_QUICK_REFERENCE.md`
- **Setup Help:** `NMAP_SETUP_GUIDE.md`
- **Integration:** `NMAP_INTEGRATION_GUIDE.md`
- **Examples:** `nmap_examples.py`
- **Tests:** `test_nmap_scanner.py`

## ✨ Features

- ✅ Port scanning (1-1000 ports)
- ✅ Service version detection
- ✅ SSL/TLS certificate analysis
- ✅ Cipher suite enumeration
- ✅ Docker integration
- ✅ Multiple output formats
- ✅ Error handling
- ✅ Well-tested
- ✅ Production-ready
- ✅ Extensively documented

## 📋 Requirements

- Python 3.11+
- Docker
- Internet connection

## 🚀 Next Steps

1. Install Docker from https://docker.com
2. Pull Nmap image: `docker pull nmap/nmap:latest`
3. Run `python nmap_scanner.py example.com`
4. Review examples in `nmap_examples.py`
5. Integrate with Amass and Shodan
6. Deploy to production

## 📝 Version Info

- **Version:** 1.0
- **Date:** October 26, 2025
- **Python:** 3.11+
- **Status:** Production-Ready

---

**Ready for production deployment and integration with Amass and Shodan**

