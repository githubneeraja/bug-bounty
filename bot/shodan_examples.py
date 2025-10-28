#!/usr/bin/env python3
"""
Shodan Scanner Examples
Demonstrates various use cases and integration patterns
"""

import json
import csv
from datetime import datetime
from shodan_scanner import scan_with_shodan, ShodanScanner
import pandas as pd


def example_1_basic_scan():
    """Example 1: Basic subdomain scanning"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Subdomain Scanning")
    print("="*70)
    
    try:
        subdomains = ['api.example.com', 'www.example.com', 'mail.example.com']
        print(f"\nScanning {len(subdomains)} subdomains...")
        
        results = scan_with_shodan(subdomains)
        
        print(f"\n✓ Scan complete: {results['scanned_subdomains']}/{results['total_subdomains']} scanned\n")
        
        for subdomain, data in results['subdomains'].items():
            if data['resolved']:
                print(f"  {subdomain} -> {data['ip']}")
                if data['scan_data']:
                    services = len(data['scan_data'].get('services', []))
                    print(f"    Services: {services}")
            else:
                print(f"  {subdomain} -> Could not resolve")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def example_2_detailed_results():
    """Example 2: Detailed scan results"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Detailed Scan Results")
    print("="*70)
    
    try:
        subdomains = ['api.example.com']
        results = scan_with_shodan(subdomains)
        
        for subdomain, data in results['subdomains'].items():
            if data['scan_data']:
                scan = data['scan_data']
                
                print(f"\nSubdomain: {subdomain}")
                print(f"IP: {scan.get('ip')}")
                print(f"Country: {scan.get('country')}")
                print(f"City: {scan.get('city')}")
                print(f"Organization: {scan.get('organization')}")
                print(f"ISP: {scan.get('isp')}")
                print(f"Ports: {scan.get('ports')}")
                print(f"OS: {scan.get('os')}")
                print(f"Tags: {scan.get('tags')}")
                
                if scan.get('services'):
                    print(f"\nServices ({len(scan['services'])}):")
                    for service in scan['services'][:3]:
                        print(f"  Port {service.get('port')}: {service.get('protocol')}")
                
                if scan.get('vulnerabilities'):
                    print(f"\nVulnerabilities: {len(scan['vulnerabilities'])}")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def example_3_export_json():
    """Example 3: Export results to JSON"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Export to JSON")
    print("="*70)
    
    try:
        subdomains = ['api.example.com', 'www.example.com']
        results = scan_with_shodan(subdomains)
        
        filename = f"shodan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n✓ Results saved to: {filename}")
        print(f"  Total subdomains: {results['total_subdomains']}")
        print(f"  Successfully scanned: {results['scanned_subdomains']}")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def example_4_export_csv():
    """Example 4: Export results to CSV"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Export to CSV")
    print("="*70)
    
    try:
        subdomains = ['api.example.com', 'www.example.com']
        results = scan_with_shodan(subdomains)
        
        csv_data = []
        for subdomain, data in results['subdomains'].items():
            if data['scan_data']:
                scan = data['scan_data']
                csv_data.append({
                    'Subdomain': subdomain,
                    'IP': data['ip'],
                    'Country': scan.get('country', 'N/A'),
                    'City': scan.get('city', 'N/A'),
                    'Organization': scan.get('organization', 'N/A'),
                    'Ports': ', '.join(map(str, scan.get('ports', []))),
                    'Services': len(scan.get('services', [])),
                    'Vulnerabilities': len(scan.get('vulnerabilities', []))
                })
        
        filename = f"shodan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'Subdomain', 'IP', 'Country', 'City', 'Organization',
                'Ports', 'Services', 'Vulnerabilities'
            ])
            writer.writeheader()
            writer.writerows(csv_data)
        
        print(f"\n✓ Results saved to: {filename}")
        print(f"  Records: {len(csv_data)}")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def example_5_pandas_analysis():
    """Example 5: Analyze with Pandas"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Pandas Analysis")
    print("="*70)
    
    try:
        subdomains = ['api.example.com', 'www.example.com', 'mail.example.com']
        results = scan_with_shodan(subdomains)
        
        # Prepare data for DataFrame
        data = []
        for subdomain, info in results['subdomains'].items():
            if info['scan_data']:
                scan = info['scan_data']
                data.append({
                    'Subdomain': subdomain,
                    'IP': info['ip'],
                    'Country': scan.get('country'),
                    'Services': len(scan.get('services', [])),
                    'Vulnerabilities': len(scan.get('vulnerabilities', []))
                })
        
        if data:
            df = pd.DataFrame(data)
            
            print(f"\n✓ Analysis Results:\n")
            print(df.to_string(index=False))
            
            print(f"\n\nStatistics:")
            print(f"  Total IPs scanned: {len(df)}")
            print(f"  Average services per IP: {df['Services'].mean():.1f}")
            print(f"  Total vulnerabilities: {df['Vulnerabilities'].sum()}")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def example_6_service_analysis():
    """Example 6: Analyze services across subdomains"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Service Analysis")
    print("="*70)
    
    try:
        subdomains = ['api.example.com', 'www.example.com']
        results = scan_with_shodan(subdomains)
        
        service_summary = {}
        
        for subdomain, data in results['subdomains'].items():
            if data['scan_data']:
                scan = data['scan_data']
                
                for service in scan.get('services', []):
                    port = service.get('port')
                    protocol = service.get('protocol', 'unknown')
                    
                    key = f"{port}/{protocol}"
                    if key not in service_summary:
                        service_summary[key] = []
                    
                    service_summary[key].append(subdomain)
        
        print(f"\n✓ Service Summary:\n")
        for service, subdomains_list in sorted(service_summary.items()):
            print(f"  {service}: {len(subdomains_list)} subdomain(s)")
            for sub in subdomains_list:
                print(f"    • {sub}")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def example_7_vulnerability_scan():
    """Example 7: Vulnerability detection"""
    print("\n" + "="*70)
    print("EXAMPLE 7: Vulnerability Detection")
    print("="*70)
    
    try:
        subdomains = ['api.example.com', 'www.example.com']
        results = scan_with_shodan(subdomains)
        
        vulnerable_ips = []
        
        for subdomain, data in results['subdomains'].items():
            if data['scan_data']:
                scan = data['scan_data']
                vulns = scan.get('vulnerabilities', [])
                
                if vulns:
                    vulnerable_ips.append({
                        'subdomain': subdomain,
                        'ip': data['ip'],
                        'vulnerabilities': vulns,
                        'count': len(vulns)
                    })
        
        print(f"\n✓ Vulnerability Report:\n")
        print(f"  Total vulnerable IPs: {len(vulnerable_ips)}")
        
        for item in vulnerable_ips:
            print(f"\n  {item['subdomain']} ({item['ip']})")
            print(f"  Vulnerabilities: {item['count']}")
            for vuln in item['vulnerabilities'][:3]:
                print(f"    • {vuln}")
            
            if item['count'] > 3:
                print(f"    ... and {item['count'] - 3} more")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def example_8_integration_with_amass():
    """Example 8: Integration with Amass enumeration"""
    print("\n" + "="*70)
    print("EXAMPLE 8: Integration with Amass")
    print("="*70)
    
    try:
        from amass_subdomain_enum import enumerate_subdomains
        
        domain = 'example.com'
        print(f"\nEnumerating subdomains for {domain}...")
        
        subdomains = enumerate_subdomains(domain)
        print(f"Found {len(subdomains)} subdomains")
        
        # Scan with Shodan
        print(f"\nScanning with Shodan...")
        results = scan_with_shodan(subdomains[:5])  # Limit to first 5
        
        print(f"\n✓ Scan Results:")
        print(f"  Total: {results['total_subdomains']}")
        print(f"  Scanned: {results['scanned_subdomains']}")
        
        for subdomain, data in results['subdomains'].items():
            if data['resolved']:
                services = len(data['scan_data'].get('services', [])) if data['scan_data'] else 0
                print(f"  {subdomain}: {data['ip']} ({services} services)")
    
    except ImportError:
        print("✗ Amass module not available")
    except Exception as e:
        print(f"✗ Error: {e}")


def example_9_error_handling():
    """Example 9: Error handling"""
    print("\n" + "="*70)
    print("EXAMPLE 9: Error Handling")
    print("="*70)
    
    test_cases = [
        (['api.example.com'], "Valid subdomain"),
        (['invalid..domain'], "Invalid domain format"),
        (['localhost'], "Local domain"),
        ([], "Empty list"),
    ]
    
    for subdomains, description in test_cases:
        print(f"\nTest: {description}")
        try:
            if subdomains:
                results = scan_with_shodan(subdomains)
                print(f"  ✓ Scanned: {results['scanned_subdomains']}/{results['total_subdomains']}")
            else:
                results = scan_with_shodan(subdomains)
        except ValueError as e:
            print(f"  ✗ ValueError: {e}")
        except Exception as e:
            print(f"  ✗ {type(e).__name__}: {e}")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("SHODAN SCANNER EXAMPLES")
    print("="*70)
    
    examples = [
        ("1", "Basic Scanning", example_1_basic_scan),
        ("2", "Detailed Results", example_2_detailed_results),
        ("3", "Export to JSON", example_3_export_json),
        ("4", "Export to CSV", example_4_export_csv),
        ("5", "Pandas Analysis", example_5_pandas_analysis),
        ("6", "Service Analysis", example_6_service_analysis),
        ("7", "Vulnerability Detection", example_7_vulnerability_scan),
        ("8", "Integration with Amass", example_8_integration_with_amass),
        ("9", "Error Handling", example_9_error_handling),
    ]
    
    print("\nAvailable Examples:")
    for num, name, _ in examples:
        print(f"  {num}. {name}")
    
    print("\nNote: Shodan API key required (set SHODAN_API_KEY environment variable)")
    
    # Run all examples
    for num, name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n✗ Example {num} failed: {e}")


if __name__ == "__main__":
    main()

