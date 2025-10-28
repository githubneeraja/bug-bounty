#!/usr/bin/env python3
"""
Make.com Webhook Test Script
Tests the connection to Make.com webhook and verifies the integration
"""

import requests
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def print_success(message):
    """Print success message"""
    print(f"✅ {message}")


def print_error(message):
    """Print error message"""
    print(f"❌ {message}")


def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")


def test_environment():
    """Test environment configuration"""
    print_header("Step 1: Environment Configuration Check")
    
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    gemini_key = os.getenv('GEMINI_API_KEY')
    google_key = os.getenv('GOOGLE_API_KEY')
    shodan_key = os.getenv('SHODAN_API_KEY')
    
    if not webhook_url:
        print_error("MAKE_WEBHOOK_URL not configured")
        print_info("Please set MAKE_WEBHOOK_URL in .env file")
        return False
    
    print_success(f"MAKE_WEBHOOK_URL configured: {webhook_url[:50]}...")
    
    if gemini_key:
        print_success(f"GEMINI_API_KEY configured: {gemini_key[:20]}...")
    else:
        print_error("GEMINI_API_KEY not configured (optional for basic test)")
    
    if google_key:
        print_success(f"GOOGLE_API_KEY configured: {google_key[:20]}...")
    else:
        print_error("GOOGLE_API_KEY not configured (optional for basic test)")
    
    if shodan_key:
        print_success(f"SHODAN_API_KEY configured: {shodan_key[:20]}...")
    else:
        print_error("SHODAN_API_KEY not configured (optional for basic test)")
    
    return True


def test_basic_webhook():
    """Test basic webhook connection"""
    print_header("Step 2: Basic Webhook Connection Test")
    
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    
    if not webhook_url:
        print_error("MAKE_WEBHOOK_URL not configured")
        return False
    
    payload = {
        'target_domain': 'example.com',
        'test': True,
        'timestamp': datetime.now().isoformat()
    }
    
    print_info(f"Sending test payload to: {webhook_url}")
    print_info(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        print_success(f"HTTP Status: {response.status_code}")
        
        if response.status_code in [200, 202, 204]:
            print_success("Webhook received successfully!")
            
            try:
                response_data = response.json()
                print_success(f"Response: {json.dumps(response_data, indent=2)}")
            except:
                print_info(f"Response text: {response.text}")
            
            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
    
    except requests.exceptions.Timeout:
        print_error("Request timeout - webhook may not be responding")
        return False
    except requests.exceptions.ConnectionError:
        print_error("Connection error - webhook URL may be invalid")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_with_files():
    """Test webhook with recon files"""
    print_header("Step 3: Webhook Test with Recon Files")
    
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    
    if not webhook_url:
        print_error("MAKE_WEBHOOK_URL not configured")
        return False
    
    payload = {
        'target_domain': 'example.com',
        'files': [
            {
                'name': 'amass_results.txt',
                'content': '''example.com
www.example.com
api.example.com
mail.example.com
admin.example.com'''
            },
            {
                'name': 'shodan_results.json',
                'content': json.dumps({
                    'example.com': {
                        'ip': '93.184.216.34',
                        'ports': [80, 443],
                        'services': ['http', 'https'],
                        'organization': 'IANA',
                        'country': 'US'
                    }
                })
            },
            {
                'name': 'nmap_results.txt',
                'content': '''Port 80: http (Apache 2.4.41)
Port 443: https (Apache 2.4.41)
SSL/TLS: TLSv1.2, TLSv1.3
Ciphers: TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384'''
            }
        ],
        'timestamp': datetime.now().isoformat()
    }
    
    print_info(f"Sending recon files to: {webhook_url}")
    print_info(f"Files: {len(payload['files'])} files")
    for file in payload['files']:
        print_info(f"  - {file['name']} ({len(file['content'])} bytes)")
    
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        print_success(f"HTTP Status: {response.status_code}")
        
        if response.status_code in [200, 202, 204]:
            print_success("Webhook received files successfully!")
            
            try:
                response_data = response.json()
                print_success(f"Response: {json.dumps(response_data, indent=2)}")
                
                # Check for document URL
                if 'document' in response_data:
                    doc_url = response_data['document'].get('webViewLink')
                    if doc_url:
                        print_success(f"Google Doc created: {doc_url}")
            except:
                print_info(f"Response text: {response.text}")
            
            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
    
    except requests.exceptions.Timeout:
        print_error("Request timeout - webhook may be processing")
        print_info("Check Make.com execution history for results")
        return False
    except requests.exceptions.ConnectionError:
        print_error("Connection error - webhook URL may be invalid")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_error_handling():
    """Test webhook error handling"""
    print_header("Step 4: Error Handling Test")
    
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    
    if not webhook_url:
        print_error("MAKE_WEBHOOK_URL not configured")
        return False
    
    test_cases = [
        {
            'name': 'Empty files',
            'payload': {'target_domain': 'example.com', 'files': []}
        },
        {
            'name': 'Missing domain',
            'payload': {'files': [{'name': 'test.txt', 'content': 'test'}]}
        },
        {
            'name': 'Invalid JSON',
            'payload': None
        }
    ]
    
    for test_case in test_cases:
        print_info(f"Testing: {test_case['name']}")
        
        try:
            if test_case['payload'] is None:
                response = requests.post(
                    webhook_url,
                    data='invalid json',
                    timeout=10,
                    headers={'Content-Type': 'application/json'}
                )
            else:
                response = requests.post(
                    webhook_url,
                    json=test_case['payload'],
                    timeout=10,
                    headers={'Content-Type': 'application/json'}
                )
            
            print_info(f"  Status: {response.status_code}")
        except Exception as e:
            print_info(f"  Error: {str(e)[:50]}")
    
    return True


def test_performance():
    """Test webhook performance"""
    print_header("Step 5: Performance Test")
    
    webhook_url = os.getenv('MAKE_WEBHOOK_URL')
    
    if not webhook_url:
        print_error("MAKE_WEBHOOK_URL not configured")
        return False
    
    import time
    
    payload = {
        'target_domain': 'example.com',
        'files': [
            {
                'name': 'results.txt',
                'content': 'Sample recon results' * 100
            }
        ]
    }
    
    print_info("Measuring webhook response time...")
    
    try:
        start_time = time.time()
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        elapsed_time = time.time() - start_time
        
        print_success(f"Response time: {elapsed_time:.2f} seconds")
        print_success(f"HTTP Status: {response.status_code}")
        
        if elapsed_time < 5:
            print_success("Excellent response time!")
        elif elapsed_time < 10:
            print_info("Good response time")
        else:
            print_info("Webhook may be processing asynchronously")
        
        return True
    
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def generate_env_template():
    """Generate .env template"""
    print_header("Environment Configuration Template")
    
    template = """# Make.com Webhook Configuration
MAKE_WEBHOOK_URL=https://hook.make.com/your_webhook_id

# Google APIs
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CREDENTIALS_FILE=google_credentials.json

# Recon Tools
SHODAN_API_KEY=your_shodan_api_key
CENSYS_API_ID=your_censys_id
CENSYS_API_SECRET=your_censys_secret
"""
    
    print(template)
    print_info("Save this as .env file in the project root")


def main():
    """Run all tests"""
    print_header("MAKE.COM WEBHOOK TEST SUITE")
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print_error(".env file not found!")
        print_info("Creating .env template...")
        generate_env_template()
        print_error("Please configure .env file and run again")
        return False
    
    results = []
    
    # Run tests
    results.append(("Environment Check", test_environment()))
    
    if results[0][1]:  # Only continue if environment is OK
        results.append(("Basic Webhook", test_basic_webhook()))
        results.append(("Webhook with Files", test_with_files()))
        results.append(("Error Handling", test_error_handling()))
        results.append(("Performance", test_performance()))
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print_info(f"Passed: {passed}/{total}")
    
    if passed == total:
        print_success("All tests passed!")
        return True
    else:
        print_error(f"{total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

