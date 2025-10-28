#!/usr/bin/env python3
"""
Amass Subdomain Enumeration Examples
Demonstrates various use cases and integration patterns
"""

import json
import csv
from datetime import datetime
from amass_subdomain_enum import enumerate_subdomains, AmassEnumerator
import pandas as pd


def example_1_basic_enumeration():
    """Example 1: Basic subdomain enumeration"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Subdomain Enumeration")
    print("="*60)
    
    try:
        domain = "example.com"
        print(f"\nEnumerating subdomains for: {domain}")
        
        subdomains = enumerate_subdomains(domain)
        
        print(f"\n✓ Found {len(subdomains)} subdomains:\n")
        for i, subdomain in enumerate(subdomains[:10], 1):
            print(f"  {i}. {subdomain}")
        
        if len(subdomains) > 10:
            print(f"  ... and {len(subdomains) - 10} more")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def example_2_json_output():
    """Example 2: Detailed JSON output with metadata"""
    print("\n" + "="*60)
    print("EXAMPLE 2: JSON Output with Metadata")
    print("="*60)
    
    try:
        enumerator = AmassEnumerator()
        domain = "example.com"
        
        print(f"\nEnumerating with detailed metadata for: {domain}")
        
        results = enumerator.enumerate_subdomains_json(domain)
        
        print(f"\n✓ Found {len(results)} subdomains with metadata:\n")
        
        for result in results[:5]:
            print(f"  Domain: {result['name']}")
            print(f"  Source: {result['source']}")
            print(f"  Type: {result['type']}")
            if result['addresses']:
                print(f"  IPs: {', '.join(result['addresses'])}")
            print()
    
    except Exception as e:
        print(f"✗ Error: {e}")


def example_3_save_to_csv():
    """Example 3: Save results to CSV file"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Save Results to CSV")
    print("="*60)
    
    try:
        enumerator = AmassEnumerator()
        domain = "example.com"
        
        print(f"\nEnumerating and saving to CSV: {domain}")
        
        results = enumerator.enumerate_subdomains_json(domain)
        
        # Prepare data for CSV
        csv_data = []
        for result in results:
            csv_data.append({
                'Subdomain': result['name'],
                'Source': result['source'],
                'Type': result['type'],
                'Tag': result['tag'],
                'IP Addresses': ', '.join(result['addresses']) if result['addresses'] else 'N/A'
            })
        
        # Save to CSV
        filename = f"subdomains_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Subdomain', 'Source', 'Type', 'Tag', 'IP Addresses'])
            writer.writeheader()
            writer.writerows(csv_data)
        
        print(f"\n✓ Results saved to: {filename}")
        print(f"  Total records: {len(csv_data)}")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def example_4_save_to_json():
    """Example 4: Save results to JSON file"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Save Results to JSON")
    print("="*60)
    
    try:
        enumerator = AmassEnumerator()
        domain = "example.com"
        
        print(f"\nEnumerating and saving to JSON: {domain}")
        
        results = enumerator.enumerate_subdomains_json(domain)
        
        # Prepare output
        output = {
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
            "total_subdomains": len(results),
            "subdomains": results
        }
        
        # Save to JSON
        filename = f"subdomains_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n✓ Results saved to: {filename}")
        print(f"  Total records: {len(results)}")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def example_5_pandas_analysis():
    """Example 5: Analyze results with Pandas"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Pandas Data Analysis")
    print("="*60)
    
    try:
        enumerator = AmassEnumerator()
        domain = "example.com"
        
        print(f"\nEnumerating and analyzing with Pandas: {domain}")
        
        results = enumerator.enumerate_subdomains_json(domain)
        
        # Create DataFrame
        df = pd.DataFrame(results)
        
        print(f"\n✓ Analysis Results:\n")
        print(f"  Total subdomains: {len(df)}")
        print(f"\n  Subdomains by source:")
        print(df['source'].value_counts().to_string())
        print(f"\n  Subdomains by type:")
        print(df['type'].value_counts().to_string())
        
        # Subdomains with IP addresses
        with_ips = df[df['addresses'].apply(lambda x: len(x) > 0)]
        print(f"\n  Subdomains with resolved IPs: {len(with_ips)}")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def example_6_multiple_domains():
    """Example 6: Enumerate multiple domains"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Multiple Domain Enumeration")
    print("="*60)
    
    domains = ["example.com", "google.com", "github.com"]
    results = {}
    
    for domain in domains:
        try:
            print(f"\nEnumerating: {domain}")
            subdomains = enumerate_subdomains(domain)
            results[domain] = {
                "count": len(subdomains),
                "subdomains": subdomains[:5]  # First 5 for display
            }
            print(f"  ✓ Found {len(subdomains)} subdomains")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results[domain] = {"count": 0, "error": str(e)}
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for domain, data in results.items():
        if "error" in data:
            print(f"\n{domain}: Error - {data['error']}")
        else:
            print(f"\n{domain}: {data['count']} subdomains")
            for subdomain in data['subdomains']:
                print(f"  • {subdomain}")


def example_7_webhook_integration():
    """Example 7: Send results to webhook (Make.com)"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Webhook Integration (Make.com)")
    print("="*60)
    
    try:
        import requests
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        webhook_url = os.getenv('MAKE_WEBHOOK_URL')
        
        if not webhook_url:
            print("\n⚠️  MAKE_WEBHOOK_URL not configured in .env")
            print("   Skipping webhook integration example")
            return
        
        domain = "example.com"
        print(f"\nEnumerating and sending to webhook: {domain}")
        
        subdomains = enumerate_subdomains(domain)
        
        payload = {
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
            "total_subdomains": len(subdomains),
            "subdomains": subdomains,
            "status": "success"
        }
        
        print(f"\nSending {len(subdomains)} subdomains to webhook...")
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"✓ Successfully sent to webhook")
        else:
            print(f"✗ Webhook returned status: {response.status_code}")
    
    except ImportError:
        print("\n⚠️  requests library not available")
    except Exception as e:
        print(f"✗ Error: {e}")


def example_8_error_handling():
    """Example 8: Error handling and edge cases"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Error Handling")
    print("="*60)
    
    test_cases = [
        ("example.com", "Valid domain"),
        ("", "Empty domain"),
        ("invalid..domain", "Invalid domain format"),
        ("localhost", "Local domain"),
    ]
    
    for domain, description in test_cases:
        print(f"\nTest: {description} - '{domain}'")
        try:
            subdomains = enumerate_subdomains(domain)
            print(f"  ✓ Found {len(subdomains)} subdomains")
        except ValueError as e:
            print(f"  ✗ ValueError: {e}")
        except RuntimeError as e:
            print(f"  ✗ RuntimeError: {e}")
        except Exception as e:
            print(f"  ✗ {type(e).__name__}: {e}")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("AMASS SUBDOMAIN ENUMERATION EXAMPLES")
    print("="*60)
    
    examples = [
        ("1", "Basic Enumeration", example_1_basic_enumeration),
        ("2", "JSON Output", example_2_json_output),
        ("3", "Save to CSV", example_3_save_to_csv),
        ("4", "Save to JSON", example_4_save_to_json),
        ("5", "Pandas Analysis", example_5_pandas_analysis),
        ("6", "Multiple Domains", example_6_multiple_domains),
        ("7", "Webhook Integration", example_7_webhook_integration),
        ("8", "Error Handling", example_8_error_handling),
    ]
    
    print("\nAvailable Examples:")
    for num, name, _ in examples:
        print(f"  {num}. {name}")
    
    print("\nNote: Amass must be installed for these examples to work")
    print("Install with: choco install amass (Windows)")
    print("             brew install amass (macOS)")
    print("             apt-get install amass (Linux)")
    
    # Run all examples
    for num, name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n✗ Example {num} failed: {e}")


if __name__ == "__main__":
    main()

