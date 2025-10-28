# Installation Guide

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Bar-EVA/EVA-enumerate-iam.git
cd EVA-enumerate-iam
```

### 2. Install Dependencies

#### Option A: Using pip
```bash
pip install -r requirements.txt
```

#### Option B: Using uv (recommended)
```bash
uv pip install -r requirements.txt
```

#### Option C: Using a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
python enumerate-iam.py --help
```

You should see:
```
usage: enumerate-iam.py [-h] --access-key ACCESS_KEY --secret-key SECRET_KEY
                        [--session-token SESSION_TOKEN] [--region REGION]
                        [--no-version-check]

Enumerate IAM permissions (v2.0.0)
...
```

## Dependencies

The tool requires the following Python packages:

- **boto3** - AWS SDK for Python
- **botocore** - Low-level AWS service access
- **requests** - HTTP library for version checking
- **packaging** - Version comparison utilities

## Testing the Installation

### Test Version Check Feature
```bash
python test_version_check.py
```

### Test Basic Functionality
```bash
# This will fail without valid credentials, but shows the tool works
python enumerate-iam.py --access-key test --secret-key test --region us-east-1
```

## Updating

### Update from GitHub
```bash
cd EVA-enumerate-iam
git pull origin master
pip install -r requirements.txt
```

### Check Current Version
```bash
python -c "from enumerate_iam.__version__ import __version__; print(__version__)"
```

## Troubleshooting

### ImportError: No module named 'boto3'
```bash
pip install boto3 botocore
```

### ImportError: No module named 'requests'
```bash
pip install requests packaging
```

### Version check fails
- Check internet connectivity
- Verify GitHub.com is accessible
- Use `--no-version-check` flag to skip version checking

### Permission denied on macOS/Linux
```bash
chmod +x enumerate-iam.py
./enumerate-iam.py --help
```

## Running from EC2 with Web Shell

If you're running this on an EC2 instance with the web shell we set up:

```bash
# SSH or use the web shell at https://YOUR_EC2_IP/
cd ~
git clone https://github.com/Bar-EVA/EVA-enumerate-iam.git
cd EVA-enumerate-iam
pip3 install --user -r requirements.txt

# Run the tool
python3 enumerate-iam.py \
  --access-key YOUR_KEY \
  --secret-key YOUR_SECRET \
  --region us-east-1
```

## Docker (Alternative)

If you prefer Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "enumerate-iam.py"]
```

Build and run:
```bash
docker build -t enumerate-iam .
docker run enumerate-iam \
  --access-key YOUR_KEY \
  --secret-key YOUR_SECRET \
  --region us-east-1
```

## System Requirements

- Python 3.7 or higher
- Internet connection (for AWS API calls and version checking)
- AWS credentials with appropriate permissions

## Next Steps

- See [USAGE_EXAMPLE.md](USAGE_EXAMPLE.md) for usage examples
- See [VERSION_UPDATE_FEATURE.md](VERSION_UPDATE_FEATURE.md) for auto-update details
- See [CUSTOMIZATION_SUMMARY.md](CUSTOMIZATION_SUMMARY.md) for customization info

