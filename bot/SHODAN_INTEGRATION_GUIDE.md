# Shodan Scanner Integration Guide

## Overview

This guide shows how to integrate the Shodan Scanner with other modules and workflows.

## Integration Patterns

### Pattern 1: Amass + Shodan Pipeline

```python
from amass_subdomain_enum import enumerate_subdomains
from shodan_scanner import scan_with_shodan

# Step 1: Enumerate subdomains
domain = 'example.com'
subdomains = enumerate_subdomains(domain)
print(f"Found {len(subdomains)} subdomains")

# Step 2: Scan with Shodan
results = scan_with_shodan(subdomains)
print(f"Scanned: {results['scanned_subdomains']}")

# Step 3: Process results
for subdomain, data in results['subdomains'].items():
    if data['resolved']:
        print(f"{subdomain}: {data['ip']}")
```

### Pattern 2: Batch Processing

```python
from shodan_scanner import scan_with_shodan
import json

domains = ['example.com', 'google.com', 'github.com']
all_results = {}

for domain in domains:
    subdomains = [f"api.{domain}", f"www.{domain}"]
    results = scan_with_shodan(subdomains)
    all_results[domain] = results

# Save all results
with open('all_results.json', 'w') as f:
    json.dump(all_results, f, indent=2, default=str)
```

### Pattern 3: Data Export Pipeline

```python
import json
import csv
import pandas as pd
from shodan_scanner import scan_with_shodan

subdomains = ['api.example.com', 'www.example.com']
results = scan_with_shodan(subdomains)

# Export to JSON
with open('results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

# Export to CSV
with open('results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, ['Subdomain', 'IP', 'Country', 'Services'])
    writer.writeheader()
    for sub, data in results['subdomains'].items():
        if data['scan_data']:
            writer.writerow({
                'Subdomain': sub,
                'IP': data['ip'],
                'Country': data['scan_data'].get('country'),
                'Services': len(data['scan_data'].get('services', []))
            })

# Export to Pandas
data = []
for sub, info in results['subdomains'].items():
    if info['scan_data']:
        data.append({
            'Subdomain': sub,
            'IP': info['ip'],
            'Country': info['scan_data'].get('country'),
            'Services': len(info['scan_data'].get('services', []))
        })
df = pd.DataFrame(data)
df.to_excel('results.xlsx', index=False)
```

### Pattern 4: Make.com Webhook Integration

```python
import requests
import os
from datetime import datetime
from shodan_scanner import scan_with_shodan
from dotenv import load_dotenv

load_dotenv()

def send_to_make(subdomains):
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    
    try:
        results = scan_with_shodan(subdomains)
        
        payload = {
            'timestamp': datetime.now().isoformat(),
            'total_subdomains': results['total_subdomains'],
            'scanned_subdomains': results['scanned_subdomains'],
            'results': results['subdomains'],
            'status': 'success'
        }
        
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 200
    
    except Exception as e:
        payload = {
            'timestamp': datetime.now().isoformat(),
            'error': str(e),
            'status': 'failed'
        }
        requests.post(webhook_url, json=payload)
        return False

# Usage
send_to_make(['api.example.com', 'www.example.com'])
```

### Pattern 5: Vulnerability Analysis

```python
from shodan_scanner import scan_with_shodan

subdomains = ['api.example.com', 'www.example.com']
results = scan_with_shodan(subdomains)

vulnerable_hosts = []

for subdomain, data in results['subdomains'].items():
    if data['scan_data']:
        vulns = data['scan_data'].get('vulnerabilities', [])
        if vulns:
            vulnerable_hosts.append({
                'subdomain': subdomain,
                'ip': data['ip'],
                'vulnerabilities': vulns,
                'count': len(vulns)
            })

# Report
print(f"Vulnerable hosts: {len(vulnerable_hosts)}")
for host in vulnerable_hosts:
    print(f"\n{host['subdomain']} ({host['ip']})")
    print(f"Vulnerabilities: {host['count']}")
    for vuln in host['vulnerabilities'][:5]:
        print(f"  • {vuln}")
```

### Pattern 6: Service Discovery

```python
from shodan_scanner import scan_with_shodan

subdomains = ['api.example.com', 'www.example.com']
results = scan_with_shodan(subdomains)

services_by_port = {}

for subdomain, data in results['subdomains'].items():
    if data['scan_data']:
        for service in data['scan_data'].get('services', []):
            port = service.get('port')
            protocol = service.get('protocol', 'unknown')
            
            key = f"{port}/{protocol}"
            if key not in services_by_port:
                services_by_port[key] = []
            
            services_by_port[key].append({
                'subdomain': subdomain,
                'ip': data['ip'],
                'product': service.get('product'),
                'version': service.get('version')
            })

# Report
for service, hosts in sorted(services_by_port.items()):
    print(f"\n{service}: {len(hosts)} host(s)")
    for host in hosts:
        print(f"  {host['subdomain']} ({host['ip']})")
        if host['product']:
            print(f"    {host['product']} {host['version']}")
```

### Pattern 7: Geolocation Analysis

```python
from shodan_scanner import scan_with_shodan

subdomains = ['api.example.com', 'www.example.com']
results = scan_with_shodan(subdomains)

locations = {}

for subdomain, data in results['subdomains'].items():
    if data['scan_data']:
        scan = data['scan_data']
        country = scan.get('country', 'Unknown')
        city = scan.get('city', 'Unknown')
        
        key = f"{country}/{city}"
        if key not in locations:
            locations[key] = []
        
        locations[key].append({
            'subdomain': subdomain,
            'ip': data['ip'],
            'lat': scan.get('latitude'),
            'lon': scan.get('longitude')
        })

# Report
for location, hosts in sorted(locations.items()):
    print(f"\n{location}: {len(hosts)} host(s)")
    for host in hosts:
        print(f"  {host['subdomain']} ({host['ip']})")
```

### Pattern 8: Error Handling & Retry

```python
import time
from shodan_scanner import scan_with_shodan

def scan_with_retry(subdomains, max_retries=3):
    for attempt in range(max_retries):
        try:
            results = scan_with_shodan(subdomains)
            return results
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Attempt {attempt + 1} failed, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

# Usage
try:
    results = scan_with_retry(['api.example.com'])
except Exception as e:
    print(f"Failed after retries: {e}")
```

### Pattern 9: Database Storage

```python
import sqlite3
from shodan_scanner import scan_with_shodan

def store_results(subdomains, db_file='shodan_results.db'):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY,
            subdomain TEXT,
            ip TEXT,
            country TEXT,
            services INTEGER,
            vulnerabilities INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Scan and store
    results = scan_with_shodan(subdomains)
    
    for subdomain, data in results['subdomains'].items():
        if data['scan_data']:
            scan = data['scan_data']
            cursor.execute('''
                INSERT INTO scans (subdomain, ip, country, services, vulnerabilities)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                subdomain,
                data['ip'],
                scan.get('country'),
                len(scan.get('services', [])),
                len(scan.get('vulnerabilities', []))
            ))
    
    conn.commit()
    conn.close()

# Usage
store_results(['api.example.com', 'www.example.com'])
```

### Pattern 10: Scheduled Scanning

```python
import schedule
import time
from shodan_scanner import scan_with_shodan

def scheduled_scan():
    subdomains = ['api.example.com', 'www.example.com']
    results = scan_with_shodan(subdomains)
    print(f"Scan complete: {results['scanned_subdomains']} scanned")

# Schedule
schedule.every().day.at("10:30").do(scheduled_scan)

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(60)
```

## Configuration

### Environment Variables

```bash
# .env file
SHODAN_API_KEY=your_api_key
MAKE_WEBHOOK_URL=https://hook.make.com/your_webhook
DATABASE_URL=sqlite:///shodan_results.db
```

### Configuration File

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

SHODAN_API_KEY = os.getenv('SHODAN_API_KEY')
MAKE_WEBHOOK_URL = os.getenv('MAKE_WEBHOOK_URL')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///shodan_results.db')
MAX_RETRIES = 3
RETRY_DELAY = 2
```

## Best Practices

✅ **Error Handling**
- Implement try-except blocks
- Log errors for debugging
- Implement retry logic

✅ **Performance**
- Batch multiple subdomains
- Cache results
- Implement rate limiting

✅ **Security**
- Store API keys in environment variables
- Never commit secrets
- Use HTTPS for webhooks

✅ **Data Management**
- Export results regularly
- Archive historical data
- Implement data retention policies

## Troubleshooting

### Integration Issues

**Problem:** Module not found
```python
# Solution: Install dependencies
pip install shodan requests pandas
```

**Problem:** API key not working
```python
# Solution: Verify environment variable
import os
print(os.getenv('SHODAN_API_KEY'))
```

**Problem:** Webhook not receiving data
```python
# Solution: Check webhook URL and test manually
import requests
requests.post('https://hook.make.com/path', json={'test': 'data'})
```

## Next Steps

1. Review integration patterns
2. Choose pattern for your use case
3. Implement error handling
4. Test with sample data
5. Deploy to production

---

**Last Updated:** October 26, 2025

