#!/usr/bin/env python3
"""
Shodan Scanner Module
Provides functionality to scan subdomains using Shodan API
"""

import shodan
import socket
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class ShodanScanner:
    """Class to handle Shodan API scanning"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Shodan scanner
        
        Args:
            api_key: Shodan API key (default: from SHODAN_API_KEY env var)
        
        Raises:
            ValueError: If API key is not provided or invalid
        """
        self.api_key = api_key or os.getenv('SHODAN_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Shodan API key not provided. "
                "Set SHODAN_API_KEY environment variable or pass api_key parameter."
            )
        
        try:
            self.client = shodan.Shodan(self.api_key)
            self.verify_api_key()
        except shodan.APIError as e:
            raise ValueError(f"Invalid Shodan API key: {e}")
    
    def verify_api_key(self) -> bool:
        """
        Verify that the Shodan API key is valid
        
        Returns:
            bool: True if API key is valid
        
        Raises:
            ValueError: If API key is invalid
        """
        try:
            info = self.client.info()
            logger.info(f"✓ Shodan API key verified")
            logger.info(f"  Query credits: {info.get('query_credits', 'N/A')}")
            logger.info(f"  Scan credits: {info.get('scan_credits', 'N/A')}")
            return True
        except shodan.APIError as e:
            logger.error(f"✗ Shodan API key verification failed: {e}")
            raise ValueError(f"Invalid Shodan API key: {e}")
    
    def resolve_subdomain(self, subdomain: str) -> Optional[str]:
        """
        Resolve subdomain to IP address
        
        Args:
            subdomain: Subdomain to resolve
        
        Returns:
            IP address or None if resolution fails
        """
        try:
            ip = socket.gethostbyname(subdomain)
            logger.debug(f"Resolved {subdomain} -> {ip}")
            return ip
        except socket.gaierror:
            logger.warning(f"Could not resolve {subdomain}")
            return None
        except Exception as e:
            logger.error(f"Error resolving {subdomain}: {e}")
            return None
    
    def scan_ip(self, ip: str) -> Dict[str, Any]:
        """
        Scan an IP address using Shodan
        
        Args:
            ip: IP address to scan
        
        Returns:
            Dictionary with Shodan data
        
        Raises:
            shodan.APIError: If Shodan API call fails
        """
        try:
            host = self.client.host(ip)
            
            # Extract relevant information
            result = {
                'ip': ip,
                'country': host.get('country_name', 'Unknown'),
                'country_code': host.get('country_code', 'N/A'),
                'city': host.get('city', 'Unknown'),
                'latitude': host.get('latitude'),
                'longitude': host.get('longitude'),
                'organization': host.get('org', 'Unknown'),
                'isp': host.get('isp', 'Unknown'),
                'ports': host.get('ports', []),
                'services': [],
                'vulnerabilities': host.get('vulns', []),
                'hostnames': host.get('hostnames', []),
                'last_update': host.get('last_update', 'N/A'),
                'os': host.get('os'),
                'tags': host.get('tags', []),
                'raw_data': host
            }
            
            # Extract service information
            if 'data' in host:
                for service in host['data']:
                    service_info = {
                        'port': service.get('port'),
                        'protocol': service.get('_shodan', {}).get('module', 'unknown'),
                        'banner': service.get('data', ''),
                        'timestamp': service.get('timestamp'),
                        'ssl': service.get('ssl'),
                        'http': service.get('http'),
                        'product': service.get('product'),
                        'version': service.get('version'),
                        'cpe': service.get('cpe'),
                    }
                    result['services'].append(service_info)
            
            logger.info(f"✓ Scanned {ip}: Found {len(result['services'])} services")
            return result
        
        except shodan.APIError as e:
            logger.error(f"Shodan API error for {ip}: {e}")
            return {
                'ip': ip,
                'error': str(e),
                'services': [],
                'vulnerabilities': []
            }
        except Exception as e:
            logger.error(f"Error scanning {ip}: {e}")
            return {
                'ip': ip,
                'error': str(e),
                'services': [],
                'vulnerabilities': []
            }
    
    def scan_subdomains(
        self,
        subdomains: List[str],
        resolve_ips: bool = True
    ) -> Dict[str, Any]:
        """
        Scan multiple subdomains using Shodan
        
        Args:
            subdomains: List of subdomains to scan
            resolve_ips: Whether to resolve subdomains to IPs (default: True)
        
        Returns:
            Dictionary with results per subdomain
        """
        if not subdomains:
            raise ValueError("Subdomains list cannot be empty")
        
        logger.info(f"Starting Shodan scan for {len(subdomains)} subdomains")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_subdomains': len(subdomains),
            'scanned_subdomains': 0,
            'subdomains': {}
        }
        
        for subdomain in subdomains:
            subdomain = subdomain.strip().lower()
            logger.info(f"Scanning: {subdomain}")
            
            subdomain_result = {
                'subdomain': subdomain,
                'ip': None,
                'resolved': False,
                'scan_data': None,
                'error': None
            }
            
            try:
                # Resolve subdomain to IP
                if resolve_ips:
                    ip = self.resolve_subdomain(subdomain)
                    if ip:
                        subdomain_result['ip'] = ip
                        subdomain_result['resolved'] = True
                        
                        # Scan the IP
                        scan_data = self.scan_ip(ip)
                        subdomain_result['scan_data'] = scan_data
                        results['scanned_subdomains'] += 1
                    else:
                        subdomain_result['error'] = 'Could not resolve subdomain'
                else:
                    # Assume subdomain is an IP
                    scan_data = self.scan_ip(subdomain)
                    subdomain_result['scan_data'] = scan_data
                    subdomain_result['ip'] = subdomain
                    subdomain_result['resolved'] = True
                    results['scanned_subdomains'] += 1
            
            except Exception as e:
                subdomain_result['error'] = str(e)
                logger.error(f"Error processing {subdomain}: {e}")
            
            results['subdomains'][subdomain] = subdomain_result
        
        logger.info(f"✓ Scan complete: {results['scanned_subdomains']}/{len(subdomains)} scanned")
        return results


def scan_with_shodan(
    subdomains: List[str],
    api_key: Optional[str] = None,
    resolve_ips: bool = True
) -> Dict[str, Any]:
    """
    Scan subdomains using Shodan API
    
    This function resolves subdomains to IP addresses and retrieves
    information about services running on those IPs from Shodan.
    
    Args:
        subdomains: List of subdomains to scan
        api_key: Shodan API key (default: from SHODAN_API_KEY env var)
        resolve_ips: Whether to resolve subdomains to IPs (default: True)
    
    Returns:
        Dictionary with Shodan scan results per subdomain
    
    Raises:
        ValueError: If subdomains list is empty or API key is invalid
        shodan.APIError: If Shodan API call fails
    
    Example:
        >>> subdomains = ['api.example.com', 'www.example.com']
        >>> results = scan_with_shodan(subdomains)
        >>> for subdomain, data in results['subdomains'].items():
        ...     print(f"{subdomain}: {data['ip']}")
    """
    try:
        scanner = ShodanScanner(api_key)
        return scanner.scan_subdomains(subdomains, resolve_ips)
    except Exception as e:
        logger.error(f"Shodan scan failed: {e}")
        raise


def main():
    """Main entry point for command-line usage"""
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python shodan_scanner.py <subdomain1> [subdomain2] ...")
        print("Example: python shodan_scanner.py api.example.com www.example.com")
        print("\nNote: Set SHODAN_API_KEY environment variable first")
        sys.exit(1)
    
    subdomains = sys.argv[1:]
    
    try:
        results = scan_with_shodan(subdomains)
        
        print(f"\n{'='*70}")
        print(f"Shodan Scan Results")
        print(f"{'='*70}")
        print(f"Timestamp: {results['timestamp']}")
        print(f"Total Subdomains: {results['total_subdomains']}")
        print(f"Successfully Scanned: {results['scanned_subdomains']}\n")
        
        for subdomain, data in results['subdomains'].items():
            print(f"\n{'─'*70}")
            print(f"Subdomain: {subdomain}")
            print(f"{'─'*70}")
            
            if data['error']:
                print(f"Error: {data['error']}")
            else:
                print(f"IP Address: {data['ip']}")
                
                if data['scan_data']:
                    scan = data['scan_data']
                    print(f"Country: {scan.get('country', 'N/A')}")
                    print(f"City: {scan.get('city', 'N/A')}")
                    print(f"Organization: {scan.get('organization', 'N/A')}")
                    print(f"ISP: {scan.get('isp', 'N/A')}")
                    print(f"Ports: {', '.join(map(str, scan.get('ports', [])))}")
                    print(f"Services Found: {len(scan.get('services', []))}")
                    
                    if scan.get('services'):
                        print(f"\nServices:")
                        for service in scan['services'][:5]:
                            print(f"  • Port {service.get('port')}: {service.get('protocol', 'unknown')}")
                        
                        if len(scan['services']) > 5:
                            print(f"  ... and {len(scan['services']) - 5} more")
                    
                    if scan.get('vulnerabilities'):
                        print(f"\nVulnerabilities: {len(scan['vulnerabilities'])}")
        
        print(f"\n{'='*70}\n")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

