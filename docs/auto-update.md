# Auto-Update Service Database

## Overview

EVA enumerate-iam automatically checks GitHub for updates to the AWS service database (`bruteforce_tests.py`) on every execution. If new services are found, they're automatically downloaded and installed.

## How It Works

### Automatic Check Process

1. **Startup Check**: Every time you run the tool, it checks GitHub
2. **Service Comparison**: Compares local services vs GitHub services
3. **Auto-Download**: If GitHub has more services, downloads the updated file
4. **Restart Prompt**: Asks you to restart to use new services

### What Gets Updated

- **Only** the `enumerate_iam/bruteforce_tests.py` file
- Contains the list of 205+ AWS services and their operations
- No code changes, just service additions

## Usage

### Normal Execution (with auto-update)
```bash
./enumerate-iam.py \
  --access-key AKIA... \
  --secret-key SECRET... \
  --region us-east-1
```

If updates are found:
```
======================================================================
🎉 SERVICE DATABASE UPDATE AVAILABLE!
Current services: 205
GitHub services:  215
New services:     10

New services found:
  + new-aws-service-1
  + new-aws-service-2
  ... and 8 more

Downloading updated service database...
✅ Service database updated successfully!
   Added 10 new services

⚠️  Please restart the tool to use new services
======================================================================
```

### Disable Auto-Update
```bash
./enumerate-iam.py \
  --no-update-check \
  --access-key AKIA... \
  --secret-key SECRET...
```

## Example Output

When new services are available:

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

# Just run the same command again
$ ./enumerate-iam.py --access-key AKIA... --secret-key SECRET...
# Now runs with 215 services!
```

## Technical Details

### File Updated
- **Location**: `enumerate_iam/bruteforce_tests.py`
- **Backup**: Automatically created as `bruteforce_tests.py.backup`
- **Safety**: Syntax validation before replacement

### Update Logic
1. Load current `BRUTEFORCE_TESTS` dictionary
2. Download GitHub version via raw content API
3. Parse both to count services
4. If GitHub has more services:
   - Create backup of current file
   - Download and replace file
   - Validate Python syntax
   - Prompt user to restart

### Network Usage
- **URL**: `https://raw.githubusercontent.com/Bar-EVA/EVA-enumerate-iam/master/enumerate_iam/bruteforce_tests.py`
- **Timeout**: 5 seconds
- **Size**: ~40KB file download
- **Frequency**: Once per execution (cached in memory)

## Safety Features

### Backup System
- Original file backed up before update
- Automatic rollback if download fails
- Syntax validation before replacement

### Validation
- Python syntax check on downloaded file
- Service count verification
- Non-blocking (fails gracefully)

### User Control
- User must restart to use new services
- Can disable with `--no-update-check`
- Clear messaging about what changed

## Troubleshooting

### Update check fails
**Symptom**: No update notification appears  
**Solutions**:
- Check internet connectivity
- Verify GitHub.com is accessible
- Check firewall/proxy settings
- Use `--no-update-check` to skip

### File download fails
**Symptom**: "Could not update service database automatically"  
**Solutions**:
```bash
# Manual update
cd EVA-enumerate-iam
git pull origin master
```

### Service count mismatch
**Symptom**: Shows same count after update  
**Solutions**:
- Restart the tool (Python caches imports)
- Check `bruteforce_tests.py.backup` exists
- Verify file was actually updated

### Permission errors
**Symptom**: "Could not replace bruteforce_tests.py"  
**Solutions**:
```bash
# Fix permissions
chmod 644 enumerate_iam/bruteforce_tests.py

# Or run manual update
git pull origin master
```

## Disabling Permanently

### Option 1: Use alias
```bash
# Add to ~/.bashrc or ~/.zshrc
alias enumerate-iam='python enumerate-iam.py --no-update-check'
```

### Option 2: Environment variable
```bash
# Add to shell profile
export ENUMERATE_IAM_NO_UPDATE=1
```

Then modify `enumerate-iam.py`:
```python
import os
if not args.no_update_check and not os.getenv('ENUMERATE_IAM_NO_UPDATE'):
    # check for updates
```

### Option 3: Comment out check
Edit `enumerate-iam.py` and comment out lines 24-32:
```python
# if not args.no_update_check:
#     try:
#         from enumerate_iam.version_checker import check_and_notify
#         ...
```

## Privacy & Security

### What's Sent
- **Nothing** - Only downloads, never uploads

### What's Downloaded
- Single file: `bruteforce_tests.py`
- No telemetry or tracking
- Open source and auditable

### Network Endpoints
- `raw.githubusercontent.com` - File downloads only
- No analytics or tracking servers

## Benefits

✅ Always have latest AWS service coverage  
✅ Automatic - no manual git pull needed  
✅ Safe - backup and validation  
✅ Fast - single file, ~40KB  
✅ Optional - can disable anytime  
✅ Transparent - shows what's new  

## Advanced: Manual Service Addition

If you want to add services without auto-update:

1. Edit `enumerate_iam/bruteforce_tests.py`
2. Add new service entry:
```python
"your-new-service": [
    "list_resources",
    "describe_configuration",
    "get_settings"
],
```
3. Test: `python -c "import enumerate_iam.bruteforce_tests"`
4. Run tool normally

## See Also

- [Installation Guide](installation.md) - Setup instructions
- [Usage Examples](usage.md) - How to use the tool
- [Service List](NEW_SERVICES_ADDED.md) - All supported services
