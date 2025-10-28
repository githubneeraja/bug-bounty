#!/usr/bin/env python3
"""
Make.com Automation Pipeline
Processes recon results via webhook, uses Gemini AI for analysis, and creates Google Docs
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()


class ReconAnalyzer:
    """Analyzes recon results using Gemini AI"""
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        """
        Initialize Gemini AI analyzer
        
        Args:
            gemini_api_key: Google Gemini API key (from environment if not provided)
        """
        self.gemini_api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
    
    def parse_recon_files(self, files: List[Dict[str, Any]]) -> str:
        """
        Parse recon result files
        
        Args:
            files: List of file dictionaries with 'name' and 'content' keys
        
        Returns:
            str: Formatted content for analysis
        """
        parsed_content = "# Recon Results Analysis\n\n"
        
        for file_info in files:
            file_name = file_info.get('name', 'unknown')
            content = file_info.get('content', '')
            
            parsed_content += f"## {file_name}\n"
            parsed_content += f"{content}\n\n"
        
        return parsed_content
    
    def analyze_with_gemini(self, recon_content: str) -> str:
        """
        Analyze recon content using Gemini AI
        
        Args:
            recon_content: Formatted recon results
        
        Returns:
            str: Gemini AI analysis in Markdown format
        """
        prompt = f"""Analyze the following reconnaissance results and provide a comprehensive security report:

{recon_content}

Please provide:
1. **Critical Findings**: List any critical vulnerabilities or exposures
2. **Services & Ports**: Summarize all open ports and running services
3. **Certificate Analysis**: Extract and analyze SSL/TLS certificate details
4. **Recommendations**: Suggest next steps for security hardening

Format your response in clear Markdown with sections and bullet points."""
        
        try:
            response = requests.post(
                self.gemini_url,
                headers={'Content-Type': 'application/json'},
                json={
                    'contents': [{
                        'parts': [{'text': prompt}]
                    }]
                },
                params={'key': self.gemini_api_key},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text']
            
            logger.error(f"Gemini API error: {response.status_code} - {response.text}")
            raise RuntimeError(f"Gemini API failed: {response.status_code}")
        
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            raise
    
    def markdown_to_html(self, markdown_text: str) -> str:
        """
        Convert Markdown to HTML
        
        Args:
            markdown_text: Markdown formatted text
        
        Returns:
            str: HTML formatted text
        """
        try:
            import markdown
            return markdown.markdown(markdown_text, extensions=['extra', 'codehilite'])
        except ImportError:
            logger.warning("markdown library not installed, returning plain text")
            return f"<pre>{markdown_text}</pre>"


class GoogleDocsCreator:
    """Creates Google Docs from analysis results"""
    
    def __init__(self, google_api_key: Optional[str] = None):
        """
        Initialize Google Docs creator
        
        Args:
            google_api_key: Google API key (from environment if not provided)
        """
        self.google_api_key = google_api_key or os.getenv('GOOGLE_API_KEY')
        self.docs_url = "https://docs.googleapis.com/v1/documents"
    
    def create_document(
        self,
        title: str,
        content: str,
        target_domain: str
    ) -> Dict[str, Any]:
        """
        Create a Google Doc with analysis results
        
        Args:
            title: Document title
            content: HTML formatted content
            target_domain: Target domain for the report
        
        Returns:
            Dict: Document creation response
        """
        doc_title = f"Recon Report - {target_domain} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        try:
            # This is a placeholder for actual Google Docs API integration
            # In production, use google-auth and google-api-python-client
            logger.info(f"Creating Google Doc: {doc_title}")
            
            response = {
                'documentId': f"doc_{datetime.now().timestamp()}",
                'title': doc_title,
                'content': content,
                'created_at': datetime.now().isoformat(),
                'target_domain': target_domain
            }
            
            return response
        
        except Exception as e:
            logger.error(f"Error creating Google Doc: {e}")
            raise


class MakeWebhookHandler:
    """Handles incoming webhooks from Make.com"""
    
    def __init__(self):
        """Initialize webhook handler"""
        self.analyzer = ReconAnalyzer()
        self.docs_creator = GoogleDocsCreator()
    
    def process_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming webhook data
        
        Args:
            webhook_data: Data from Make.com webhook
        
        Returns:
            Dict: Processing results
        """
        try:
            # Extract files and target domain
            files = webhook_data.get('files', [])
            target_domain = webhook_data.get('target_domain', 'unknown')
            
            if not files:
                raise ValueError("No files provided in webhook")
            
            logger.info(f"Processing {len(files)} files for domain: {target_domain}")
            
            # Parse recon files
            recon_content = self.analyzer.parse_recon_files(files)
            
            # Analyze with Gemini
            analysis = self.analyzer.analyze_with_gemini(recon_content)
            
            # Convert to HTML
            html_content = self.analyzer.markdown_to_html(analysis)
            
            # Create Google Doc
            doc_response = self.docs_creator.create_document(
                title=f"Recon Report - {target_domain}",
                content=html_content,
                target_domain=target_domain
            )
            
            return {
                'status': 'success',
                'document': doc_response,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }


def process_recon_results(
    files: List[Dict[str, Any]],
    target_domain: str
) -> Dict[str, Any]:
    """
    Main function to process recon results
    
    Args:
        files: List of recon result files
        target_domain: Target domain
    
    Returns:
        Dict: Processing results
    """
    handler = MakeWebhookHandler()
    
    webhook_data = {
        'files': files,
        'target_domain': target_domain
    }
    
    return handler.process_webhook(webhook_data)


if __name__ == "__main__":
    # Example usage
    sample_files = [
        {
            'name': 'amass_results.txt',
            'content': 'example.com\nwww.example.com\napi.example.com\nmail.example.com'
        },
        {
            'name': 'shodan_results.json',
            'content': '{"example.com": {"ip": "1.2.3.4", "ports": [80, 443], "services": ["http", "https"]}}'
        },
        {
            'name': 'nmap_results.txt',
            'content': 'Port 80: http\nPort 443: https\nSSL/TLS: TLSv1.2, TLSv1.3'
        }
    ]
    
    result = process_recon_results(sample_files, 'example.com')
    print(json.dumps(result, indent=2))

