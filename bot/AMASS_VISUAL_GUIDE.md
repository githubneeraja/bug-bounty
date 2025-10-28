# Amass Subdomain Enumeration - Visual Guide

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Python Script                        │
│                                                              │
│  from amass_subdomain_enum import enumerate_subdomains     │
│  subdomains = enumerate_subdomains('example.com')           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              amass_subdomain_enum.py Module                 │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  enumerate_subdomains(domain: str) -> List[str]     │  │
│  │  - Validates input                                   │  │
│  │  - Creates AmassEnumerator                           │  │
│  │  - Calls enumerate_subdomains()                      │  │
│  │  - Returns list of subdomains                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  AmassEnumerator Class                               │  │
│  │  - verify_amass_installed()                          │  │
│  │  - enumerate_subdomains()                            │  │
│  │  - enumerate_subdomains_json()                       │  │
│  │  - _parse_amass_output()                             │  │
│  │  - _parse_amass_json()                               │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              subprocess.run() - Execute Amass               │
│                                                              │
│  Command: amass enum -passive -d example.com               │
│  Capture: stdout, stderr                                    │
│  Timeout: 300 seconds (configurable)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Amass Tool                               │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Passive Mode (Default)                              │  │
│  │  - DNS records                                       │  │
│  │  - Certificate transparency                          │  │
│  │  - Search engines                                    │  │
│  │  - Public APIs                                       │  │
│  │  - WHOIS data                                        │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Output Parsing                           │
│                                                              │
│  Raw Output:                                                │
│  api.example.com                                            │
│  blog.example.com                                           │
│  www.example.com                                            │
│                                                              │
│  Parsed Result:                                             │
│  ['api.example.com', 'blog.example.com', 'www.example.com']│
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Return to User                           │
│                                                              │
│  List[str] of discovered subdomains                         │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Data Flow Diagram

```
Input Domain
    │
    ▼
Validation
    │
    ├─ Empty? ──► ValueError
    │
    ├─ Not String? ──► ValueError
    │
    └─ Valid ──► Continue
                 │
                 ▼
         Normalize (lowercase, strip)
                 │
                 ▼
         Build Amass Command
                 │
                 ├─ amass enum
                 ├─ -passive
                 ├─ -d example.com
                 └─ (optional: -json output.json)
                 │
                 ▼
         Execute subprocess.run()
                 │
                 ├─ Success ──► Parse Output
                 │              │
                 │              ▼
                 │         Extract Subdomains
                 │              │
                 │              ▼
                 │         Sort & Deduplicate
                 │              │
                 │              ▼
                 │         Return List[str]
                 │
                 └─ Error ──► RuntimeError
                              │
                              ▼
                         Log Error
                              │
                              ▼
                         Raise Exception
```

## 🔄 Integration Patterns

### Pattern 1: Simple Function
```
User Code
    │
    ▼
enumerate_subdomains('example.com')
    │
    ▼
List[str]
    │
    ▼
Process Results
```

### Pattern 2: Class-Based
```
User Code
    │
    ▼
AmassEnumerator()
    │
    ├─ verify_amass_installed()
    │
    ▼
enumerate_subdomains()
    │
    ▼
List[str]
    │
    ▼
Process Results
```

### Pattern 3: JSON Output
```
User Code
    │
    ▼
AmassEnumerator()
    │
    ▼
enumerate_subdomains_json()
    │
    ▼
List[Dict]
    │
    ├─ name
    ├─ source
    ├─ type
    ├─ tag
    └─ addresses
    │
    ▼
Export/Analyze
```

### Pattern 4: Make.com Integration
```
User Code
    │
    ▼
enumerate_subdomains()
    │
    ▼
List[str]
    │
    ▼
Build Payload
    │
    ├─ domain
    ├─ timestamp
    ├─ total_subdomains
    └─ subdomains
    │
    ▼
requests.post(webhook_url)
    │
    ▼
Make.com Scenario
    │
    ├─ Process Data
    ├─ Store Results
    ├─ Send Notifications
    └─ Generate Reports
```

## 📈 Performance Characteristics

```
Domain Size vs Time

Large Domain (1000+ subdomains)
████████████████████ 60 seconds

Medium Domain (100-1000 subdomains)
██████████ 30 seconds

Small Domain (10-100 subdomains)
█████ 15 seconds

Tiny Domain (< 10 subdomains)
██ 5 seconds

Timeout: 300 seconds (configurable)
```

## 🎯 Use Case Flowchart

```
Start
  │
  ▼
Need Subdomains?
  │
  ├─ Yes ──► Install Amass
  │           │
  │           ▼
  │         Import Module
  │           │
  │           ▼
  │         Call enumerate_subdomains()
  │           │
  │           ▼
  │         Get Results
  │           │
  │           ├─ Export to CSV
  │           ├─ Export to JSON
  │           ├─ Analyze with Pandas
  │           ├─ Send to Make.com
  │           └─ Process Further
  │           │
  │           ▼
  │         Done
  │
  └─ No ──► Exit
```

## 🔐 Security Flow

```
Input Domain
    │
    ▼
Validate Input
    │
    ├─ Check if empty
    ├─ Check if string
    ├─ Normalize (lowercase)
    └─ Sanitize
    │
    ▼
Verify Amass Installed
    │
    ├─ Check PATH
    ├─ Verify executable
    └─ Get version
    │
    ▼
Execute in Passive Mode
    │
    ├─ No active scanning
    ├─ No network probes
    └─ Public data only
    │
    ▼
Parse Output Safely
    │
    ├─ Validate JSON
    ├─ Handle errors
    └─ Sanitize data
    │
    ▼
Return Results
    │
    ├─ Log activity
    ├─ Track metrics
    └─ Audit trail
```

## 📚 File Organization

```
Project Root
│
├── amass_subdomain_enum.py
│   ├── AmassEnumerator class
│   ├── enumerate_subdomains() function
│   └── Helper methods
│
├── amass_examples.py
│   ├── Example 1: Basic
│   ├── Example 2: JSON
│   ├── Example 3: CSV
│   ├── Example 4: JSON File
│   ├── Example 5: Pandas
│   ├── Example 6: Multiple
│   ├── Example 7: Webhook
│   └── Example 8: Error Handling
│
├── test_amass_enum.py
│   ├── TestAmassEnumerator
│   ├── TestEnumerateSubdomainsFunction
│   └── TestIntegration
│
├── Documentation
│   ├── AMASS_README.md
│   ├── AMASS_SETUP_GUIDE.md
│   ├── AMASS_INTEGRATION_GUIDE.md
│   ├── AMASS_QUICK_REFERENCE.md
│   ├── AMASS_IMPLEMENTATION_SUMMARY.md
│   └── AMASS_VISUAL_GUIDE.md
│
└── Configuration
    └── .env (optional)
        ├── MAKE_WEBHOOK_URL
        ├── SHODAN_API_KEY
        ├── CENSYS_API_ID
        └── CENSYS_API_SECRET
```

## 🚀 Deployment Pipeline

```
Development
    │
    ▼
Testing
    │
    ├─ Unit Tests
    ├─ Integration Tests
    └─ Manual Testing
    │
    ▼
Documentation
    │
    ├─ API Reference
    ├─ Setup Guide
    ├─ Examples
    └─ Troubleshooting
    │
    ▼
Staging
    │
    ├─ Test with Real Domains
    ├─ Verify Performance
    └─ Check Error Handling
    │
    ▼
Production
    │
    ├─ Deploy Module
    ├─ Configure Environment
    ├─ Set Up Logging
    └─ Monitor Usage
    │
    ▼
Maintenance
    │
    ├─ Monitor Performance
    ├─ Track Errors
    ├─ Update Documentation
    └─ Optimize Code
```

## 💡 Decision Tree

```
Need to enumerate subdomains?
    │
    ├─ Yes
    │   │
    │   ├─ Need just domain names?
    │   │   │
    │   │   ├─ Yes ──► Use enumerate_subdomains()
    │   │   │
    │   │   └─ No ──► Use enumerate_subdomains_json()
    │   │
    │   ├─ Need to export data?
    │   │   │
    │   │   ├─ CSV ──► Use csv module
    │   │   ├─ JSON ──► Use json module
    │   │   └─ Database ──► Use pandas
    │   │
    │   ├─ Need to send to Make.com?
    │   │   │
    │   │   └─ Yes ──► Use requests + webhook
    │   │
    │   └─ Need to analyze data?
    │       │
    │       └─ Yes ──► Use pandas DataFrame
    │
    └─ No ──► Exit
```

## 📊 Output Examples

### Text Output
```
api.example.com
blog.example.com
cdn.example.com
dev.example.com
mail.example.com
www.example.com
```

### JSON Output
```json
{
  "name": "api.example.com",
  "source": "Shodan",
  "type": "CNAME",
  "tag": "cert",
  "addresses": ["192.0.2.1"]
}
```

### CSV Output
```
name,source,type,tag,addresses
api.example.com,Shodan,CNAME,cert,192.0.2.1
blog.example.com,Censys,A,cert,192.0.2.2
```

---

**Visual Guide v1.0** | October 26, 2025

