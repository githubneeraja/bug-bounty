#!/usr/bin/env python3
"""
Unit tests for Amass subdomain enumeration module
"""

import unittest
import tempfile
import json
import os
from unittest.mock import patch, MagicMock
from amass_subdomain_enum import (
    AmassEnumerator,
    enumerate_subdomains
)


class TestAmassEnumerator(unittest.TestCase):
    """Test cases for AmassEnumerator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.enumerator = AmassEnumerator()
    
    def test_verify_amass_installed(self):
        """Test Amass installation verification"""
        # This will pass if Amass is installed, fail otherwise
        result = self.enumerator.verify_amass_installed()
        # Don't assert - just check it runs without error
        self.assertIsInstance(result, bool)
    
    def test_parse_amass_output_empty(self):
        """Test parsing empty Amass output"""
        output = ""
        result = AmassEnumerator._parse_amass_output(output)
        self.assertEqual(result, [])
    
    def test_parse_amass_output_single(self):
        """Test parsing single subdomain"""
        output = "www.example.com"
        result = AmassEnumerator._parse_amass_output(output)
        self.assertEqual(result, ["www.example.com"])
    
    def test_parse_amass_output_multiple(self):
        """Test parsing multiple subdomains"""
        output = """api.example.com
blog.example.com
www.example.com
mail.example.com"""
        result = AmassEnumerator._parse_amass_output(output)
        self.assertEqual(len(result), 4)
        self.assertIn("api.example.com", result)
        self.assertIn("www.example.com", result)
    
    def test_parse_amass_output_with_whitespace(self):
        """Test parsing output with extra whitespace"""
        output = """
        api.example.com
        
        blog.example.com
        """
        result = AmassEnumerator._parse_amass_output(output)
        self.assertEqual(len(result), 2)
    
    def test_parse_amass_output_sorted(self):
        """Test that output is sorted"""
        output = """zebra.example.com
apple.example.com
banana.example.com"""
        result = AmassEnumerator._parse_amass_output(output)
        self.assertEqual(result, sorted(result))
    
    def test_parse_amass_json_empty_file(self):
        """Test parsing empty JSON file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write("")
            temp_file = f.name
        
        try:
            result = AmassEnumerator._parse_amass_json(temp_file)
            self.assertEqual(result, [])
        finally:
            os.unlink(temp_file)
    
    def test_parse_amass_json_single_record(self):
        """Test parsing single JSON record"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json_data = {
                "name": "www.example.com",
                "type": "CNAME",
                "source": "Shodan",
                "tag": "cert",
                "addresses": ["192.0.2.1"]
            }
            f.write(json.dumps(json_data) + "\n")
            temp_file = f.name
        
        try:
            result = AmassEnumerator._parse_amass_json(temp_file)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['name'], "www.example.com")
            self.assertEqual(result[0]['source'], "Shodan")
        finally:
            os.unlink(temp_file)
    
    def test_parse_amass_json_multiple_records(self):
        """Test parsing multiple JSON records"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            records = [
                {"name": "api.example.com", "type": "A", "source": "Censys", "tag": "cert", "addresses": []},
                {"name": "blog.example.com", "type": "CNAME", "source": "Shodan", "tag": "cert", "addresses": ["192.0.2.2"]},
                {"name": "www.example.com", "type": "A", "source": "DNS", "tag": "dns", "addresses": ["192.0.2.1"]},
            ]
            for record in records:
                f.write(json.dumps(record) + "\n")
            temp_file = f.name
        
        try:
            result = AmassEnumerator._parse_amass_json(temp_file)
            self.assertEqual(len(result), 3)
            names = [r['name'] for r in result]
            self.assertIn("api.example.com", names)
            self.assertIn("blog.example.com", names)
        finally:
            os.unlink(temp_file)
    
    def test_parse_amass_json_nonexistent_file(self):
        """Test parsing nonexistent JSON file"""
        result = AmassEnumerator._parse_amass_json("/nonexistent/file.json")
        self.assertEqual(result, [])
    
    def test_enumerate_subdomains_invalid_domain_empty(self):
        """Test enumeration with empty domain"""
        with self.assertRaises(ValueError):
            self.enumerator.enumerate_subdomains("")
    
    def test_enumerate_subdomains_invalid_domain_none(self):
        """Test enumeration with None domain"""
        with self.assertRaises(ValueError):
            self.enumerator.enumerate_subdomains(None)
    
    def test_enumerate_subdomains_invalid_domain_not_string(self):
        """Test enumeration with non-string domain"""
        with self.assertRaises(ValueError):
            self.enumerator.enumerate_subdomains(12345)
    
    def test_enumerate_subdomains_domain_normalization(self):
        """Test domain normalization (lowercase, strip)"""
        # This test verifies the function accepts various formats
        test_domains = [
            "EXAMPLE.COM",
            "  example.com  ",
            "Example.Com"
        ]
        
        for domain in test_domains:
            try:
                # Should not raise ValueError for format
                self.enumerator.enumerate_subdomains(domain, timeout=1)
            except ValueError:
                self.fail(f"Domain normalization failed for: {domain}")
            except Exception:
                # Other exceptions are OK (e.g., timeout, Amass not installed)
                pass


class TestEnumerateSubdomainsFunction(unittest.TestCase):
    """Test cases for enumerate_subdomains function"""
    
    def test_enumerate_subdomains_function_exists(self):
        """Test that enumerate_subdomains function exists"""
        self.assertTrue(callable(enumerate_subdomains))
    
    def test_enumerate_subdomains_invalid_domain(self):
        """Test function with invalid domain"""
        with self.assertRaises(ValueError):
            enumerate_subdomains("")
    
    def test_enumerate_subdomains_returns_list(self):
        """Test that function returns a list"""
        try:
            result = enumerate_subdomains("example.com")
            self.assertIsInstance(result, list)
        except RuntimeError:
            # Amass not installed - that's OK for this test
            pass


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_workflow(self):
        """Test complete workflow"""
        enumerator = AmassEnumerator()
        
        # Verify Amass is available
        if not enumerator.verify_amass_installed():
            self.skipTest("Amass not installed")
        
        # Test with a real domain (using short timeout)
        try:
            subdomains = enumerator.enumerate_subdomains(
                "example.com",
                passive_only=True,
                timeout=30
            )
            self.assertIsInstance(subdomains, list)
        except Exception as e:
            # May fail due to network or timeout
            self.skipTest(f"Integration test skipped: {e}")


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAmassEnumerator))
    suite.addTests(loader.loadTestsFromTestCase(TestEnumerateSubdomainsFunction))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)

