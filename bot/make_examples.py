#!/usr/bin/env python3
"""
Make.com Integration Examples
Demonstrates various ways to use the recon automation bot with Make.com
"""

import json
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()


# Example 1: Basic Webhook Send
def example_1_basic_webhook():
    """Send basic recon results to Make.com"""
    print("\n" + "="*70)
    print("Example 1: Basic Webhook Send")
    print("="*70)
    
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    
    payload = {
        'target_domain': 'example.com',
        'files': [
            {
                'name': 'amass_results.txt',
                'content': 'example.com\nwww.example.com\napi.example.com'
            },
            {
                'name': 'shodan_results.json',
                'content': json.dumps({
                    'example.com': {
                        'ip': '1.2.3.4',
                        'ports': [80, 443],
                        'services': ['http', 'https']
                    }
                })
            },
            {
                'name': 'nmap_results.txt',
                'content': 'Port 80: http\nPort 443: https\nSSL/TLS: TLSv1.2, TLSv1.3'
            }
        ]
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")


# Example 2: Multiple Domains
def example_2_multiple_domains():
    """Process multiple domains"""
    print("\n" + "="*70)
    print("Example 2: Multiple Domains")
    print("="*70)
    
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    domains = ['example.com', 'test.com', 'sample.com']
    
    for domain in domains:
        payload = {
            'target_domain': domain,
            'files': [
                {
                    'name': f'{domain}_results.txt',
                    'content': f'Scan results for {domain}'
                }
            ]
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            print(f"{domain}: {response.status_code}")
        except Exception as e:
            print(f"{domain}: Error - {e}")


# Example 3: Full Pipeline
def example_3_full_pipeline():
    """Run full recon pipeline"""
    print("\n" + "="*70)
    print("Example 3: Full Pipeline")
    print("="*70)
    
    try:
        from recon_automation_bot import ReconAutomationBot
        
        bot = ReconAutomationBot()
        results = bot.run_full_pipeline('example.com')
        
        print(json.dumps(results, indent=2, default=str))
    except ImportError:
        print("Error: recon_automation_bot module not available")


# Example 4: Custom Analysis Prompt
def example_4_custom_analysis():
    """Send custom analysis request"""
    print("\n" + "="*70)
    print("Example 4: Custom Analysis Prompt")
    print("="*70)
    
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    
    payload = {
        'target_domain': 'example.com',
        'analysis_type': 'vulnerability_assessment',
        'files': [
            {
                'name': 'scan_results.json',
                'content': json.dumps({
                    'open_ports': [80, 443, 8080],
                    'services': ['http', 'https', 'http-alt'],
                    'ssl_version': 'TLSv1.2',
                    'vulnerabilities': ['CVE-2021-1234']
                })
            }
        ]
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")


# Example 5: Batch Processing with Delay
def example_5_batch_processing():
    """Process multiple domains with delay"""
    print("\n" + "="*70)
    print("Example 5: Batch Processing")
    print("="*70)
    
    import time
    
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    domains = ['example.com', 'test.com', 'sample.com']
    
    for i, domain in enumerate(domains, 1):
        payload = {
            'target_domain': domain,
            'batch_number': i,
            'total_batches': len(domains),
            'files': [
                {
                    'name': f'{domain}_batch_{i}.txt',
                    'content': f'Batch {i} of {len(domains)}: {domain}'
                }
            ]
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            print(f"[{i}/{len(domains)}] {domain}: {response.status_code}")
            
            if i < len(domains):
                time.sleep(5)  # Wait 5 seconds between requests
        except Exception as e:
            print(f"[{i}/{len(domains)}] {domain}: Error - {e}")


# Example 6: Error Handling
def example_6_error_handling():
    """Demonstrate error handling"""
    print("\n" + "="*70)
    print("Example 6: Error Handling")
    print("="*70)
    
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    
    if not webhook_url:
        print("Error: MAKE_WEBHOOK_URL not configured")
        return
    
    # Test with invalid data
    test_cases = [
        {'target_domain': 'example.com', 'files': []},  # Empty files
        {'target_domain': '', 'files': [{'name': 'test.txt', 'content': 'test'}]},  # Empty domain
        {'files': [{'name': 'test.txt', 'content': 'test'}]},  # Missing domain
    ]
    
    for i, payload in enumerate(test_cases, 1):
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            print(f"Test {i}: {response.status_code}")
        except Exception as e:
            print(f"Test {i}: Error - {e}")


# Example 7: Response Processing
def example_7_response_processing():
    """Process webhook response"""
    print("\n" + "="*70)
    print("Example 7: Response Processing")
    print("="*70)
    
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    
    payload = {
        'target_domain': 'example.com',
        'files': [
            {
                'name': 'results.txt',
                'content': 'Sample recon results'
            }
        ]
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract document info
            if 'document' in data:
                doc = data['document']
                print(f"Document ID: {doc.get('documentId')}")
                print(f"Title: {doc.get('title')}")
                print(f"Created: {doc.get('created_at')}")
            
            # Extract analysis
            if 'analysis' in data:
                print(f"\nAnalysis Preview:")
                print(data['analysis'][:500] + "...")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")


# Example 8: Scheduled Execution
def example_8_scheduled_execution():
    """Schedule periodic scans"""
    print("\n" + "="*70)
    print("Example 8: Scheduled Execution")
    print("="*70)
    
    try:
        import schedule
        import time
        
        def scheduled_scan():
            from recon_automation_bot import ReconAutomationBot
            bot = ReconAutomationBot()
            results = bot.run_full_pipeline('example.com')
            print(f"Scan completed: {results['status']}")
        
        # Schedule daily scan at 2 AM
        schedule.every().day.at("02:00").do(scheduled_scan)
        
        print("Scheduled daily scan at 02:00")
        print("To run scheduler: schedule.run_pending()")
    except ImportError:
        print("Error: schedule module not installed")
        print("Install with: pip install schedule")


# Example 9: Parallel Processing
def example_9_parallel_processing():
    """Process multiple domains in parallel"""
    print("\n" + "="*70)
    print("Example 9: Parallel Processing")
    print("="*70)
    
    from concurrent.futures import ThreadPoolExecutor
    import time
    
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    domains = ['example.com', 'test.com', 'sample.com']
    
    def send_domain(domain):
        payload = {
            'target_domain': domain,
            'files': [
                {
                    'name': f'{domain}_results.txt',
                    'content': f'Results for {domain}'
                }
            ]
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            return (domain, response.status_code)
        except Exception as e:
            return (domain, f"Error: {e}")
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(send_domain, domains))
    
    for domain, status in results:
        print(f"{domain}: {status}")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("MAKE.COM INTEGRATION EXAMPLES")
    print("="*70)
    
    examples = [
        ("1", "Basic Webhook Send", example_1_basic_webhook),
        ("2", "Multiple Domains", example_2_multiple_domains),
        ("3", "Full Pipeline", example_3_full_pipeline),
        ("4", "Custom Analysis", example_4_custom_analysis),
        ("5", "Batch Processing", example_5_batch_processing),
        ("6", "Error Handling", example_6_error_handling),
        ("7", "Response Processing", example_7_response_processing),
        ("8", "Scheduled Execution", example_8_scheduled_execution),
        ("9", "Parallel Processing", example_9_parallel_processing),
    ]
    
    print("\nAvailable Examples:")
    for num, name, _ in examples:
        print(f"  {num}. {name}")
    
    choice = input("\nSelect example (1-9) or 'all': ").strip()
    
    if choice == 'all':
        for num, name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"Error in example {num}: {e}")
    else:
        for num, name, func in examples:
            if num == choice:
                func()
                break


if __name__ == "__main__":
    main()

