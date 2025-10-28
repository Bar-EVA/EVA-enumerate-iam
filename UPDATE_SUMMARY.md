# Latest Updates Summary

## Version 2.0.0 - Major Enhancement Release

### 🎉 New Features

#### 1. Auto-Update Check (NEW!)
- Automatically checks for updates on every execution
- Queries GitHub for latest releases
- Non-blocking and can be disabled with `--no-version-check`
- Shows update notification with release notes
- See [VERSION_UPDATE_FEATURE.md](VERSION_UPDATE_FEATURE.md) for details

#### 2. 66 New AWS Services Added
- Comprehensive AWS service coverage expanded from ~139 to 205 services
- 145+ new API operations added
- Total of 1,024 operations now tested
- Includes latest AWS services: Bedrock, Cost Optimization Hub, Geographic services, and more
- See [NEW_SERVICES_ADDED.md](NEW_SERVICES_ADDED.md) for full list

### 📊 Statistics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Services** | ~139 | 205 | +66 |
| **Operations** | ~879 | 1,024 | +145 |
| **Version** | 1.x | 2.0.0 | Major |

### 📁 New Files

1. **`enumerate_iam/__version__.py`** - Version information
2. **`enumerate_iam/version_checker.py`** - Auto-update checking logic
3. **`CUSTOMIZATION_SUMMARY.md`** - Overview of all changes
4. **`NEW_SERVICES_ADDED.md`** - Detailed list of 66 new services
5. **`USAGE_EXAMPLE.md`** - Comprehensive usage guide
6. **`VERSION_UPDATE_FEATURE.md`** - Auto-update documentation
7. **`INSTALLATION.md`** - Installation instructions
8. **`test_version_check.py`** - Test script for version checking

### 🔧 Modified Files

1. **`enumerate_iam/bruteforce_tests.py`** - Added 66 services with operations
2. **`enumerate-iam.py`** - Integrated version checking
3. **`requirements.txt`** - Added `requests` and `packaging` dependencies

### 🚀 How to Update

```bash
cd EVA-enumerate-iam
git pull origin master
pip install -r requirements.txt
```

### ✨ New CLI Options

```bash
# Check version
python enumerate-iam.py --help  # Shows version in description

# Skip version check (faster startup)
python enumerate-iam.py --no-version-check \
  --access-key KEY --secret-key SECRET --region us-east-1
```

### 🎯 Notable New Services

**AI/ML & Bedrock (19 operations)**
- bedrock - Foundation models and inference
- bedrock-agent-runtime - Agent memory
- bedrock-data-automation - Blueprints and projects
- qapps, qconnect - Q Apps and Connect services

**Cost Management (6 operations)**
- billing - Billing views
- cost-optimization-hub - Recommendations
- freetier - Free tier usage
- taxsettings - Tax registrations

**Security (11 operations)**
- controlcatalog - Common controls
- security-ir - Incident response
- inspector-scan - Security scanning
- trustedadvisor - Recommendations

**Geographic (6 operations)**
- geo-maps - Map styles and tiles
- geo-places - Place information
- geo-routes - Route calculation

**Observability (4 operations)**
- application-signals - Service level objectives
- observabilityadmin - Resource telemetry
- networkmonitor - Network monitoring

### 🛡️ Security & Privacy

- Version check only connects to GitHub's public API
- No credentials or sensitive data transmitted
- No telemetry or tracking
- Completely optional (use `--no-version-check`)
- Open source and auditable

### 📝 Usage Examples

```bash
# Basic usage (with auto-update check)
python enumerate-iam.py \
  --access-key AKIA... \
  --secret-key SECRET... \
  --region us-east-1

# Disable update check for faster startup
python enumerate-iam.py \
  --no-version-check \
  --access-key AKIA... \
  --secret-key SECRET... \
  --region us-east-1

# Test version checker
python test_version_check.py
```

### 🔗 Related Documentation

- [INSTALLATION.md](INSTALLATION.md) - How to install and setup
- [USAGE_EXAMPLE.md](USAGE_EXAMPLE.md) - Usage examples and patterns
- [CUSTOMIZATION_SUMMARY.md](CUSTOMIZATION_SUMMARY.md) - Complete customization details
- [NEW_SERVICES_ADDED.md](NEW_SERVICES_ADDED.md) - All 66 new services listed
- [VERSION_UPDATE_FEATURE.md](VERSION_UPDATE_FEATURE.md) - Auto-update feature details

### 🐛 Known Issues

None currently. Please report issues on GitHub.

### 🎯 Future Plans

- [ ] Add more granular service filtering
- [ ] Support for custom IAM policy simulation
- [ ] Export results in multiple formats (JSON, CSV, HTML)
- [ ] Add rate limiting controls
- [ ] Parallel region testing

### 💬 Feedback

Found a bug or have a feature request? Open an issue on GitHub:
https://github.com/Bar-EVA/EVA-enumerate-iam/issues

---

**Current Version**: 2.0.0  
**Last Updated**: October 28, 2025  
**Repository**: https://github.com/Bar-EVA/EVA-enumerate-iam

