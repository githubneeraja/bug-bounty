#!/usr/bin/env python3
"""
Amass Subdomain Enumeration Module
Provides functionality to enumerate subdomains using Amass in passive mode
"""

import subprocess
import json
import os
import sys
import tempfile
from typing import List, Dict, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AmassEnumerator:
    """Class to handle Amass subdomain enumeration"""
    
    def __init__(self, amass_path: str = "amass"):
        """
        Initialize the Amass enumerator
        
        Args:
            amass_path: Path to Amass executable (default: 'amass' in PATH)
        """
        self.amass_path = amass_path
        self.verify_amass_installed()
    
    def verify_amass_installed(self) -> bool:
        """
        Verify that Amass is installed and accessible
        
        Returns:
            bool: True if Amass is installed, False otherwise
        """
        try:
            result = subprocess.run(
                [self.amass_path, "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"✓ Amass found: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            logger.error(f"✗ Amass not found at: {self.amass_path}")
            logger.error("Please install Amass: https://github.com/OWASP/Amass")
            return False
        except Exception as e:
            logger.error(f"✗ Error verifying Amass: {e}")
            return False
        
        return False
    
    def enumerate_subdomains(
        self,
        domain: str,
        passive_only: bool = True,
        timeout: int = 300
    ) -> List[str]:
        """
        Enumerate subdomains for a given domain using Amass
        
        Args:
            domain: Target domain to enumerate
            passive_only: Use passive mode only (default: True)
            timeout: Command timeout in seconds (default: 300)
        
        Returns:
            List of discovered subdomains
        
        Raises:
            ValueError: If domain is invalid
            subprocess.TimeoutExpired: If command times out
            RuntimeError: If Amass execution fails
        """
        if not domain or not isinstance(domain, str):
            raise ValueError("Domain must be a non-empty string")
        
        domain = domain.strip().lower()
        logger.info(f"Starting subdomain enumeration for: {domain}")
        
        # Build Amass command
        cmd = [self.amass_path, "enum"]
        
        if passive_only:
            cmd.append("-passive")
        
        cmd.extend(["-d", domain])
        
        logger.debug(f"Executing command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Amass error: {result.stderr}")
                raise RuntimeError(f"Amass failed: {result.stderr}")
            
            # Parse output and extract subdomains
            subdomains = self._parse_amass_output(result.stdout)
            logger.info(f"✓ Found {len(subdomains)} subdomains")
            
            return subdomains
        
        except subprocess.TimeoutExpired:
            logger.error(f"Amass command timed out after {timeout} seconds")
            raise
        except Exception as e:
            logger.error(f"Error during enumeration: {e}")
            raise
    
    def enumerate_subdomains_json(
        self,
        domain: str,
        passive_only: bool = True,
        timeout: int = 300
    ) -> List[Dict]:
        """
        Enumerate subdomains and return detailed JSON data
        
        Args:
            domain: Target domain to enumerate
            passive_only: Use passive mode only (default: True)
            timeout: Command timeout in seconds (default: 300)
        
        Returns:
            List of subdomain dictionaries with metadata
        """
        if not domain or not isinstance(domain, str):
            raise ValueError("Domain must be a non-empty string")
        
        domain = domain.strip().lower()
        logger.info(f"Starting JSON enumeration for: {domain}")
        
        # Create temporary file for JSON output
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False
        ) as tmp:
            json_file = tmp.name
        
        try:
            # Build Amass command with JSON output
            cmd = [self.amass_path, "enum"]
            
            if passive_only:
                cmd.append("-passive")
            
            cmd.extend([
                "-d", domain,
                "-json", json_file
            ])
            
            logger.debug(f"Executing command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Amass error: {result.stderr}")
                raise RuntimeError(f"Amass failed: {result.stderr}")
            
            # Read and parse JSON output
            subdomains_data = self._parse_amass_json(json_file)
            logger.info(f"✓ Found {len(subdomains_data)} subdomains with metadata")
            
            return subdomains_data
        
        finally:
            # Clean up temporary file
            if os.path.exists(json_file):
                os.remove(json_file)
    
    @staticmethod
    def _parse_amass_output(output: str) -> List[str]:
        """
        Parse Amass text output and extract subdomains
        
        Args:
            output: Raw Amass output
        
        Returns:
            List of unique subdomains
        """
        subdomains = set()
        
        for line in output.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('['):
                # Amass outputs subdomains directly
                subdomains.add(line)
        
        return sorted(list(subdomains))
    
    @staticmethod
    def _parse_amass_json(json_file: str) -> List[Dict]:
        """
        Parse Amass JSON output
        
        Args:
            json_file: Path to JSON output file
        
        Returns:
            List of subdomain dictionaries
        """
        subdomains_data = []
        
        try:
            with open(json_file, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        if data.get('name'):
                            subdomains_data.append({
                                'name': data.get('name'),
                                'type': data.get('type'),
                                'source': data.get('source'),
                                'tag': data.get('tag'),
                                'addresses': data.get('addresses', [])
                            })
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            logger.warning(f"JSON file not found: {json_file}")
        
        return subdomains_data


def enumerate_subdomains(domain: str) -> List[str]:
    """
    Enumerate subdomains for a given domain using Amass in passive mode
    
    This is the main function that runs Amass in passive mode and returns
    a list of discovered subdomains.
    
    Args:
        domain: Target domain to enumerate (e.g., 'example.com')
    
    Returns:
        List of discovered subdomains
    
    Example:
        >>> subdomains = enumerate_subdomains('example.com')
        >>> print(f"Found {len(subdomains)} subdomains")
        >>> for subdomain in subdomains[:5]:
        ...     print(subdomain)
    
    Raises:
        ValueError: If domain is invalid
        RuntimeError: If Amass is not installed or execution fails
    """
    try:
        enumerator = AmassEnumerator()
        return enumerator.enumerate_subdomains(domain, passive_only=True)
    except Exception as e:
        logger.error(f"Subdomain enumeration failed: {e}")
        raise


def main():
    """Main entry point for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python amass_subdomain_enum.py <domain>")
        print("Example: python amass_subdomain_enum.py example.com")
        sys.exit(1)
    
    domain = sys.argv[1]
    
    try:
        subdomains = enumerate_subdomains(domain)
        
        print(f"\n{'='*60}")
        print(f"Subdomain Enumeration Results for: {domain}")
        print(f"{'='*60}")
        print(f"Total subdomains found: {len(subdomains)}\n")
        
        for subdomain in subdomains:
            print(f"  • {subdomain}")
        
        print(f"\n{'='*60}\n")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

