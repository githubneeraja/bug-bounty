#!/usr/bin/env python3
"""
Recon Automation Bot
Complete reconnaissance pipeline: Amass → Shodan → Nmap → Gemini AI → Google Docs
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
import requests

# Import recon modules
try:
    from amass_subdomain_enum import enumerate_subdomains
    from shodan_scanner import scan_with_shodan
    from nmap_scanner import scan_target
    from make_automation import process_recon_results
except ImportError as e:
    print(f"Warning: Could not import recon modules: {e}")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()


class ReconAutomationBot:
    """Main automation bot orchestrating the full recon pipeline"""
    
    def __init__(self):
        """Initialize the bot"""
        self.make_webhook_url = os.getenv('MAKE_WEBHOOK_URL')
        self.results = {}
    
    def enumerate_subdomains(self, domain: str) -> List[str]:
        """
        Step 1: Enumerate subdomains using Amass
        
        Args:
            domain: Target domain
        
        Returns:
            List of discovered subdomains
        """
        logger.info(f"Step 1: Enumerating subdomains for {domain}")
        
        try:
            subdomains = enumerate_subdomains(domain)
            logger.info(f"Found {len(subdomains)} subdomains")
            self.results['subdomains'] = subdomains
            return subdomains
        except Exception as e:
            logger.error(f"Subdomain enumeration failed: {e}")
            self.results['subdomains'] = []
            return []
    
    def scan_with_shodan(self, subdomains: List[str]) -> Dict[str, Any]:
        """
        Step 2: Scan subdomains with Shodan API
        
        Args:
            subdomains: List of subdomains to scan
        
        Returns:
            Shodan scan results
        """
        logger.info(f"Step 2: Scanning {len(subdomains)} subdomains with Shodan")
        
        try:
            # Limit to first 5 subdomains to avoid API quota issues
            results = scan_with_shodan(subdomains[:5])
            logger.info("Shodan scan completed")
            self.results['shodan'] = results
            return results
        except Exception as e:
            logger.error(f"Shodan scan failed: {e}")
            self.results['shodan'] = {}
            return {}
    
    def scan_with_nmap(self, domain: str) -> Dict[str, Any]:
        """
        Step 3: Scan domain with Nmap
        
        Args:
            domain: Target domain
        
        Returns:
            Nmap scan results
        """
        logger.info(f"Step 3: Scanning {domain} with Nmap")
        
        try:
            output_file = f"{domain}_nmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            results = scan_target(domain, output_file=output_file)
            logger.info(f"Nmap scan completed, results saved to {output_file}")
            self.results['nmap'] = results
            self.results['nmap_file'] = output_file
            return results
        except Exception as e:
            logger.error(f"Nmap scan failed: {e}")
            self.results['nmap'] = {}
            return {}
    
    def prepare_files_for_make(self, domain: str) -> List[Dict[str, Any]]:
        """
        Prepare recon results as files for Make.com
        
        Args:
            domain: Target domain
        
        Returns:
            List of file dictionaries
        """
        logger.info("Step 4: Preparing files for Make.com")
        
        files = []
        
        # Amass results
        if self.results.get('subdomains'):
            files.append({
                'name': f'{domain}_amass_results.txt',
                'content': '\n'.join(self.results['subdomains'])
            })
        
        # Shodan results
        if self.results.get('shodan'):
            files.append({
                'name': f'{domain}_shodan_results.json',
                'content': json.dumps(self.results['shodan'], indent=2, default=str)
            })
        
        # Nmap results
        if self.results.get('nmap'):
            files.append({
                'name': f'{domain}_nmap_results.json',
                'content': json.dumps(self.results['nmap'], indent=2, default=str)
            })
        
        logger.info(f"Prepared {len(files)} files for Make.com")
        return files
    
    def send_to_make(self, files: List[Dict[str, Any]], domain: str) -> Dict[str, Any]:
        """
        Step 5: Send results to Make.com for processing
        
        Args:
            files: List of recon result files
            domain: Target domain
        
        Returns:
            Make.com processing results
        """
        logger.info("Step 5: Sending results to Make.com")
        
        if not self.make_webhook_url:
            logger.error("MAKE_WEBHOOK_URL not configured")
            return {'status': 'error', 'message': 'Webhook URL not configured'}
        
        try:
            payload = {
                'target_domain': domain,
                'files': files,
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(
                self.make_webhook_url,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info("Successfully sent to Make.com")
                return response.json()
            else:
                logger.error(f"Make.com error: {response.status_code}")
                return {'status': 'error', 'code': response.status_code}
        
        except Exception as e:
            logger.error(f"Error sending to Make.com: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def run_full_pipeline(self, domain: str) -> Dict[str, Any]:
        """
        Run the complete reconnaissance pipeline
        
        Args:
            domain: Target domain
        
        Returns:
            Complete pipeline results
        """
        logger.info(f"Starting full recon pipeline for {domain}")
        logger.info("=" * 70)
        
        start_time = datetime.now()
        
        try:
            # Step 1: Enumerate subdomains
            subdomains = self.enumerate_subdomains(domain)
            
            # Step 2: Scan with Shodan
            shodan_results = self.scan_with_shodan(subdomains)
            
            # Step 3: Scan with Nmap
            nmap_results = self.scan_with_nmap(domain)
            
            # Step 4: Prepare files
            files = self.prepare_files_for_make(domain)
            
            # Step 5: Send to Make.com
            make_results = self.send_to_make(files, domain)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("=" * 70)
            logger.info(f"Pipeline completed in {duration:.2f} seconds")
            
            return {
                'status': 'success',
                'domain': domain,
                'subdomains_found': len(subdomains),
                'shodan_results': shodan_results,
                'nmap_results': nmap_results,
                'make_results': make_results,
                'duration_seconds': duration,
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            return {
                'status': 'error',
                'domain': domain,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Recon Automation Bot - Complete reconnaissance pipeline'
    )
    parser.add_argument('domain', help='Target domain to scan')
    parser.add_argument(
        '--output',
        help='Output file for results (JSON)',
        default=None
    )
    
    args = parser.parse_args()
    
    # Run pipeline
    bot = ReconAutomationBot()
    results = bot.run_full_pipeline(args.domain)
    
    # Output results
    print("\n" + "=" * 70)
    print("RECON AUTOMATION BOT - RESULTS")
    print("=" * 70)
    print(json.dumps(results, indent=2, default=str))
    
    # Save to file if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"Results saved to {args.output}")
    
    return results


if __name__ == "__main__":
    main()

