#!/usr/bin/env python3
"""
Unit tests for Nmap scanner module
"""

import unittest
import os
from unittest.mock import patch, MagicMock
from nmap_scanner import NmapScanner, scan_target, save_results


class TestNmapScanner(unittest.TestCase):
    """Test cases for NmapScanner class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scanner = None
    
    def test_docker_verification(self):
        """Test Docker verification"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="Docker version 20.10.0"
            )
            
            scanner = NmapScanner()
            self.assertIsNotNone(scanner)
    
    def test_docker_not_available(self):
        """Test Docker not available"""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = FileNotFoundError()
            
            with self.assertRaises(RuntimeError):
                NmapScanner()
    
    def test_port_scan_basic(self):
        """Test basic port scan"""
        with patch.object(NmapScanner, 'verify_docker'):
            with patch.object(NmapScanner, 'run_docker_nmap') as mock_run:
                mock_run.return_value = (
                    """<?xml version="1.0"?>
                    <nmaprun>
                    <host>
                    <ports>
                    <port protocol="tcp" portid="80"><state state="open"/><service name="http"/></port>
                    <port protocol="tcp" portid="443"><state state="open"/><service name="https"/></port>
                    <port protocol="tcp" portid="22"><state state="closed"/></port>
                    </ports>
                    </host>
                    </nmaprun>""",
                    "",
                    0
                )
                
                scanner = NmapScanner()
                results = scanner.port_scan("example.com")
                
                self.assertEqual(results['target'], "example.com")
                self.assertEqual(len(results['open_ports']), 2)
                self.assertIn(80, results['open_ports'])
                self.assertIn(443, results['open_ports'])
    
    def test_port_scan_with_custom_ports(self):
        """Test port scan with custom port range"""
        with patch.object(NmapScanner, 'verify_docker'):
            with patch.object(NmapScanner, 'run_docker_nmap') as mock_run:
                mock_run.return_value = ("", "", 0)
                
                scanner = NmapScanner()
                scanner.port_scan("example.com", ports="80,443,8080")
                
                # Verify correct arguments were passed
                call_args = mock_run.call_args[0][0]
                self.assertIn("-p", call_args)
                self.assertIn("80,443,8080", call_args)
    
    def test_ssl_tls_scan(self):
        """Test SSL/TLS scan"""
        with patch.object(NmapScanner, 'verify_docker'):
            with patch.object(NmapScanner, 'run_docker_nmap') as mock_run:
                mock_run.return_value = (
                    """<?xml version="1.0"?>
                    <nmaprun>
                    <host>
                    <ports>
                    <port protocol="tcp" portid="443">
                    <state state="open"/>
                    <service name="https"/>
                    </port>
                    </ports>
                    </host>
                    </nmaprun>
                    Subject: CN=example.com
                    Issuer: CN=Let's Encrypt
                    TLSv1.2 AES_256_GCM_SHA384
                    TLSv1.3 CHACHA20_POLY1305_SHA256""",
                    "",
                    0
                )
                
                scanner = NmapScanner()
                results = scanner.ssl_tls_scan("example.com", port=443)
                
                self.assertEqual(results['target'], "example.com")
                self.assertEqual(results['port'], 443)
                self.assertTrue(results['ssl_enabled'])
    
    def test_full_scan(self):
        """Test full scan (port + SSL/TLS)"""
        with patch.object(NmapScanner, 'verify_docker'):
            with patch.object(NmapScanner, 'port_scan') as mock_port:
                with patch.object(NmapScanner, 'ssl_tls_scan') as mock_ssl:
                    mock_port.return_value = {
                        'target': 'example.com',
                        'open_ports': [80, 443],
                        'services': {80: 'http', 443: 'https'}
                    }
                    mock_ssl.return_value = {
                        'target': 'example.com',
                        'ssl_enabled': True,
                        'protocols': ['TLSv1.2', 'TLSv1.3']
                    }
                    
                    scanner = NmapScanner()
                    results = scanner.full_scan("example.com")
                    
                    self.assertEqual(results['target'], "example.com")
                    self.assertIsNotNone(results['port_scan'])
                    self.assertIsNotNone(results['ssl_scan'])
    
    def test_port_scan_timeout(self):
        """Test port scan timeout"""
        with patch.object(NmapScanner, 'verify_docker'):
            with patch.object(NmapScanner, 'run_docker_nmap') as mock_run:
                import subprocess
                mock_run.side_effect = subprocess.TimeoutExpired("cmd", 300)
                
                scanner = NmapScanner()
                with self.assertRaises(RuntimeError):
                    scanner.port_scan("example.com")
    
    def test_port_scan_error(self):
        """Test port scan error handling"""
        with patch.object(NmapScanner, 'verify_docker'):
            with patch.object(NmapScanner, 'run_docker_nmap') as mock_run:
                mock_run.return_value = ("", "Error: Invalid target", 2)
                
                scanner = NmapScanner()
                with self.assertRaises(RuntimeError):
                    scanner.port_scan("example.com")
    
    def test_parse_port_scan_empty(self):
        """Test parsing empty port scan results"""
        with patch.object(NmapScanner, 'verify_docker'):
            scanner = NmapScanner()
            results = scanner._parse_port_scan("", "example.com")
            
            self.assertEqual(results['target'], "example.com")
            self.assertEqual(len(results['open_ports']), 0)
    
    def test_parse_ssl_scan_empty(self):
        """Test parsing empty SSL scan results"""
        with patch.object(NmapScanner, 'verify_docker'):
            scanner = NmapScanner()
            results = scanner._parse_ssl_scan("", "example.com", 443)
            
            self.assertEqual(results['target'], "example.com")
            self.assertFalse(results['ssl_enabled'])


class TestScanTarget(unittest.TestCase):
    """Test cases for scan_target function"""
    
    def test_scan_target_basic(self):
        """Test basic scan_target function"""
        with patch('nmap_scanner.NmapScanner') as mock_scanner_class:
            mock_scanner = MagicMock()
            mock_scanner_class.return_value = mock_scanner
            mock_scanner.full_scan.return_value = {
                'target': 'example.com',
                'port_scan': {'open_ports': [80, 443]},
                'ssl_scan': {'ssl_enabled': True},
                'errors': []
            }
            
            results = scan_target("example.com")
            
            self.assertEqual(results['target'], "example.com")
            mock_scanner.full_scan.assert_called_once()
    
    def test_scan_target_with_output_file(self):
        """Test scan_target with output file"""
        with patch('nmap_scanner.NmapScanner') as mock_scanner_class:
            with patch('nmap_scanner.save_results') as mock_save:
                mock_scanner = MagicMock()
                mock_scanner_class.return_value = mock_scanner
                mock_scanner.full_scan.return_value = {
                    'target': 'example.com',
                    'errors': []
                }
                
                results = scan_target("example.com", output_file="results.txt")
                
                mock_save.assert_called_once()


class TestSaveResults(unittest.TestCase):
    """Test cases for save_results function"""
    
    def test_save_results_basic(self):
        """Test saving results to file"""
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name
        
        try:
            results = {
                'target': 'example.com',
                'timestamp': '2025-10-26T10:00:00',
                'port_scan': {
                    'open_ports': [80, 443],
                    'closed_ports': [],
                    'filtered_ports': [],
                    'services': {80: 'http', 443: 'https'}
                },
                'ssl_scan': {
                    'ssl_enabled': True,
                    'certificate_info': {'subject': 'CN=example.com'},
                    'protocols': ['TLSv1.2'],
                    'ciphers': ['AES_256_GCM_SHA384']
                },
                'errors': []
            }
            
            save_results(results, temp_file)
            
            # Verify file was created and contains expected content
            with open(temp_file, 'r') as f:
                content = f.read()
                self.assertIn('NMAP SCAN RESULTS', content)
                self.assertIn('example.com', content)
                self.assertIn('80', content)
                self.assertIn('443', content)
        
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_save_results_creates_directory(self):
        """Test that save_results creates output directory"""
        import tempfile
        import shutil
        
        temp_dir = tempfile.mkdtemp()
        output_file = os.path.join(temp_dir, "subdir", "results.txt")
        
        try:
            results = {
                'target': 'example.com',
                'timestamp': '2025-10-26T10:00:00',
                'port_scan': None,
                'ssl_scan': None,
                'errors': []
            }
            
            save_results(results, output_file)
            
            self.assertTrue(os.path.exists(output_file))
        
        finally:
            shutil.rmtree(temp_dir)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestNmapScanner))
    suite.addTests(loader.loadTestsFromTestCase(TestScanTarget))
    suite.addTests(loader.loadTestsFromTestCase(TestSaveResults))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)

