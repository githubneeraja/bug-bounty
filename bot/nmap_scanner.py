#!/usr/bin/env python3
"""
Nmap Scanner Module
Performs port scans and SSL/TLS analysis via Docker
"""

import subprocess
import json
import logging
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NmapScanner:
    """Class to handle Nmap scanning via Docker"""
    
    def __init__(self, docker_image: str = "nmap/nmap:latest"):
        """
        Initialize Nmap scanner
        
        Args:
            docker_image: Docker image to use for Nmap (default: nmap/nmap:latest)
        """
        self.docker_image = docker_image
        self.verify_docker()
    
    def verify_docker(self) -> bool:
        """
        Verify Docker is installed and running
        
        Returns:
            bool: True if Docker is available
        
        Raises:
            RuntimeError: If Docker is not available
        """
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"✓ Docker available: {result.stdout.strip()}")
                return True
            else:
                raise RuntimeError("Docker not available")
        except FileNotFoundError:
            raise RuntimeError("Docker not installed. Please install Docker first.")
        except Exception as e:
            raise RuntimeError(f"Docker verification failed: {e}")
    
    def run_docker_nmap(self, args: List[str]) -> Tuple[str, str, int]:
        """
        Run Nmap command via Docker
        
        Args:
            args: Nmap command arguments
        
        Returns:
            Tuple of (stdout, stderr, return_code)
        """
        try:
            cmd = ["docker", "run", "--rm", self.docker_image] + args
            logger.debug(f"Running: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return result.stdout, result.stderr, result.returncode
        
        except subprocess.TimeoutExpired:
            logger.error("Nmap scan timed out")
            raise RuntimeError("Nmap scan timed out after 300 seconds")
        except Exception as e:
            logger.error(f"Error running Docker Nmap: {e}")
            raise
    
    def port_scan(
        self,
        target: str,
        ports: str = "1-1000",
        service_detection: bool = True
    ) -> Dict[str, Any]:
        """
        Perform port scan on target
        
        Args:
            target: Target domain or IP
            ports: Port range to scan (default: 1-1000)
            service_detection: Enable service version detection
        
        Returns:
            Dictionary with scan results
        """
        logger.info(f"Starting port scan on {target} (ports: {ports})")
        
        try:
            # Build Nmap command
            args = [
                "nmap",
                "-p", ports,
                "-sV" if service_detection else "-sS",
                "-oX", "-",  # Output XML to stdout
                target
            ]
            
            stdout, stderr, returncode = self.run_docker_nmap(args)
            
            if returncode != 0 and returncode != 1:
                logger.error(f"Nmap error: {stderr}")
                raise RuntimeError(f"Nmap scan failed: {stderr}")
            
            # Parse results
            results = self._parse_port_scan(stdout, target)
            logger.info(f"✓ Port scan complete: {len(results['open_ports'])} open ports found")
            
            return results
        
        except Exception as e:
            logger.error(f"Port scan failed: {e}")
            raise
    
    def ssl_tls_scan(self, target: str, port: int = 443) -> Dict[str, Any]:
        """
        Perform SSL/TLS analysis on target
        
        Args:
            target: Target domain or IP
            port: Port to scan (default: 443)
        
        Returns:
            Dictionary with SSL/TLS analysis results
        """
        logger.info(f"Starting SSL/TLS scan on {target}:{port}")
        
        try:
            # Build Nmap command for SSL/TLS
            args = [
                "nmap",
                "-p", str(port),
                "--script", "ssl-enum-ciphers,ssl-cert",
                "-sV",
                "-oX", "-",
                target
            ]
            
            stdout, stderr, returncode = self.run_docker_nmap(args)
            
            if returncode != 0 and returncode != 1:
                logger.error(f"Nmap error: {stderr}")
                raise RuntimeError(f"SSL/TLS scan failed: {stderr}")
            
            # Parse results
            results = self._parse_ssl_scan(stdout, target, port)
            logger.info(f"✓ SSL/TLS scan complete")
            
            return results
        
        except Exception as e:
            logger.error(f"SSL/TLS scan failed: {e}")
            raise
    
    def _parse_port_scan(self, xml_output: str, target: str) -> Dict[str, Any]:
        """Parse Nmap XML port scan output"""
        results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'open_ports': [],
            'closed_ports': [],
            'filtered_ports': [],
            'services': {}
        }
        
        try:
            # Extract port information from XML
            port_pattern = r'<port protocol="tcp" portid="(\d+)"><state state="(\w+)"[^>]*>.*?</state>(?:<service name="([^"]*)"[^>]*>)?'
            
            for match in re.finditer(port_pattern, xml_output, re.DOTALL):
                port = int(match.group(1))
                state = match.group(2)
                service = match.group(3) or "unknown"
                
                port_info = {
                    'port': port,
                    'state': state,
                    'service': service
                }
                
                if state == 'open':
                    results['open_ports'].append(port)
                    results['services'][port] = service
                elif state == 'closed':
                    results['closed_ports'].append(port)
                elif state == 'filtered':
                    results['filtered_ports'].append(port)
            
            results['open_ports'].sort()
            results['closed_ports'].sort()
            results['filtered_ports'].sort()
        
        except Exception as e:
            logger.warning(f"Error parsing port scan results: {e}")
        
        return results
    
    def _parse_ssl_scan(self, xml_output: str, target: str, port: int) -> Dict[str, Any]:
        """Parse Nmap XML SSL/TLS scan output"""
        results = {
            'target': target,
            'port': port,
            'timestamp': datetime.now().isoformat(),
            'ssl_enabled': False,
            'certificate_info': {},
            'ciphers': [],
            'protocols': []
        }
        
        try:
            # Check if SSL/TLS is enabled
            if 'ssl' in xml_output.lower() or 'tls' in xml_output.lower():
                results['ssl_enabled'] = True
            
            # Extract certificate information
            cert_pattern = r'Subject: ([^\n]*)'
            cert_match = re.search(cert_pattern, xml_output)
            if cert_match:
                results['certificate_info']['subject'] = cert_match.group(1).strip()
            
            issuer_pattern = r'Issuer: ([^\n]*)'
            issuer_match = re.search(issuer_pattern, xml_output)
            if issuer_match:
                results['certificate_info']['issuer'] = issuer_match.group(1).strip()
            
            # Extract cipher information
            cipher_pattern = r'TLSv[\d.]+ ([A-Z0-9_-]+)'
            for match in re.finditer(cipher_pattern, xml_output):
                cipher = match.group(1)
                if cipher not in results['ciphers']:
                    results['ciphers'].append(cipher)
            
            # Extract protocol information
            protocol_pattern = r'(TLSv[\d.]+|SSLv[\d.]+)'
            for match in re.finditer(protocol_pattern, xml_output):
                protocol = match.group(1)
                if protocol not in results['protocols']:
                    results['protocols'].append(protocol)
        
        except Exception as e:
            logger.warning(f"Error parsing SSL/TLS scan results: {e}")
        
        return results
    
    def full_scan(
        self,
        target: str,
        ports: str = "1-1000",
        ssl_port: int = 443
    ) -> Dict[str, Any]:
        """
        Perform both port scan and SSL/TLS analysis
        
        Args:
            target: Target domain or IP
            ports: Port range for port scan
            ssl_port: Port for SSL/TLS scan
        
        Returns:
            Dictionary with combined results
        """
        logger.info(f"Starting full scan on {target}")
        
        results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'port_scan': None,
            'ssl_scan': None,
            'errors': []
        }
        
        try:
            # Port scan
            try:
                results['port_scan'] = self.port_scan(target, ports)
            except Exception as e:
                logger.error(f"Port scan error: {e}")
                results['errors'].append(f"Port scan: {str(e)}")
            
            # SSL/TLS scan
            try:
                results['ssl_scan'] = self.ssl_tls_scan(target, ssl_port)
            except Exception as e:
                logger.error(f"SSL/TLS scan error: {e}")
                results['errors'].append(f"SSL/TLS scan: {str(e)}")
        
        except Exception as e:
            logger.error(f"Full scan failed: {e}")
            results['errors'].append(f"Full scan: {str(e)}")
        
        logger.info(f"✓ Full scan complete")
        return results


def scan_target(
    target: str,
    ports: str = "1-1000",
    ssl_port: int = 443,
    output_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Scan target domain with Nmap
    
    Args:
        target: Target domain or IP
        ports: Port range to scan
        ssl_port: Port for SSL/TLS scan
        output_file: Optional file to save results
    
    Returns:
        Dictionary with scan results
    
    Raises:
        RuntimeError: If Docker is not available or scan fails
    """
    try:
        scanner = NmapScanner()
        results = scanner.full_scan(target, ports, ssl_port)
        
        if output_file:
            save_results(results, output_file)
        
        return results
    
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise


def save_results(results: Dict[str, Any], output_file: str) -> None:
    """
    Save scan results to file
    
    Args:
        results: Scan results dictionary
        output_file: Output file path
    """
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("NMAP SCAN RESULTS\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Target: {results['target']}\n")
            f.write(f"Timestamp: {results['timestamp']}\n\n")
            
            # Port scan results
            if results['port_scan']:
                f.write("PORT SCAN RESULTS\n")
                f.write("-" * 70 + "\n")
                port_scan = results['port_scan']
                f.write(f"Open Ports: {len(port_scan['open_ports'])}\n")
                if port_scan['open_ports']:
                    f.write(f"  {', '.join(map(str, port_scan['open_ports']))}\n\n")
                    f.write("Services:\n")
                    for port, service in sorted(port_scan['services'].items()):
                        f.write(f"  Port {port}: {service}\n")
                f.write(f"\nClosed Ports: {len(port_scan['closed_ports'])}\n")
                f.write(f"Filtered Ports: {len(port_scan['filtered_ports'])}\n\n")
            
            # SSL/TLS results
            if results['ssl_scan']:
                f.write("SSL/TLS ANALYSIS\n")
                f.write("-" * 70 + "\n")
                ssl_scan = results['ssl_scan']
                f.write(f"SSL/TLS Enabled: {ssl_scan['ssl_enabled']}\n")
                if ssl_scan['certificate_info']:
                    f.write("Certificate Information:\n")
                    for key, value in ssl_scan['certificate_info'].items():
                        f.write(f"  {key.capitalize()}: {value}\n")
                if ssl_scan['protocols']:
                    f.write(f"Protocols: {', '.join(ssl_scan['protocols'])}\n")
                if ssl_scan['ciphers']:
                    f.write(f"Ciphers: {len(ssl_scan['ciphers'])} found\n")
                f.write("\n")
            
            # Errors
            if results['errors']:
                f.write("ERRORS\n")
                f.write("-" * 70 + "\n")
                for error in results['errors']:
                    f.write(f"  • {error}\n")
        
        logger.info(f"✓ Results saved to {output_file}")
    
    except Exception as e:
        logger.error(f"Error saving results: {e}")
        raise


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python nmap_scanner.py <target> [output_file]")
        print("Example: python nmap_scanner.py example.com results.txt")
        sys.exit(1)
    
    target = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        results = scan_target(target, output_file=output_file)
        
        print(f"\n{'='*70}")
        print("NMAP SCAN RESULTS")
        print(f"{'='*70}")
        print(f"Target: {target}")
        
        if results['port_scan']:
            port_scan = results['port_scan']
            print(f"\nOpen Ports: {len(port_scan['open_ports'])}")
            if port_scan['open_ports']:
                print(f"  {', '.join(map(str, port_scan['open_ports']))}")
        
        if results['ssl_scan']:
            ssl_scan = results['ssl_scan']
            print(f"\nSSL/TLS Enabled: {ssl_scan['ssl_enabled']}")
        
        if results['errors']:
            print(f"\nErrors: {len(results['errors'])}")
            for error in results['errors']:
                print(f"  • {error}")
        
        print(f"\n{'='*70}\n")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

