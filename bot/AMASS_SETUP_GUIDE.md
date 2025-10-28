# Amass Subdomain Enumeration Guide

## Overview

This guide explains how to set up and use Amass for subdomain enumeration with the provided Python module.

## What is Amass?

**Amass** is an open-source tool by OWASP that performs network mapping of attack surfaces and external asset discovery using open source information gathering and active reconnaissance techniques.

**Key Features:**
- Passive subdomain enumeration
- Active reconnaissance
- DNS enumeration
- Brute force capabilities
- Multiple data source integration
- JSON output support

## Installation

### Windows Installation

#### Option 1: Using Chocolatey (Recommended)
```bash
choco install amass
```

#### Option 2: Using Go
```bash
go install -v github.com/OWASP/Amass/v3/cmd/amass@latest
```

#### Option 3: Download Binary
1. Visit: https://github.com/OWASP/Amass/releases
2. Download the Windows binary
3. Extract to a folder in your PATH
4. Verify: `amass -version`

### Linux Installation

#### Ubuntu/Debian
```bash
sudo apt-get install amass
```

#### Using Go
```bash
go install -v github.com/OWASP/Amass/v3/cmd/amass@latest
```

### macOS Installation

#### Using Homebrew
```bash
brew install amass
```

#### Using Go
```bash
go install -v github.com/OWASP/Amass/v3/cmd/amass@latest
```

## Verify Installation

```bash
amass -version
amass -help
```

## Python Module Usage

### Basic Usage

```python
from amass_subdomain_enum import enumerate_subdomains

# Enumerate subdomains
subdomains = enumerate_subdomains('example.com')

# Print results
for subdomain in subdomains:
    print(subdomain)
```

### Advanced Usage with Class

```python
from amass_subdomain_enum import AmassEnumerator

# Create enumerator instance
enumerator = AmassEnumerator()

# Passive enumeration
subdomains = enumerator.enumerate_subdomains(
    domain='example.com',
    passive_only=True,
    timeout=300
)

# Get detailed JSON data
detailed_results = enumerator.enumerate_subdomains_json(
    domain='example.com',
    passive_only=True
)

for result in detailed_results:
    print(f"Domain: {result['name']}")
    print(f"Source: {result['source']}")
    print(f"Type: {result['type']}")
    print(f"Addresses: {result['addresses']}")
    print()
```

### Command-Line Usage

```bash
# Activate virtual environment
C:\Users\Neeraja\Desktop\recon_bot_env\Scripts\activate

# Run enumeration
python amass_subdomain_enum.py example.com

# Example output:
# ============================================================
# Subdomain Enumeration Results for: example.com
# ============================================================
# Total subdomains found: 42
#
#   • api.example.com
#   • blog.example.com
#   • cdn.example.com
#   • dev.example.com
#   • mail.example.com
#   • www.example.com
# ============================================================
```

## Amass Modes

### Passive Mode (Default)
- Uses only public data sources
- No active scanning
- No network traffic to target
- Slower but stealthier
- **Recommended for reconnaissance**

```bash
amass enum -passive -d example.com
```

### Active Mode
- Performs DNS queries
- May trigger IDS/WAF
- Faster results
- More intrusive

```bash
amass enum -d example.com
```

## Data Sources

Amass uses multiple data sources:
- DNS records
- Certificate transparency logs
- Search engines
- APIs (Shodan, Censys, etc.)
- WHOIS data
- And many more

### Configure API Keys

Create a config file at `~/.config/amass/config.ini`:

```ini
[data_sources]
shodan = YOUR_SHODAN_API_KEY
censys_id = YOUR_CENSYS_ID
censys_secret = YOUR_CENSYS_SECRET
```

## Common Amass Commands

```bash
# Passive enumeration
amass enum -passive -d example.com

# Active enumeration
amass enum -d example.com

# Brute force subdomains
amass enum -brute -d example.com

# Output to JSON
amass enum -d example.com -json output.json

# Output to text file
amass enum -d example.com -o output.txt

# Specify data sources
amass enum -d example.com -src "Shodan,Censys"

# Increase verbosity
amass enum -d example.com -v

# Set timeout
amass enum -d example.com -timeout 60
```

## Integration with Make.com

### Webhook Integration

```python
import requests
from amass_subdomain_enum import enumerate_subdomains

def send_to_make(webhook_url, domain):
    """Send enumeration results to Make.com"""
    try:
        subdomains = enumerate_subdomains(domain)
        
        payload = {
            "domain": domain,
            "total_subdomains": len(subdomains),
            "subdomains": subdomains,
            "timestamp": datetime.now().isoformat()
        }
        
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

# Usage
webhook_url = "https://hook.make.com/your_webhook_path"
send_to_make(webhook_url, "example.com")
```

## Troubleshooting

### Issue: "amass: command not found"
**Solution:** 
- Verify Amass is installed: `amass -version`
- Add Amass to PATH
- Use full path to Amass executable

### Issue: No subdomains found
**Solution:**
- Try active mode: `amass enum -d example.com`
- Check domain spelling
- Verify internet connection
- Configure API keys for more sources

### Issue: Timeout errors
**Solution:**
- Increase timeout: `timeout=600`
- Use passive mode only
- Check network connectivity

### Issue: Permission denied
**Solution:**
- Ensure Amass is executable: `chmod +x amass`
- Run with appropriate permissions

## Performance Tips

1. **Use passive mode** for faster, stealthier enumeration
2. **Configure API keys** for more data sources
3. **Set appropriate timeout** based on domain size
4. **Use JSON output** for better parsing
5. **Run multiple domains** in parallel for efficiency

## Security Considerations

⚠️ **Important:**
- Only enumerate domains you own or have permission to test
- Respect robots.txt and terms of service
- Use passive mode to avoid detection
- Consider rate limiting
- Log all activities for compliance

## Resources

- **Official Repository:** https://github.com/OWASP/Amass
- **Documentation:** https://owasp.org/www-project-amass/
- **Installation Guide:** https://github.com/OWASP/Amass/blob/master/README.md
- **Configuration:** https://github.com/OWASP/Amass/blob/master/examples/config.ini

## Next Steps

1. Install Amass on your system
2. Verify installation with `amass -version`
3. Test the Python module: `python amass_subdomain_enum.py example.com`
4. Integrate with your recon automation workflow
5. Configure API keys for enhanced data sources

---

**Last Updated:** October 26, 2025
**Module Version:** 1.0

