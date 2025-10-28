# Auto-Update Check Feature

## Overview

The enumerate-iam tool now automatically checks for newer versions on every execution by querying the GitHub repository.

## How It Works

1. **Automatic Check**: On every execution, the tool checks the GitHub repository for updates
2. **Non-Blocking**: If the version check fails or times out, the tool continues normally
3. **User Notification**: If an update is available, a clear message is displayed before execution
4. **Can Be Disabled**: Use `--no-version-check` flag to skip the check

## Usage

### Normal Execution (with version check)
```bash
python enumerate-iam.py \
  --access-key AKIA... \
  --secret-key SECRET... \
  --region us-east-1
```

### Disable Version Check
```bash
python enumerate-iam.py \
  --access-key AKIA... \
  --secret-key SECRET... \
  --region us-east-1 \
  --no-version-check
```

## Example Output

When an update is available:

```
======================================================================
🎉 UPDATE AVAILABLE!
Current version: 2.0.0
Latest version:  2.1.0

Download: https://github.com/Bar-EVA/EVA-enumerate-iam/releases/latest
Release notes: Added 20 new AWS services, improved performance...

To update, run:
  cd /path/to/EVA-enumerate-iam
  git pull origin master
  pip install -r requirements.txt
======================================================================
```

## Configuration

### Version Information
The current version is stored in `enumerate_iam/__version__.py`:
```python
__version__ = "2.0.0"
__repo_url__ = "https://github.com/Bar-EVA/EVA-enumerate-iam"
```

### Timeout
The version check has a 3-second timeout by default to avoid delaying execution.

### Update Detection
The tool checks:
1. **GitHub Releases**: If releases exist, compares version tags
2. **Latest Commits**: If no releases, checks for latest commits
3. **Version Comparison**: Uses semantic versioning (major.minor.patch)

## Technical Details

### Files Added
- `enumerate_iam/__version__.py` - Version information
- `enumerate_iam/version_checker.py` - Update checking logic

### Files Modified
- `enumerate-iam.py` - Integrated version check on startup
- `requirements.txt` - Added `requests` and `packaging` dependencies

### Dependencies
- **requests**: For HTTP calls to GitHub API
- **packaging**: For semantic version comparison

## Privacy & Security

- Only connects to GitHub's public API
- No credentials or sensitive data transmitted
- No telemetry or tracking
- Open source and auditable

## Disabling Permanently

If you want to disable version checking permanently, you can:

1. **Environment variable** (add to your shell profile):
```bash
export ENUMERATE_IAM_NO_VERSION_CHECK=1
```

2. **Always use flag**:
```bash
alias enumerate-iam='python enumerate-iam.py --no-version-check'
```

3. **Remove the check** (edit `enumerate-iam.py`):
```python
# Comment out or remove these lines:
# if not args.no_version_check:
#     try:
#         check_and_notify()
#     except Exception:
#         pass
```

## Benefits

- ✅ Stay up-to-date with latest AWS service additions
- ✅ Get security patches and bug fixes
- ✅ Know about new features immediately
- ✅ Non-intrusive and optional
- ✅ Works offline (fails gracefully)

## Troubleshooting

### Version check fails
- Check internet connectivity
- Verify GitHub.com is accessible
- Use `--no-version-check` to skip

### False positives
- May show updates if running from a development branch
- Version comparison uses semantic versioning
- Check actual version with `--help`

### Slow execution
- Default timeout is 3 seconds
- Network issues may cause delays
- Use `--no-version-check` for faster startup

