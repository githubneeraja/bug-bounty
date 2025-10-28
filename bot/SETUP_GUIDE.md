# Recon Bot - Python Environment Setup Guide

## ✅ Setup Complete

Your Python 3.12 virtual environment `recon_bot_env` has been successfully created and configured with all necessary libraries for recon automation.

## 📍 Location

**Virtual Environment Path:** `C:\Users\Neeraja\Desktop\recon_bot_env`

## 🔧 Installed Libraries

All requested libraries have been installed and verified:

### Core Recon Libraries
- **requests** (2.32.5) - HTTP library for API calls
- **shodan** (1.31.0) - Shodan API client for device reconnaissance
- **censys** (2.2.18) - Censys API client for internet scanning
- **pandas** (2.3.3) - Data manipulation and analysis
- **python-dotenv** (1.2.1) - Environment variable management

### Built-in Module
- **subprocess** - Process execution (Python standard library)

### Dependencies
All transitive dependencies are automatically installed, including:
- numpy, urllib3, certifi, click, colorama, and more

## 🚀 Quick Start

### 1. Activate the Virtual Environment

**Windows (Command Prompt):**
```bash
C:\Users\Neeraja\Desktop\recon_bot_env\Scripts\activate
```

**Windows (PowerShell):**
```powershell
C:\Users\Neeraja\Desktop\recon_bot_env\Scripts\Activate.ps1
```

### 2. Verify Installation

```bash
python -c "import subprocess, requests, shodan, censys, pandas, dotenv; print('✓ All libraries ready!')"
```

### 3. Create Your First Script

```python
import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Your recon automation code here
print("Recon bot environment is ready!")
```

## 📦 Requirements File

A `requirements.txt` file has been generated in the venv directory:
```
C:\Users\Neeraja\Desktop\recon_bot_env\requirements.txt
```

To recreate this environment elsewhere:
```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables Setup

Create a `.env` file in your project directory:

```
SHODAN_API_KEY=your_shodan_key_here
CENSYS_API_ID=your_censys_id_here
CENSYS_API_SECRET=your_censys_secret_here
```

Then load in your Python scripts:
```python
from dotenv import load_dotenv
import os

load_dotenv()
shodan_key = os.getenv('SHODAN_API_KEY')
```

## 🔗 Make.com Integration Compatibility

This environment is fully compatible with Make.com (formerly Integromat):

1. **Python Version:** 3.12 (meets 3.11+ requirement)
2. **All libraries:** Pip-installable and compatible
3. **subprocess module:** Available for system command execution
4. **Environment variables:** Supported via python-dotenv

### For Make.com Webhooks:
```python
import requests
import json

def send_to_make(webhook_url, data):
    response = requests.post(webhook_url, json=data)
    return response.json()
```

## 📋 Library Documentation

- **Shodan:** https://shodan.readthedocs.io/
- **Censys:** https://censys.io/api/
- **Requests:** https://requests.readthedocs.io/
- **Pandas:** https://pandas.pydata.org/docs/
- **python-dotenv:** https://github.com/theskumar/python-dotenv

## ⚠️ Important Notes

1. **Always activate the venv** before running scripts
2. **Keep the venv folder** - it contains all dependencies
3. **Use .env files** for sensitive API keys (never commit to git)
4. **Test imports** regularly to ensure all libraries are accessible

## 🆘 Troubleshooting

### Issue: "python: command not found"
**Solution:** Make sure the venv is activated first

### Issue: "ModuleNotFoundError"
**Solution:** Reinstall the library:
```bash
pip install --upgrade requests shodan censys pandas python-dotenv
```

### Issue: API key errors
**Solution:** Verify your `.env` file exists and contains correct keys

## ✨ Next Steps

1. Create your recon automation scripts
2. Test API connections with your credentials
3. Set up Make.com webhooks for automation
4. Deploy and monitor your recon bot

---

**Setup Date:** October 26, 2025
**Python Version:** 3.12.0
**Environment Name:** recon_bot_env

