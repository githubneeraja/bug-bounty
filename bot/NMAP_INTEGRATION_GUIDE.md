# Nmap Scanner Integration Guide

## Overview

This guide shows how to integrate the Nmap Scanner with other modules and workflows.

## Integration Patterns

### Pattern 1: Amass + Shodan + Nmap Pipeline

```python
from amass_subdomain_enum import enumerate_subdomains
from shodan_scanner import scan_with_shodan
from nmap_scanner import NmapScanner

# Step 1: Enumerate subdomains
domain = 'example.com'
subdomains = enumerate_subdomains(domain)
print(f"Found {len(subdomains)} subdomains")

# Step 2: Scan with Shodan
shodan_results = scan_with_shodan(subdomains[:5])

# Step 3: Port scan with Nmap
scanner = NmapScanner()
for subdomain in subdomains[:5]:
    nmap_results = scanner.port_scan(subdomain, ports='80,443')
    print(f"{subdomain}: {nmap_results['open_ports']}")
```

### Pattern 2: Batch Port Scanning

```python
from nmap_scanner import NmapScanner
import json

targets = ['example.com', 'google.com', 'github.com']
all_results = {}

scanner = NmapScanner()

for target in targets:
    print(f"Scanning {target}...")
    results = scanner.port_scan(target, ports='1-1000')
    all_results[target] = results

# Save combined results
with open('nmap_batch_results.json', 'w') as f:
    json.dump(all_results, f, indent=2, default=str)
```

### Pattern 3: SSL/TLS Audit

```python
from nmap_scanner import NmapScanner

targets = ['example.com', 'google.com', 'github.com']
scanner = NmapScanner()

print("SSL/TLS Audit Results")
print("=" * 70)

for target in targets:
    results = scanner.ssl_tls_scan(target, port=443)
    
    print(f"\n{target}:")
    print(f"  SSL/TLS Enabled: {results['ssl_enabled']}")
    print(f"  Protocols: {', '.join(results['protocols'])}")
    print(f"  Ciphers: {len(results['ciphers'])} found")
    
    if results['certificate_info']:
        print(f"  Certificate:")
        for key, value in results['certificate_info'].items():
            print(f"    {key}: {value}")
```

### Pattern 4: Vulnerability Assessment

```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.full_scan('example.com', ports='1-1000')

# Analyze results for vulnerabilities
port_scan = results['port_scan']
ssl_scan = results['ssl_scan']

print("Vulnerability Assessment")
print("=" * 70)

# Check for common vulnerable ports
vulnerable_ports = {
    23: 'Telnet (unencrypted)',
    25: 'SMTP (unencrypted)',
    80: 'HTTP (unencrypted)',
    3306: 'MySQL (exposed)',
    5432: 'PostgreSQL (exposed)',
    6379: 'Redis (exposed)'
}

if port_scan:
    for port in port_scan['open_ports']:
        if port in vulnerable_ports:
            print(f"⚠️  Port {port}: {vulnerable_ports[port]}")

# Check SSL/TLS configuration
if ssl_scan and ssl_scan['ssl_enabled']:
    protocols = ssl_scan['protocols']
    if 'SSLv2' in protocols or 'SSLv3' in protocols:
        print("⚠️  Weak SSL/TLS protocols detected")
```

### Pattern 5: Service Enumeration

```python
from nmap_scanner import NmapScanner

scanner = NmapScanner()
results = scanner.port_scan(
    'example.com',
    ports='1-1000',
    service_detection=True
)

print("Service Enumeration")
print("=" * 70)

services_by_type = {}

for port, service in results['services'].items():
    service_type = service.split('/')[0] if '/' in service else service
    
    if service_type not in services_by_type:
        services_by_type[service_type] = []
    
    services_by_type[service_type].append(port)

for service_type, ports in sorted(services_by_type.items()):
    print(f"\n{service_type}:")
    for port in sorted(ports):
        print(f"  Port {port}")
```

### Pattern 6: Export to Multiple Formats

```python
import json
import csv
from nmap_scanner import NmapScanner, save_results

scanner = NmapScanner()
results = scanner.full_scan('example.com')

# Save as text
save_results(results, 'nmap_results.txt')

# Save as JSON
with open('nmap_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

# Save as CSV
if results['port_scan']:
    with open('nmap_ports.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, ['Port', 'State', 'Service'])
        writer.writeheader()
        
        for port in results['port_scan']['open_ports']:
            service = results['port_scan']['services'].get(port, 'unknown')
            writer.writerow({
                'Port': port,
                'State': 'open',
                'Service': service
            })
```

### Pattern 7: Scheduled Scanning

```python
import schedule
import time
from nmap_scanner import scan_target

def scheduled_scan():
    targets = ['example.com', 'google.com']
    
    for target in targets:
        print(f"Scanning {target}...")
        results = scan_target(
            target,
            output_file=f'nmap_{target}_{int(time.time())}.txt'
        )
        print(f"Scan complete: {results['target']}")

# Schedule daily scan at 2 AM
schedule.every().day.at("02:00").do(scheduled_scan)

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(60)
```

### Pattern 8: Database Storage

```python
import sqlite3
from nmap_scanner import NmapScanner

def store_scan_results(results):
    conn = sqlite3.connect('nmap_scans.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY,
            target TEXT,
            timestamp DATETIME,
            open_ports TEXT,
            ssl_enabled BOOLEAN,
            scan_data TEXT
        )
    ''')
    
    # Insert results
    if results['port_scan']:
        open_ports = ','.join(map(str, results['port_scan']['open_ports']))
    else:
        open_ports = ''
    
    ssl_enabled = results['ssl_scan']['ssl_enabled'] if results['ssl_scan'] else False
    
    cursor.execute('''
        INSERT INTO scans (target, timestamp, open_ports, ssl_enabled)
        VALUES (?, ?, ?, ?)
    ''', (results['target'], results['timestamp'], open_ports, ssl_enabled))
    
    conn.commit()
    conn.close()

# Usage
scanner = NmapScanner()
results = scanner.full_scan('example.com')
store_scan_results(results)
```

### Pattern 9: Make.com Webhook Integration

```python
import requests
import json
from nmap_scanner import scan_target
from dotenv import load_dotenv
import os

load_dotenv()

def send_to_make(target):
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    
    try:
        results = scan_target(target)
        
        payload = {
            'target': target,
            'timestamp': results['timestamp'],
            'open_ports': results['port_scan']['open_ports'] if results['port_scan'] else [],
            'ssl_enabled': results['ssl_scan']['ssl_enabled'] if results['ssl_scan'] else False,
            'status': 'success'
        }
        
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 200
    
    except Exception as e:
        payload = {
            'target': target,
            'error': str(e),
            'status': 'failed'
        }
        requests.post(webhook_url, json=payload)
        return False

# Usage
send_to_make('example.com')
```

### Pattern 10: Error Handling & Retry

```python
import time
from nmap_scanner import NmapScanner

def scan_with_retry(target, max_retries=3):
    scanner = NmapScanner()
    
    for attempt in range(max_retries):
        try:
            results = scanner.port_scan(target)
            return results
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Attempt {attempt + 1} failed, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

# Usage
try:
    results = scan_with_retry('example.com')
except Exception as e:
    print(f"Failed after retries: {e}")
```

## Configuration

### Environment Variables

```bash
# .env file
NMAP_DOCKER_IMAGE=nmap/nmap:latest
MAKE_WEBHOOK_URL=https://hook.make.com/your_webhook
```

### Configuration File

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

NMAP_DOCKER_IMAGE = os.getenv('NMAP_DOCKER_IMAGE', 'nmap/nmap:latest')
MAKE_WEBHOOK_URL = os.getenv('MAKE_WEBHOOK_URL')
DEFAULT_PORTS = '1-1000'
DEFAULT_SSL_PORT = 443
SCAN_TIMEOUT = 300
```

## Best Practices

✅ **Error Handling**
- Implement try-except blocks
- Log errors for debugging
- Implement retry logic

✅ **Performance**
- Batch multiple targets
- Cache results
- Use appropriate port ranges

✅ **Security**
- Only scan authorized targets
- Handle results securely
- Log all activities

✅ **Data Management**
- Export results regularly
- Archive historical data
- Implement data retention

## Troubleshooting

### Integration Issues

**Problem:** Module not found
```python
# Solution: Install dependencies
pip install docker
```

**Problem:** Docker connection failed
```python
# Solution: Verify Docker is running
docker ps
```

**Problem:** Scan timeout
```python
# Solution: Reduce port range or increase timeout
results = scanner.port_scan('example.com', ports='80,443')
```

## Next Steps

1. Review integration patterns
2. Choose pattern for your use case
3. Implement error handling
4. Test with sample data
5. Deploy to production

---

**Last Updated:** October 26, 2025

