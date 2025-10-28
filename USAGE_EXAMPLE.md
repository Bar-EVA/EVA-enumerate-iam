# Usage Examples for Customized enumerate-iam

## Quick Start

### 1. Install Dependencies

```bash
cd EVA-enumerate-iam
pip install -r requirements.txt
```

Or using uv (as per user preferences):

```bash
cd EVA-enumerate-iam
uv pip install -r requirements.txt
```

### 2. Basic Usage

```bash
python enumerate-iam.py \
  --access-key AKIAIOSFODNN7EXAMPLE \
  --secret-key wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
  --region us-east-1
```

### 3. With Session Token (for temporary credentials)

```bash
python enumerate-iam.py \
  --access-key ASIAIOSFODNN7EXAMPLE \
  --secret-key wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
  --session-token AQoDYXdzEJr...<snip>...CRciCYEXAMPLEKEY \
  --region us-east-1
```

## What to Expect

### Console Output

The tool will:
1. Test IAM-specific operations first (get_user, list_roles, etc.)
2. Then brute-force test all 205 services with 1,024 operations
3. Show successful operations with "-- service.operation() worked!"
4. Log failed attempts (which is normal and expected)

Example output:
```
2025-10-28 10:30:15 - INFO - Starting permission enumeration for access-key-id "AKIA..."
2025-10-28 10:30:16 - INFO - -- User "test-user" has 2 attached policies
2025-10-28 10:30:17 - INFO - Attempting common-service describe / list brute force.
2025-10-28 10:30:18 - INFO - -- bedrock.list_foundation_models() worked!
2025-10-28 10:30:19 - INFO - -- s3.list_buckets() worked!
2025-10-28 10:30:20 - INFO - -- ec2.describe_instances() worked!
...
```

### Output Data

The tool returns a Python dictionary with two main sections:

```python
{
    "iam": {
        "iam.get_user": { ... },
        "iam.list_attached_user_policies": { ... },
        ...
    },
    "bruteforce": {
        "s3.list_buckets": { ... },
        "bedrock.list_foundation_models": { ... },
        "cost-optimization-hub.get_preferences": { ... },
        ...
    }
}
```

## Testing Specific New Services

### Test Bedrock Permissions

```bash
# The tool will automatically test these new Bedrock operations:
# - list_custom_models
# - list_foundation_models
# - list_guardrails
# - list_inference_profiles
# - get_model_invocation_logging_configuration
# ... and 9 more
```

### Test Cost Optimization Hub

```bash
# The tool will test:
# - list_enrollment_statuses
# - list_recommendation_summaries
# - get_preferences
```

### Test Geographic Services

```bash
# The tool will test:
# - geo-maps: get_map_style_descriptor, get_sprites, get_tile
# - geo-places: get_place, list_keys
# - geo-routes: get_routes
```

## Advanced Usage

### Programmatic Use

You can also use the tool as a Python library:

```python
from enumerate_iam.main import enumerate_iam

results = enumerate_iam(
    access_key='AKIAIOSFODNN7EXAMPLE',
    secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    session_token=None,
    region='us-east-1'
)

# Check what worked
for operation, result in results['bruteforce'].items():
    print(f"✓ {operation} succeeded")
    print(f"  Result: {result}")
```

### Filter Results for Specific Services

```python
from enumerate_iam.main import enumerate_iam

results = enumerate_iam(...)

# Find all Bedrock-related permissions
bedrock_ops = {k: v for k, v in results['bruteforce'].items() 
               if k.startswith('bedrock')}

print(f"Found {len(bedrock_ops)} Bedrock operations:")
for op in bedrock_ops:
    print(f"  - {op}")
```

### Save Results to JSON

```python
import json
from enumerate_iam.main import enumerate_iam

results = enumerate_iam(...)

with open('iam_enumeration_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("Results saved to iam_enumeration_results.json")
```

## Performance Notes

- The tool uses 25 concurrent threads for faster execution
- Typical run time: 2-5 minutes depending on permissions and region
- Services not available in your region are automatically skipped
- Failed operations don't affect successful ones

## Common Use Cases

### 1. Security Assessment
Verify what permissions are actually available to a set of credentials:
```bash
python enumerate-iam.py \
  --access-key $AWS_ACCESS_KEY_ID \
  --secret-key $AWS_SECRET_ACCESS_KEY \
  --region us-east-1 > assessment.log 2>&1
```

### 2. Troubleshooting Access Issues
Determine if credentials have access to specific services:
```bash
python enumerate-iam.py \
  --access-key $AWS_ACCESS_KEY_ID \
  --secret-key $AWS_SECRET_ACCESS_KEY \
  --region us-east-1 | grep "bedrock\|s3\|ec2"
```

### 3. Audit Temporary Credentials
Test STS temporary credentials:
```bash
# Get temporary credentials
CREDS=$(aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/MyRole \
  --role-session-name test-session)

# Extract credentials and test
python enumerate-iam.py \
  --access-key $(echo $CREDS | jq -r '.Credentials.AccessKeyId') \
  --secret-key $(echo $CREDS | jq -r '.Credentials.SecretAccessKey') \
  --session-token $(echo $CREDS | jq -r '.Credentials.SessionToken') \
  --region us-east-1
```

## Troubleshooting

### SSL Warnings
The tool disables SSL verification warnings by default (see line 204 in main.py). This is for testing purposes only.

### Region-Specific Services
Some newer services may only be available in specific regions. Try different regions:
- us-east-1 (N. Virginia) - Usually has most services
- us-west-2 (Oregon)
- eu-west-1 (Ireland)

### Rate Limiting
If you encounter rate limiting:
1. Reduce MAX_THREADS in main.py (default: 25)
2. Add delays between operations
3. Test during off-peak hours

## Security Considerations

⚠️ **Important Security Notes:**
- Only use this tool on credentials you own or have permission to test
- The tool makes many API calls that may be logged by AWS CloudTrail
- Some organizations may flag this activity as suspicious
- Consider running in a test/sandbox AWS account first
- Never share the tool's output as it may contain sensitive information

## New Services Coverage

With this customization, you can now enumerate permissions for:

**66 additional services** including:
- ✅ AI/ML: Bedrock, QApps, QConnect
- ✅ Cost Management: Cost Optimization Hub, Billing, Tax Settings
- ✅ Security: Control Catalog, Security IR, Inspector Scan
- ✅ Geographic: Geo-maps, Geo-places, Geo-routes
- ✅ Observability: Application Signals, Network Monitors
- ✅ And 51 more AWS services!

See `NEW_SERVICES_ADDED.md` for the complete list.

## Support

For issues or questions:
1. Check the original enumerate-iam documentation
2. Review AWS IAM documentation for permission requirements
3. Verify credentials and region availability
4. Check CloudTrail logs for detailed error information

---

**Happy IAM Enumerating! 🔐**

