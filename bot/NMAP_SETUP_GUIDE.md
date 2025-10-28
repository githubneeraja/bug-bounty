# Nmap Scanner Setup Guide

## Overview

The Nmap Scanner module provides Python integration with Nmap for performing port scans and SSL/TLS analysis via Docker. It enables comprehensive network reconnaissance with structured output.

## What is Nmap?

**Nmap** (Network Mapper) is a powerful open-source tool for network discovery and security auditing:
- Port scanning and enumeration
- Service version detection
- OS fingerprinting
- SSL/TLS certificate analysis
- Vulnerability detection

## Prerequisites

### Required
- Python 3.11+
- Docker (for running Nmap)
- Internet connection

### Optional
- Nmap installed locally (for direct usage)

## Installation

### Step 1: Install Docker

**Windows:**
```bash
# Download Docker Desktop from https://www.docker.com/products/docker-desktop
# Or use Chocolatey
choco install docker-desktop
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install docker.io
sudo usermod -aG docker $USER
```

**macOS:**
```bash
brew install docker
# Or download Docker Desktop
```

### Step 2: Verify Docker Installation

```bash
docker --version
docker run hello-world
```

### Step 3: Pull Nmap Docker Image

```bash
docker pull nmap/nmap:latest
```

### Step 4: Install Python Module

The module is already included in your project. No additional installation needed.

## Quick Start

### Basic Port Scan

```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.port_scan("example.com", ports="1-1000")

print(f"Open Ports: {results['open_ports']}")
print(f"Services: {results['services']}")
```

### SSL/TLS Analysis

```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.ssl_tls_scan("example.com", port=443)

print(f"SSL/TLS Enabled: {results['ssl_enabled']}")
print(f"Protocols: {results['protocols']}")
print(f"Ciphers: {results['ciphers']}")
```

### Full Scan

```python
from nmap_scanner import scan_target

results = scan_target(
    "example.com",
    ports="1-1000",
    ssl_port=443,
    output_file="nmap_results.txt"
)
```

## API Reference

### NmapScanner Class

```python
class NmapScanner:
    def __init__(docker_image: str = "nmap/nmap:latest")
    def verify_docker() -> bool
    def port_scan(target: str, ports: str = "1-1000", service_detection: bool = True) -> Dict
    def ssl_tls_scan(target: str, port: int = 443) -> Dict
    def full_scan(target: str, ports: str = "1-1000", ssl_port: int = 443) -> Dict
```

### Main Functions

```python
def scan_target(
    target: str,
    ports: str = "1-1000",
    ssl_port: int = 443,
    output_file: Optional[str] = None
) -> Dict[str, Any]

def save_results(results: Dict[str, Any], output_file: str) -> None
```

## Output Format

### Port Scan Results

```python
{
    'target': 'example.com',
    'timestamp': '2025-10-26T10:00:00',
    'open_ports': [80, 443],
    'closed_ports': [22, 25],
    'filtered_ports': [3306],
    'services': {
        80: 'http',
        443: 'https'
    }
}
```

### SSL/TLS Results

```python
{
    'target': 'example.com',
    'port': 443,
    'timestamp': '2025-10-26T10:00:00',
    'ssl_enabled': True,
    'certificate_info': {
        'subject': 'CN=example.com',
        'issuer': 'CN=Let\'s Encrypt'
    },
    'protocols': ['TLSv1.2', 'TLSv1.3'],
    'ciphers': ['AES_256_GCM_SHA384', 'CHACHA20_POLY1305_SHA256']
}
```

## Common Tasks

### Task 1: Scan Common Web Ports

```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.port_scan("example.com", ports="80,443,8080,8443")
```

### Task 2: Detect Service Versions

```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.port_scan(
    "example.com",
    ports="1-1000",
    service_detection=True
)

for port, service in results['services'].items():
    print(f"Port {port}: {service}")
```

### Task 3: Analyze SSL/TLS Configuration

```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.ssl_tls_scan("example.com", port=443)

print(f"Protocols: {results['protocols']}")
print(f"Ciphers: {results['ciphers']}")
```

### Task 4: Save Results to File

```python
from nmap_scanner import scan_target

results = scan_target(
    "example.com",
    output_file="nmap_results.txt"
)
```

### Task 5: Export to JSON

```python
import json
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.full_scan("example.com")

with open("results.json", "w") as f:
    json.dump(results, f, indent=2, default=str)
```

### Task 6: Scan Multiple Targets

```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
targets = ["example.com", "google.com", "github.com"]

for target in targets:
    results = scanner.port_scan(target, ports="80,443")
    print(f"{target}: {results['open_ports']}")
```

## Troubleshooting

### Issue: "Docker not installed"
**Solution:**
1. Install Docker from https://www.docker.com
2. Verify installation: `docker --version`
3. Run: `docker run hello-world`

### Issue: "Docker daemon not running"
**Solution:**
1. Start Docker Desktop (Windows/macOS)
2. Or run: `sudo systemctl start docker` (Linux)

### Issue: "Nmap image not found"
**Solution:**
```bash
docker pull nmap/nmap:latest
```

### Issue: "Permission denied" (Linux)
**Solution:**
```bash
sudo usermod -aG docker $USER
# Log out and log back in
```

### Issue: "Scan timeout"
**Solution:**
- Increase timeout in code
- Reduce port range
- Check network connectivity

## Performance Tips

✅ **Optimization**
- Scan specific ports instead of full range
- Use service detection only when needed
- Batch multiple targets
- Cache results

✅ **Best Practices**
- Start with common ports (80, 443, 22)
- Use appropriate port ranges
- Handle errors gracefully
- Log all scans

## Security Considerations

⚠️ **Important**
- Only scan targets you own or have permission to scan
- Respect network policies
- Use appropriate scan types
- Log all activities
- Handle results securely

## Docker Configuration

### Custom Docker Image

```python
from nmap_scanner import NmapScanner

scanner = NmapScanner(docker_image="custom/nmap:latest")
```

### Docker Options

```bash
# Pull specific version
docker pull nmap/nmap:7.92

# List available versions
docker search nmap/nmap
```

## Advanced Usage

### Custom Nmap Arguments

```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
stdout, stderr, code = scanner.run_docker_nmap([
    "nmap",
    "-p", "1-65535",
    "-sV",
    "-O",
    "example.com"
])
```

### Error Handling

```python
from nmap_scanner import NmapScanner

try:
    scanner = NmapScanner()
    results = scanner.port_scan("example.com")
except RuntimeError as e:
    print(f"Scan failed: {e}")
```

## Resources

- **Nmap Official:** https://nmap.org
- **Nmap Documentation:** https://nmap.org/book/
- **Docker Hub:** https://hub.docker.com/r/nmap/nmap
- **Nmap Scripts:** https://nmap.org/nsedoc/

## Next Steps

1. Install Docker
2. Pull Nmap image: `docker pull nmap/nmap:latest`
3. Test basic scan: `python nmap_scanner.py example.com`
4. Review examples: `python nmap_examples.py`
5. Integrate into workflow

---

**Last Updated:** October 26, 2025

