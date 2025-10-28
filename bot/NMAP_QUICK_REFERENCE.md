# Nmap Scanner Quick Reference

## 🚀 Quick Start (5 minutes)

### 1. Install Docker
```bash
# Windows/macOS: Download Docker Desktop
# Linux: sudo apt-get install docker.io
```

### 2. Pull Nmap Image
```bash
docker pull nmap/nmap:latest
```

### 3. Test
```bash
python nmap_scanner.py example.com results.txt
```

## 📝 Basic Usage

### Simple Port Scan
```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.port_scan('example.com')
print(results['open_ports'])
```

### SSL/TLS Analysis
```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.ssl_tls_scan('example.com', port=443)
print(results['ssl_enabled'])
```

### Full Scan
```python
from nmap_scanner import scan_target

results = scan_target('example.com', output_file='results.txt')
```

## 🎯 Common Tasks

### Task 1: Scan Specific Ports
```python
scanner = NmapScanner()
results = scanner.port_scan('example.com', ports='80,443,8080')
```

### Task 2: Service Detection
```python
scanner = NmapScanner()
results = scanner.port_scan('example.com', service_detection=True)
for port, service in results['services'].items():
    print(f"Port {port}: {service}")
```

### Task 3: Export to JSON
```python
import json
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.full_scan('example.com')
with open('results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)
```

### Task 4: Multiple Targets
```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
for target in ['example.com', 'google.com']:
    results = scanner.port_scan(target, ports='80,443')
    print(f"{target}: {results['open_ports']}")
```

### Task 5: SSL Certificate Info
```python
scanner = NmapScanner()
results = scanner.ssl_tls_scan('example.com')
print(results['certificate_info'])
print(results['protocols'])
```

### Task 6: Error Handling
```python
from nmap_scanner import NmapScanner

try:
    scanner = NmapScanner()
    results = scanner.port_scan('example.com')
except RuntimeError as e:
    print(f"Error: {e}")
```

## 🔧 Command Line

```bash
# Basic scan
python nmap_scanner.py example.com

# Save to file
python nmap_scanner.py example.com results.txt

# Run tests
python test_nmap_scanner.py

# Run examples
python nmap_examples.py
```

## 📊 Output Structure

### Port Scan
```python
{
    'target': 'example.com',
    'timestamp': '2025-10-26T10:00:00',
    'open_ports': [80, 443],
    'closed_ports': [22],
    'filtered_ports': [],
    'services': {80: 'http', 443: 'https'}
}
```

### SSL/TLS Scan
```python
{
    'target': 'example.com',
    'port': 443,
    'ssl_enabled': True,
    'certificate_info': {
        'subject': 'CN=example.com',
        'issuer': 'CN=Let\'s Encrypt'
    },
    'protocols': ['TLSv1.2', 'TLSv1.3'],
    'ciphers': ['AES_256_GCM_SHA384']
}
```

## 🎛️ Options

### Port Ranges
```python
# Specific ports
ports='80,443,8080'

# Range
ports='1-1000'

# Common ports
ports='1-65535'
```

### Service Detection
```python
# Enable service detection
service_detection=True

# Disable (faster)
service_detection=False
```

### Custom Docker Image
```python
scanner = NmapScanner(docker_image='nmap/nmap:7.92')
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Docker not installed" | Install Docker Desktop |
| "Docker daemon not running" | Start Docker |
| "Nmap image not found" | `docker pull nmap/nmap:latest` |
| "Permission denied" | `sudo usermod -aG docker $USER` |
| "Scan timeout" | Reduce port range or increase timeout |

## 📚 API Reference

```python
# Main class
NmapScanner(docker_image='nmap/nmap:latest')

# Methods
.verify_docker() -> bool
.port_scan(target, ports='1-1000', service_detection=True) -> Dict
.ssl_tls_scan(target, port=443) -> Dict
.full_scan(target, ports='1-1000', ssl_port=443) -> Dict
.run_docker_nmap(args) -> Tuple[str, str, int]

# Functions
scan_target(target, ports='1-1000', ssl_port=443, output_file=None) -> Dict
save_results(results, output_file) -> None
```

## 💡 Pro Tips

1. **Batch Scans** - Scan multiple targets at once
2. **Cache Results** - Save results to avoid duplicate scans
3. **Error Handling** - Always wrap scans in try-except
4. **Logging** - Enable logging for debugging
5. **Port Selection** - Start with common ports (80, 443, 22)
6. **Service Detection** - Use only when needed (slower)
7. **Docker Caching** - Results are cached in Docker

## 🔐 Security

- ✅ Only scan targets you own
- ✅ Respect network policies
- ✅ Handle results securely
- ✅ Log all activities
- ✅ Use appropriate scan types

## 📞 Quick Help

```bash
# Show version
docker run nmap/nmap:latest --version

# Test Docker
docker run hello-world

# List images
docker images

# Remove image
docker rmi nmap/nmap:latest
```

## 🎓 Learning Path

1. Install Docker (5 min)
2. Pull Nmap image (2 min)
3. Run basic scan (5 min)
4. Review examples (10 min)
5. Integrate into workflow (15 min)

## 📋 Files

| File | Purpose |
|------|---------|
| `nmap_scanner.py` | Main module |
| `nmap_examples.py` | 9 usage examples |
| `test_nmap_scanner.py` | Unit tests |
| `NMAP_SETUP_GUIDE.md` | Setup guide |
| `NMAP_QUICK_REFERENCE.md` | This file |

## 🔗 Resources

- **Nmap:** https://nmap.org
- **Docker:** https://docker.com
- **Nmap Scripts:** https://nmap.org/nsedoc/
- **Docker Hub:** https://hub.docker.com/r/nmap/nmap

---

**Quick Reference v1.0** | October 26, 2025

