# EVA enumerate-iam Customization Summary

## Overview

Successfully customized the enumerate-iam tool by adding **66 new AWS service checks** to the existing bruteforce tests.

## Changes Made

### File Modified
- **`enumerate_iam/bruteforce_tests.py`**
  - Added 66 new AWS services with their respective list/describe/get operations
  - Removed duplicate entries (gamelift, workspaces)
  - Maintained alphabetical ordering within the file structure

### Statistics

| Metric | Value |
|--------|-------|
| **Total Services Now Supported** | 205 |
| **New Services Added** | 66 |
| **Total API Operations** | 1,024 |
| **Average Operations per Service** | 5.0 |

## New Services Added

All 66 requested services have been successfully added:

✓ aiops  
✓ application-signals  
✓ apptest  
✓ arc-zonal-shift  
✓ backupsearch  
✓ bcm-pricing-calculator  
✓ bedrock  
✓ bedrock-agent-runtime  
✓ bedrock-data-automation  
✓ bedrock-data-automation-runtime  
✓ billing  
✓ controlcatalog  
✓ cost-optimization-hub  
✓ deadline  
✓ ds-data  
✓ dsql  
✓ entityresolution  
✓ evs  
✓ freetier  
✓ geo-maps  
✓ geo-places  
✓ geo-routes  
✓ inspector-scan  
✓ iot-data  
✓ iot1click-projects  
✓ keyspaces  
✓ kinesis-video-webrtc-storage  
✓ mailmanager  
✓ marketplace-agreement  
✓ marketplace-deployment  
✓ marketplace-reporting  
✓ medical-imaging  
✓ mpa  
✓ neptune-graph  
✓ networkflowmonitor  
✓ networkmonitor  
✓ notifications  
✓ notificationscontacts  
✓ observabilityadmin  
✓ odb  
✓ osis  
✓ partnercentral-selling  
✓ pca-connector-scep  
✓ pcs  
✓ qapps  
✓ qconnect  
✓ repostspace  
✓ route53profiles  
✓ s3tables  
✓ s3outposts  
✓ s3express  
✓ sagemaker-edge  
✓ sagemaker-metrics  
✓ security-ir  
✓ socialmessaging  
✓ ssm-contacts  
✓ ssm-guiconnect  
✓ ssm-incidents  
✓ ssm-quicksetup  
✓ supplychain  
✓ taxsettings  
✓ timestream-influxdb  
✓ trustedadvisor  
✓ voice-id  
✓ workspaces-thin-client  
✓ workspaces-web

## Validation Results

All tests passed successfully:
- ✓ All 205 services load correctly
- ✓ All 1,024 operations are properly formatted
- ✓ No syntax errors in Python code
- ✓ All new services verified present in BRUTEFORCE_TESTS
- ✓ Data structure integrity maintained

## Usage

The tool usage remains the same. Install dependencies first:

```bash
pip install -r requirements.txt
```

Then run the tool:

```bash
python enumerate-iam.py \
  --access-key YOUR_ACCESS_KEY \
  --secret-key YOUR_SECRET_KEY \
  --region us-east-1
```

Or with session tokens:

```bash
python enumerate-iam.py \
  --access-key YOUR_ACCESS_KEY \
  --secret-key YOUR_SECRET_KEY \
  --session-token YOUR_SESSION_TOKEN \
  --region us-east-1
```

## What the Tool Does

The enumerate-iam tool:

1. **Tests IAM Permissions**: Attempts to call various AWS API operations to determine what permissions are available to given credentials
2. **Uses Safe Operations**: Only calls read-only operations (list, describe, get) that don't modify resources
3. **Parallel Execution**: Uses threading (25 concurrent threads) for faster enumeration
4. **Comprehensive Coverage**: Now tests 205 AWS services with 1,024 different operations
5. **Handles Failures Gracefully**: Automatically handles services not available in specific regions or operations that fail due to permissions

## Key Features of Added Services

### New Service Categories Covered:

1. **AI/ML Services**: Bedrock suite, QApps, QConnect
2. **Observability**: Application Signals, Network Monitors, Observability Admin
3. **Cost Management**: Billing, Cost Optimization Hub, Tax Settings
4. **Security**: Control Catalog, Security IR, Inspector Scan
5. **Geographic Services**: Geo-maps, Geo-places, Geo-routes
6. **Data Services**: DSQL, Neptune Graph, Timestream InfluxDB
7. **Messaging**: Mail Manager, Social Messaging
8. **Marketplace**: Agreement, Deployment, Reporting
9. **Healthcare**: Medical Imaging, MPA
10. **WorkSpaces**: Thin Client, Web variants

## Technical Details

### Operation Selection Criteria

Operations were selected based on:
- No required input parameters (or all parameters optional)
- Safe read-only operations (list, describe, get methods)
- Standard AWS API naming conventions
- AWS CLI documentation compatibility

### Service Name Mapping

Service names use AWS boto3 client naming conventions:
- Hyphens for multi-word services (e.g., `bedrock-agent`)
- Lowercase naming
- Matches boto3's `client()` service parameter

## References

- Based on [AWS Bedrock CLI Documentation](https://docs.aws.amazon.com/cli/latest/reference/bedrock/)
- AWS boto3 SDK service names
- AWS IAM Permission reference

## Notes

- Some services may not be available in all regions
- The tool automatically skips unavailable services
- Failed operations are logged but don't stop enumeration
- Results provide insight into actual IAM permissions available to credentials

---

**Customization completed successfully!** ✓

For detailed information about each service and its operations, see `NEW_SERVICES_ADDED.md`.

