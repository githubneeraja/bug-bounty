#!/usr/bin/env python3
"""
Unit tests for Shodan scanner module
"""

import unittest
import os
from unittest.mock import patch, MagicMock
from shodan_scanner import ShodanScanner, scan_with_shodan


class TestShodanScanner(unittest.TestCase):
    """Test cases for ShodanScanner class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.api_key = os.getenv('SHODAN_API_KEY', 'test_key')
    
    def test_init_with_api_key(self):
        """Test initialization with API key"""
        with patch('shodan_scanner.shodan.Shodan') as mock_shodan:
            mock_client = MagicMock()
            mock_shodan.return_value = mock_client
            mock_client.info.return_value = {
                'query_credits': 100,
                'scan_credits': 50
            }
            
            scanner = ShodanScanner(api_key='test_key')
            self.assertIsNotNone(scanner.client)
    
    def test_init_without_api_key(self):
        """Test initialization without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                ShodanScanner()
    
    def test_init_with_invalid_api_key(self):
        """Test initialization with invalid API key"""
        with patch('shodan_scanner.shodan.Shodan') as mock_shodan:
            mock_shodan.return_value.info.side_effect = Exception("Invalid key")
            
            with self.assertRaises(ValueError):
                ShodanScanner(api_key='invalid_key')
    
    def test_verify_api_key_valid(self):
        """Test API key verification with valid key"""
        with patch('shodan_scanner.shodan.Shodan') as mock_shodan:
            mock_client = MagicMock()
            mock_shodan.return_value = mock_client
            mock_client.info.return_value = {
                'query_credits': 100,
                'scan_credits': 50
            }
            
            scanner = ShodanScanner(api_key='test_key')
            result = scanner.verify_api_key()
            self.assertTrue(result)
    
    def test_verify_api_key_invalid(self):
        """Test API key verification with invalid key"""
        with patch('shodan_scanner.shodan.Shodan') as mock_shodan:
            mock_client = MagicMock()
            mock_shodan.return_value = mock_client
            mock_client.info.side_effect = Exception("Invalid key")
            
            with self.assertRaises(ValueError):
                scanner = ShodanScanner(api_key='invalid_key')
    
    def test_resolve_subdomain_valid(self):
        """Test subdomain resolution with valid domain"""
        with patch('shodan_scanner.shodan.Shodan') as mock_shodan:
            mock_client = MagicMock()
            mock_shodan.return_value = mock_client
            mock_client.info.return_value = {'query_credits': 100}
            
            scanner = ShodanScanner(api_key='test_key')
            
            with patch('shodan_scanner.socket.gethostbyname') as mock_resolve:
                mock_resolve.return_value = '192.0.2.1'
                
                ip = scanner.resolve_subdomain('example.com')
                self.assertEqual(ip, '192.0.2.1')
    
    def test_resolve_subdomain_invalid(self):
        """Test subdomain resolution with invalid domain"""
        with patch('shodan_scanner.shodan.Shodan') as mock_shodan:
            mock_client = MagicMock()
            mock_shodan.return_value = mock_client
            mock_client.info.return_value = {'query_credits': 100}
            
            scanner = ShodanScanner(api_key='test_key')
            
            with patch('shodan_scanner.socket.gethostbyname') as mock_resolve:
                import socket
                mock_resolve.side_effect = socket.gaierror("Name resolution failed")
                
                ip = scanner.resolve_subdomain('invalid..domain')
                self.assertIsNone(ip)
    
    def test_scan_ip_valid(self):
        """Test IP scanning with valid IP"""
        with patch('shodan_scanner.shodan.Shodan') as mock_shodan:
            mock_client = MagicMock()
            mock_shodan.return_value = mock_client
            mock_client.info.return_value = {'query_credits': 100}
            
            mock_client.host.return_value = {
                'ip_str': '192.0.2.1',
                'country_name': 'United States',
                'country_code': 'US',
                'city': 'New York',
                'latitude': 40.7128,
                'longitude': -74.0060,
                'org': 'Example Corp',
                'isp': 'Example ISP',
                'ports': [80, 443],
                'vulns': [],
                'hostnames': ['example.com'],
                'last_update': '2025-10-26',
                'os': 'Linux',
                'tags': ['web'],
                'data': []
            }
            
            scanner = ShodanScanner(api_key='test_key')
            result = scanner.scan_ip('192.0.2.1')
            
            self.assertEqual(result['ip'], '192.0.2.1')
            self.assertEqual(result['country'], 'United States')
            self.assertEqual(result['ports'], [80, 443])
    
    def test_scan_ip_with_services(self):
        """Test IP scanning with services"""
        with patch('shodan_scanner.shodan.Shodan') as mock_shodan:
            mock_client = MagicMock()
            mock_shodan.return_value = mock_client
            mock_client.info.return_value = {'query_credits': 100}
            
            mock_client.host.return_value = {
                'ip_str': '192.0.2.1',
                'country_name': 'United States',
                'ports': [80, 443],
                'vulns': [],
                'hostnames': [],
                'data': [
                    {
                        'port': 80,
                        '_shodan': {'module': 'http'},
                        'data': 'HTTP/1.1 200 OK',
                        'product': 'Apache',
                        'version': '2.4.41'
                    }
                ]
            }
            
            scanner = ShodanScanner(api_key='test_key')
            result = scanner.scan_ip('192.0.2.1')
            
            self.assertEqual(len(result['services']), 1)
            self.assertEqual(result['services'][0]['port'], 80)
    
    def test_scan_subdomains_empty_list(self):
        """Test scanning with empty subdomain list"""
        with patch('shodan_scanner.shodan.Shodan') as mock_shodan:
            mock_client = MagicMock()
            mock_shodan.return_value = mock_client
            mock_client.info.return_value = {'query_credits': 100}
            
            scanner = ShodanScanner(api_key='test_key')
            
            with self.assertRaises(ValueError):
                scanner.scan_subdomains([])
    
    def test_scan_subdomains_valid(self):
        """Test scanning with valid subdomains"""
        with patch('shodan_scanner.shodan.Shodan') as mock_shodan:
            mock_client = MagicMock()
            mock_shodan.return_value = mock_client
            mock_client.info.return_value = {'query_credits': 100}
            
            mock_client.host.return_value = {
                'ip_str': '192.0.2.1',
                'country_name': 'United States',
                'ports': [80],
                'vulns': [],
                'hostnames': [],
                'data': []
            }
            
            scanner = ShodanScanner(api_key='test_key')
            
            with patch.object(scanner, 'resolve_subdomain') as mock_resolve:
                mock_resolve.return_value = '192.0.2.1'
                
                results = scanner.scan_subdomains(['example.com'])
                
                self.assertEqual(results['total_subdomains'], 1)
                self.assertIn('example.com', results['subdomains'])


class TestScanWithShodanFunction(unittest.TestCase):
    """Test cases for scan_with_shodan function"""
    
    def test_scan_with_shodan_function_exists(self):
        """Test that scan_with_shodan function exists"""
        self.assertTrue(callable(scan_with_shodan))
    
    def test_scan_with_shodan_empty_list(self):
        """Test function with empty subdomain list"""
        with self.assertRaises(ValueError):
            scan_with_shodan([])
    
    def test_scan_with_shodan_invalid_api_key(self):
        """Test function with invalid API key"""
        with self.assertRaises(ValueError):
            scan_with_shodan(['example.com'], api_key='invalid_key')


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_workflow(self):
        """Test complete workflow"""
        with patch('shodan_scanner.shodan.Shodan') as mock_shodan:
            mock_client = MagicMock()
            mock_shodan.return_value = mock_client
            mock_client.info.return_value = {'query_credits': 100}
            
            mock_client.host.return_value = {
                'ip_str': '192.0.2.1',
                'country_name': 'United States',
                'ports': [80, 443],
                'vulns': [],
                'hostnames': [],
                'data': []
            }
            
            with patch('shodan_scanner.socket.gethostbyname') as mock_resolve:
                mock_resolve.return_value = '192.0.2.1'
                
                results = scan_with_shodan(['example.com'])
                
                self.assertIsInstance(results, dict)
                self.assertIn('subdomains', results)
                self.assertEqual(results['total_subdomains'], 1)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestShodanScanner))
    suite.addTests(loader.loadTestsFromTestCase(TestScanWithShodanFunction))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)

