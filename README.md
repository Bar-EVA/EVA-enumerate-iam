# EVA enumerate-iam

> Comprehensive AWS IAM permission enumeration tool supporting 205 services with 1,024+ operations

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/Bar-EVA/EVA-enumerate-iam)
[![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)](LICENSE)
[![AWS Services](https://img.shields.io/badge/AWS_Services-205-orange.svg)](docs/NEW_SERVICES_ADDED.md)

## Overview

Found AWS credentials and need to know their permissions? This tool brute-forces all possible AWS API calls to enumerate IAM permissions. All operations are **read-only** (list, describe, get) and non-destructive.

```bash
./enumerate-iam.py --access-key AKIA... --secret-key SECRET...
```

The tool will test 205 AWS services and report which API calls succeed, revealing the actual permissions available to the credentials.

## Key Features

- ✅ **205 AWS Services** - Comprehensive coverage including Bedrock, Cost Optimization Hub, Geographic services
- ✅ **1,024+ Operations** - All safe read-only API calls
- ✅ **Auto-Update Check** - Automatically notifies when new versions are available
- ✅ **Parallel Execution** - 25 concurrent threads for fast enumeration
- ✅ **Library Support** - Use as CLI or import as Python library
- ✅ **Well Documented** - Complete documentation and examples

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Bar-EVA/EVA-enumerate-iam.git
cd EVA-enumerate-iam

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Enumerate permissions
./enumerate-iam.py \
  --access-key AKIA... \
  --secret-key SECRET... \
  --region us-east-1

# With session token (temporary credentials)
./enumerate-iam.py \
  --access-key ASIA... \
  --secret-key SECRET... \
  --session-token TOKEN... \
  --region us-east-1

# Skip version check for faster startup
./enumerate-iam.py --no-version-check \
  --access-key AKIA... \
  --secret-key SECRET...
```

## What's New in v2.0.0

### Auto-Update Feature 🎉
- Automatically checks for updates on startup
- Shows release notes and download links
- Non-blocking (3-second timeout)
- Disable with `--no-version-check` flag

### 66 New AWS Services Added 🚀
Expanded from 139 to **205 services**, including:

**AI/ML**: Bedrock (14 ops), QApps, QConnect  
**Cost**: Billing, Cost Optimization Hub, Free Tier, Tax Settings  
**Security**: Control Catalog, Security IR, Inspector Scan, Trusted Advisor  
**Geographic**: Geo-maps, Geo-places, Geo-routes  
**Observability**: Application Signals, Network Monitors  
**And 51 more...**

[See complete list →](docs/NEW_SERVICES_ADDED.md)

## Use as Python Library

```python
from enumerate_iam.main import enumerate_iam

results = enumerate_iam(
    access_key='AKIA...',
    secret_key='SECRET...',
    session_token=None,
    region='us-east-1'
)

# Results structure:
# {
#     'iam': {...},        # IAM-specific results
#     'bruteforce': {...}  # Service enumeration results
# }

# Filter results
bedrock_perms = {k: v for k, v in results['bruteforce'].items() 
                 if k.startswith('bedrock')}
```

## CLI Options

```
usage: enumerate-iam.py [-h] --access-key ACCESS_KEY --secret-key SECRET_KEY
                        [--session-token SESSION_TOKEN] [--region REGION]
                        [--no-version-check]

Options:
  --access-key          AWS access key ID (required)
  --secret-key          AWS secret access key (required)
  --session-token       STS session token (optional, for temporary credentials)
  --region              AWS region (default: us-east-1)
  --no-version-check    Skip checking for newer versions
```

## Documentation

| Document | Description |
|----------|-------------|
| [Installation Guide](docs/installation.md) | Detailed setup instructions |
| [Usage Examples](docs/usage.md) | Common use cases and patterns |
| [Auto-Update Feature](docs/auto-update.md) | Version checking documentation |
| [New Services](docs/NEW_SERVICES_ADDED.md) | Complete list of 66 new services |
| [Changelog](docs/changelog.md) | Version history and updates |
| [Customization](docs/CUSTOMIZATION_SUMMARY.md) | How we customized this tool |

## Example Output

```
2025-10-28 10:30:15 - INFO - Starting permission enumeration for access-key-id "AKIA..."
2025-10-28 10:30:16 - INFO - User "admin" has 2 attached policies
2025-10-28 10:30:17 - INFO - Attempting common-service describe / list brute force.
2025-10-28 10:30:18 - INFO - -- bedrock.list_foundation_models() worked!
2025-10-28 10:30:19 - INFO - -- s3.list_buckets() worked!
2025-10-28 10:30:20 - INFO - -- ec2.describe_instances() worked!
2025-10-28 10:30:21 - INFO - -- cost-optimization-hub.get_preferences() worked!
...
```

## Project Structure

```
EVA-enumerate-iam/
├── enumerate-iam.py              # Main CLI entry point
├── test_version_check.py         # Version checker test
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── LICENSE                       # GPL-3.0 license
├── enumerate_iam/
│   ├── __init__.py
│   ├── __version__.py           # Version information
│   ├── main.py                  # Core enumeration logic
│   ├── bruteforce_tests.py      # 205 services, 1,024 operations
│   ├── version_checker.py       # Auto-update functionality
│   └── utils/
│       ├── __init__.py
│       ├── json_utils.py
│       └── remove_metadata.py
└── docs/                         # Documentation
    ├── installation.md          # Installation guide
    ├── usage.md                 # Usage examples
    ├── auto-update.md           # Auto-update docs
    ├── changelog.md             # Version history
    ├── NEW_SERVICES_ADDED.md    # Service list
    └── CUSTOMIZATION_SUMMARY.md # Customization notes
```

## Requirements

- Python 3.7+
- boto3
- botocore
- requests
- packaging

## Security Considerations

- **Read-Only**: Only performs list/describe/get operations
- **No Modifications**: Never creates, updates, or deletes resources
- **Logged Activity**: All API calls are logged in CloudTrail
- **Rate Limiting**: Uses 25 threads by default (configurable)
- **Network Traffic**: Connects to AWS APIs and GitHub (for version check)

⚠️ **Important**: Only use on credentials you own or have permission to test.

## Common Use Cases

### 1. Security Assessment
Audit what permissions are actually available to a set of credentials:
```bash
./enumerate-iam.py --access-key $KEY --secret-key $SECRET > audit.log
```

### 2. Troubleshooting Access
Determine if credentials can access specific services:
```bash
./enumerate-iam.py --access-key $KEY --secret-key $SECRET | grep "bedrock\|s3"
```

### 3. Testing Temporary Credentials
Verify STS assume-role permissions:
```bash
./enumerate-iam.py \
  --access-key $TEMP_KEY \
  --secret-key $TEMP_SECRET \
  --session-token $TOKEN
```

### 4. Programmatic Integration
Use as library for automated security checks:
```python
results = enumerate_iam(key, secret, token, region)
if 'iam.get_account_authorization_details' in results['bruteforce']:
    print("WARNING: Full IAM access detected!")
```

## Performance

- **Typical runtime**: 2-5 minutes
- **Concurrent threads**: 25 (configurable in code)
- **Timeout per call**: 5 seconds
- **Version check**: 3 seconds (can disable)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Import errors | Run `pip install -r requirements.txt` |
| Version check fails | Use `--no-version-check` or check internet connection |
| Slow execution | Some services/regions may be slow; this is normal |
| Rate limiting | AWS may throttle; reduce MAX_THREADS in `main.py` |

## Contributing

Contributions welcome! This fork adds 66 new AWS services. To add more:

1. Update `enumerate_iam/bruteforce_tests.py`
2. Add service name and list/describe/get operations
3. Test with `python -c "import enumerate_iam.bruteforce_tests"`
4. Submit PR

## Updates

To update to the latest version:

```bash
cd EVA-enumerate-iam
git pull origin master
pip install -r requirements.txt
```

The tool automatically checks for updates on startup (disable with `--no-version-check`).

## Credits

- **Original Author**: Andrés Riancho ([@andresriancho](https://github.com/andresriancho))
- **Original Repository**: [andresriancho/enumerate-iam](https://github.com/andresriancho/enumerate-iam)
- **This Fork**: Enhanced with 66 new services and auto-update feature
- **Customized By**: Bar-EVA

## Related Research

This tool was originally released as part of the [Internet-Scale Analysis of AWS Cognito Security](https://www.blackhat.com/us-19/briefings/schedule/#internet-scale-analysis-of-aws-cognito-security-15829) research at Black Hat USA 2019.

## License

GPL-3.0 License - see [LICENSE](LICENSE) file for details.

## Links

- **Repository**: https://github.com/Bar-EVA/EVA-enumerate-iam
- **Issues**: https://github.com/Bar-EVA/EVA-enumerate-iam/issues
- **Original**: https://github.com/andresriancho/enumerate-iam

---

**Version**: 2.0.0 | **AWS Services**: 205 | **Operations**: 1,024+
