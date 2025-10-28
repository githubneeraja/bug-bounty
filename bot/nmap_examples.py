#!/usr/bin/env python3
"""
Nmap Scanner Examples
Demonstrates various usage patterns for the Nmap scanner module
"""

import json
from nmap_scanner import NmapScanner, scan_target, save_results


def example_1_basic_port_scan():
    """Example 1: Basic port scan"""
    print("\n" + "="*70)
    print("Example 1: Basic Port Scan")
    print("="*70)
    
    try:
        scanner = NmapScanner()
        results = scanner.port_scan("example.com", ports="1-1000")
        
        print(f"Target: {results['target']}")
        print(f"Open Ports: {len(results['open_ports'])}")
        if results['open_ports']:
            print(f"  {', '.join(map(str, results['open_ports']))}")
        print(f"Services: {results['services']}")
    
    except Exception as e:
        print(f"Error: {e}")


def example_2_ssl_tls_scan():
    """Example 2: SSL/TLS analysis"""
    print("\n" + "="*70)
    print("Example 2: SSL/TLS Analysis")
    print("="*70)
    
    try:
        scanner = NmapScanner()
        results = scanner.ssl_tls_scan("example.com", port=443)
        
        print(f"Target: {results['target']}")
        print(f"Port: {results['port']}")
        print(f"SSL/TLS Enabled: {results['ssl_enabled']}")
        print(f"Protocols: {results['protocols']}")
        print(f"Ciphers: {len(results['ciphers'])} found")
        if results['certificate_info']:
            print("Certificate Info:")
            for key, value in results['certificate_info'].items():
                print(f"  {key}: {value}")
    
    except Exception as e:
        print(f"Error: {e}")


def example_3_full_scan():
    """Example 3: Full scan (port + SSL/TLS)"""
    print("\n" + "="*70)
    print("Example 3: Full Scan")
    print("="*70)
    
    try:
        scanner = NmapScanner()
        results = scanner.full_scan("example.com", ports="1-1000", ssl_port=443)
        
        print(f"Target: {results['target']}")
        print(f"Timestamp: {results['timestamp']}")
        
        if results['port_scan']:
            print(f"\nPort Scan Results:")
            print(f"  Open Ports: {len(results['port_scan']['open_ports'])}")
            print(f"  Closed Ports: {len(results['port_scan']['closed_ports'])}")
            print(f"  Filtered Ports: {len(results['port_scan']['filtered_ports'])}")
        
        if results['ssl_scan']:
            print(f"\nSSL/TLS Results:")
            print(f"  SSL/TLS Enabled: {results['ssl_scan']['ssl_enabled']}")
            print(f"  Protocols: {results['ssl_scan']['protocols']}")
        
        if results['errors']:
            print(f"\nErrors: {len(results['errors'])}")
            for error in results['errors']:
                print(f"  • {error}")
    
    except Exception as e:
        print(f"Error: {e}")


def example_4_custom_port_range():
    """Example 4: Custom port range"""
    print("\n" + "="*70)
    print("Example 4: Custom Port Range")
    print("="*70)
    
    try:
        scanner = NmapScanner()
        # Scan common web ports
        results = scanner.port_scan("example.com", ports="80,443,8080,8443")
        
        print(f"Target: {results['target']}")
        print(f"Open Ports: {results['open_ports']}")
        print(f"Services:")
        for port, service in results['services'].items():
            print(f"  Port {port}: {service}")
    
    except Exception as e:
        print(f"Error: {e}")


def example_5_save_results():
    """Example 5: Save results to file"""
    print("\n" + "="*70)
    print("Example 5: Save Results to File")
    print("="*70)
    
    try:
        results = scan_target(
            "example.com",
            ports="1-1000",
            ssl_port=443,
            output_file="nmap_results.txt"
        )
        
        print(f"Scan complete!")
        print(f"Results saved to: nmap_results.txt")
        print(f"Target: {results['target']}")
    
    except Exception as e:
        print(f"Error: {e}")


def example_6_json_export():
    """Example 6: Export results to JSON"""
    print("\n" + "="*70)
    print("Example 6: JSON Export")
    print("="*70)
    
    try:
        scanner = NmapScanner()
        results = scanner.full_scan("example.com")
        
        # Save to JSON
        with open("nmap_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"Results exported to: nmap_results.json")
        print(f"JSON content preview:")
        print(json.dumps(results, indent=2, default=str)[:500] + "...")
    
    except Exception as e:
        print(f"Error: {e}")


def example_7_multiple_targets():
    """Example 7: Scan multiple targets"""
    print("\n" + "="*70)
    print("Example 7: Multiple Targets")
    print("="*70)
    
    targets = ["example.com", "google.com", "github.com"]
    all_results = {}
    
    try:
        scanner = NmapScanner()
        
        for target in targets:
            print(f"\nScanning {target}...")
            results = scanner.port_scan(target, ports="80,443")
            all_results[target] = results
            print(f"  Open Ports: {results['open_ports']}")
        
        # Save combined results
        with open("nmap_multiple_results.json", "w") as f:
            json.dump(all_results, f, indent=2, default=str)
        
        print(f"\nAll results saved to: nmap_multiple_results.json")
    
    except Exception as e:
        print(f"Error: {e}")


def example_8_error_handling():
    """Example 8: Error handling"""
    print("\n" + "="*70)
    print("Example 8: Error Handling")
    print("="*70)
    
    try:
        scanner = NmapScanner()
        
        # Try scanning invalid target
        try:
            results = scanner.port_scan("invalid..domain", ports="80,443")
            print(f"Results: {results}")
        except Exception as e:
            print(f"Caught error: {e}")
        
        # Try with Docker not available
        try:
            bad_scanner = NmapScanner(docker_image="nonexistent/image")
            results = bad_scanner.port_scan("example.com")
        except Exception as e:
            print(f"Caught error: {e}")
    
    except Exception as e:
        print(f"Error: {e}")


def example_9_service_detection():
    """Example 9: Service version detection"""
    print("\n" + "="*70)
    print("Example 9: Service Version Detection")
    print("="*70)
    
    try:
        scanner = NmapScanner()
        results = scanner.port_scan(
            "example.com",
            ports="80,443,22,25",
            service_detection=True
        )
        
        print(f"Target: {results['target']}")
        print(f"Open Ports with Services:")
        for port, service in sorted(results['services'].items()):
            print(f"  Port {port}: {service}")
    
    except Exception as e:
        print(f"Error: {e}")


def run_all_examples():
    """Run all examples"""
    print("\n" + "="*70)
    print("NMAP SCANNER EXAMPLES")
    print("="*70)
    
    examples = [
        ("Basic Port Scan", example_1_basic_port_scan),
        ("SSL/TLS Analysis", example_2_ssl_tls_scan),
        ("Full Scan", example_3_full_scan),
        ("Custom Port Range", example_4_custom_port_range),
        ("Save Results", example_5_save_results),
        ("JSON Export", example_6_json_export),
        ("Multiple Targets", example_7_multiple_targets),
        ("Error Handling", example_8_error_handling),
        ("Service Detection", example_9_service_detection),
    ]
    
    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\nError in {name}: {e}")
    
    print("\n" + "="*70)
    print("EXAMPLES COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_all_examples()

