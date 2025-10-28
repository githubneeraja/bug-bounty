#!/usr/bin/env python3
"""
Sample Recon Bot Script
Demonstrates usage of installed libraries for reconnaissance automation
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import requests
import pandas as pd

# Load environment variables
load_dotenv()

class ReconBot:
    """Main reconnaissance bot class"""
    
    def __init__(self):
        """Initialize the recon bot with API credentials"""
        self.shodan_key = os.getenv('SHODAN_API_KEY')
        self.censys_id = os.getenv('CENSYS_API_ID')
        self.censys_secret = os.getenv('CENSYS_API_SECRET')
        self.webhook_url = os.getenv('MAKE_WEBHOOK_URL')
        self.results = []
        
        print("✓ Recon Bot initialized")
        print(f"  - Shodan API: {'✓ Configured' if self.shodan_key else '✗ Not configured'}")
        print(f"  - Censys API: {'✓ Configured' if self.censys_id else '✗ Not configured'}")
        print(f"  - Make.com Webhook: {'✓ Configured' if self.webhook_url else '✗ Not configured'}")
    
    def test_libraries(self):
        """Test that all libraries are working correctly"""
        print("\n📦 Testing installed libraries...")
        
        try:
            import requests
            print("  ✓ requests")
        except ImportError as e:
            print(f"  ✗ requests: {e}")
        
        try:
            import shodan
            print("  ✓ shodan")
        except ImportError as e:
            print(f"  ✗ shodan: {e}")
        
        try:
            import censys
            print("  ✓ censys")
        except ImportError as e:
            print(f"  ✗ censys: {e}")
        
        try:
            import pandas
            print("  ✓ pandas")
        except ImportError as e:
            print(f"  ✗ pandas: {e}")
        
        try:
            import subprocess
            print("  ✓ subprocess")
        except ImportError as e:
            print(f"  ✗ subprocess: {e}")
        
        try:
            from dotenv import load_dotenv
            print("  ✓ python-dotenv")
        except ImportError as e:
            print(f"  ✗ python-dotenv: {e}")
    
    def execute_command(self, command):
        """Execute a system command using subprocess"""
        print(f"\n🔧 Executing command: {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            print(f"  Output: {result.stdout}")
            if result.stderr:
                print(f"  Error: {result.stderr}")
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print("  ✗ Command timed out")
            return False
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return False
    
    def send_to_webhook(self, data):
        """Send results to Make.com webhook"""
        if not self.webhook_url:
            print("⚠️  Webhook URL not configured")
            return False
        
        print(f"\n📤 Sending data to webhook...")
        try:
            response = requests.post(
                self.webhook_url,
                json=data,
                timeout=10
            )
            if response.status_code == 200:
                print("  ✓ Data sent successfully")
                return True
            else:
                print(f"  ✗ Webhook returned status {response.status_code}")
                return False
        except Exception as e:
            print(f"  ✗ Error sending to webhook: {e}")
            return False
    
    def save_results(self, filename="recon_results.json"):
        """Save results to file"""
        print(f"\n💾 Saving results to {filename}...")
        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            print(f"  ✓ Results saved")
            return True
        except Exception as e:
            print(f"  ✗ Error saving results: {e}")
            return False
    
    def create_dataframe(self):
        """Create a pandas DataFrame from results"""
        print("\n📊 Creating data analysis...")
        try:
            df = pd.DataFrame(self.results)
            print(f"  ✓ DataFrame created with {len(df)} rows")
            print(f"  Columns: {list(df.columns)}")
            return df
        except Exception as e:
            print(f"  ✗ Error creating DataFrame: {e}")
            return None
    
    def run_demo(self):
        """Run a demonstration of the bot"""
        print("\n" + "="*50)
        print("RECON BOT - DEMONSTRATION")
        print("="*50)
        
        # Test libraries
        self.test_libraries()
        
        # Add sample data
        self.results = [
            {
                "timestamp": datetime.now().isoformat(),
                "type": "domain_scan",
                "target": "example.com",
                "status": "success",
                "data": {"ip": "93.184.216.34", "ports": [80, 443]}
            },
            {
                "timestamp": datetime.now().isoformat(),
                "type": "port_scan",
                "target": "192.168.1.1",
                "status": "success",
                "data": {"open_ports": [22, 80, 443]}
            }
        ]
        
        # Save results
        self.save_results()
        
        # Create DataFrame
        df = self.create_dataframe()
        
        # Send to webhook (if configured)
        if self.webhook_url:
            self.send_to_webhook({"results": self.results})
        
        print("\n" + "="*50)
        print("✓ DEMONSTRATION COMPLETE")
        print("="*50)


def main():
    """Main entry point"""
    try:
        bot = ReconBot()
        bot.run_demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

