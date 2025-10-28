# Auto-Update Implementation Summary

## What Changed

Instead of version-based updates, the tool now uses **file-based service comparison**:

### Old Approach ❌
- Compared version numbers (2.0.0 vs 2.1.0)
- Required manual version tracking
- Would download entire codebase

### New Approach ✅
- Compares `bruteforce_tests.py` file content
- Counts services in local vs GitHub version
- **Only downloads the service database file**
- Automatically installs if more services available

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  1. User runs enumerate-iam.py                              │
│     ↓                                                        │
│  2. Check GitHub for bruteforce_tests.py                    │
│     ↓                                                        │
│  3. Parse local services: 205                               │
│     Parse GitHub services: 215                              │
│     ↓                                                        │
│  4. If GitHub has more → Download file                      │
│     ↓                                                        │
│  5. Backup local file (.backup)                             │
│     ↓                                                        │
│  6. Replace with GitHub version                             │
│     ↓                                                        │
│  7. Validate Python syntax                                  │
│     ↓                                                        │
│  8. Prompt user to restart                                  │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Details

### Files Modified

1. **`enumerate_iam/version_checker.py`**
   - Complete rewrite
   - Now checks service count instead of versions
   - Downloads only `bruteforce_tests.py`
   - Creates backups automatically
   - Validates syntax before replacing

2. **`enumerate-iam.py`**
   - Integrated file-based checker
   - Changed flag: `--no-version-check` → `--no-update-check`
   - Exits after update to prompt restart
   - Better error handling

3. **`requirements.txt`**
   - Removed `packaging` (no longer needed)
   - Kept `requests` for downloads

4. **`docs/auto-update.md`**
   - Updated documentation
   - Explains new file-based approach
   - Troubleshooting guide

### Key Functions

```python
# Check and auto-update
def check_and_update_services(timeout=5):
    """
    Compares local vs GitHub service count
    Downloads file if GitHub has more services
    """
    
# Parse services from file content
def parse_services_from_content(content):
    """
    Extracts service names using regex
    Returns set of service names
    """

# Download and replace
def download_and_replace_bruteforce(content):
    """
    Creates backup
    Replaces file
    Validates syntax
    Rolls back if invalid
    """
```

## Usage

### Before (version-based)
```bash
./enumerate-iam.py --no-version-check \
  --access-key KEY --secret-key SECRET
```

### After (file-based)
```bash
./enumerate-iam.py --no-update-check \
  --access-key KEY --secret-key SECRET
```

## Example Session

```bash
$ ./enumerate-iam.py --access-key AKIA... --secret-key SECRET...

======================================================================
🎉 SERVICE DATABASE UPDATE AVAILABLE!
Current services: 205
GitHub services:  215
New services:     10

New services found:
  + bedrock-runtime
  + qbusiness
  + vpc-lattice
  + verified-permissions
  + payment-cryptography
  + cost-optimization-hub-v2
  + application-auto-scaling-v2
  + cloudwatch-logs-v2
  + ssm-contacts-v2
  + ec2-instance-connect-v2

Downloading updated service database...
✅ Service database updated successfully!
   Added 10 new services

⚠️  Please restart the tool to use new services
======================================================================

⚠️  Service database was updated. Please run the command again.
   This ensures the new services are loaded properly.

$ ./enumerate-iam.py --access-key AKIA... --secret-key SECRET...
# Now runs with 215 services!
```

## Safety Features

### 1. Backup System
- Original file backed up as `bruteforce_tests.py.backup`
- Automatic rollback on failure

### 2. Validation
- Python syntax validation before accepting
- Service count verification
- Regex-based parsing (safe)

### 3. User Control
- Requires restart to use new services
- Can disable with `--no-update-check`
- Clear messaging about changes

### 4. Error Handling
- Network timeout: 5 seconds
- Graceful failure (doesn't block tool)
- Detailed logging for debugging

## Benefits

✅ **No version tracking needed** - File comparison only  
✅ **Automatic** - Downloads and installs automatically  
✅ **Safe** - Backup, validation, rollback  
✅ **Fast** - Only downloads one 40KB file  
✅ **Smart** - Only updates if GitHub has more services  
✅ **Optional** - Can disable with flag  

## What Gets Downloaded

**Only one file**: `enumerate_iam/bruteforce_tests.py`

- **Size**: ~40KB
- **Source**: `https://raw.githubusercontent.com/Bar-EVA/EVA-enumerate-iam/master/enumerate_iam/bruteforce_tests.py`
- **Frequency**: Once per execution (if updates available)
- **No tracking**: Just downloads, never uploads

## Comparison: Old vs New

| Feature | Old (Version-based) | New (File-based) |
|---------|-------------------|------------------|
| **What's checked** | Version numbers | Service count |
| **What's downloaded** | Full repo | Single file |
| **Update trigger** | Version increment | More services |
| **Tracking needed** | Yes (versions) | No (file diff) |
| **Installation** | Manual git pull | Automatic |
| **Size** | Full repo (~1MB) | One file (40KB) |
| **Complexity** | High | Low |

## Testing

### Test the Parser
```python
from enumerate_iam.version_checker import parse_services_from_content

content = open('enumerate_iam/bruteforce_tests.py').read()
services = parse_services_from_content(content)
print(f"Found {len(services)} services")
```

### Test the Checker
```bash
# With check
./enumerate-iam.py --access-key test --secret-key test

# Without check
./enumerate-iam.py --no-update-check --access-key test --secret-key test
```

## Maintenance

### Adding Services Manually

If you add services yourself:
1. Edit `enumerate_iam/bruteforce_tests.py`
2. Add services in alphabetical order
3. The tool will compare your version with GitHub
4. If GitHub has services you don't, it will prompt update

### Force Re-Download

```bash
# Delete local file
rm enumerate_iam/bruteforce_tests.py

# Tool will re-download on next run
./enumerate-iam.py --access-key KEY --secret-key SECRET
```

### Restore Backup

```bash
# If something goes wrong
cp enumerate_iam/bruteforce_tests.py.backup enumerate_iam/bruteforce_tests.py
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Update fails | Check internet, try manual: `git pull origin master` |
| Permission denied | `chmod 644 enumerate_iam/bruteforce_tests.py` |
| Syntax error | Automatic rollback to `.backup` file |
| Slow download | Increase timeout or use `--no-update-check` |

## Future Enhancements

Possible improvements:
- [ ] Cache GitHub check (once per day)
- [ ] Show operation count changes
- [ ] Delta download (only new services)
- [ ] Update other files if needed
- [ ] Silent background updates

---

**Result**: A simpler, smarter update system that "just works" without version management! ✨

