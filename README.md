# EVA enumerate-iam

> AWS IAM permission enumeration tool with 311 services and 1,999 operations

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/Bar-EVA/EVA-enumerate-iam)
[![AWS Services](https://img.shields.io/badge/AWS_Services-311-orange.svg)](#services)
[![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)](LICENSE)

## Quick Start

```bash
# Install
git clone https://github.com/Bar-EVA/EVA-enumerate-iam.git
cd EVA-enumerate-iam
pip install -r requirements.txt

# Run
./enumerate-iam.py --access-key AKIA... --secret-key SECRET... --region us-east-1
```

## What It Does

Discovers IAM permissions by testing **311 AWS services** with **1,999 read-only operations** (list, describe, get). All operations are non-destructive and won't modify your AWS resources.

## Features

- ✅ **311 AWS Services** - Most comprehensive coverage available
- ✅ **Auto-Update** - Downloads new services from GitHub automatically
- ✅ **Fast** - 25 concurrent threads
- ✅ **Safe** - Read-only operations only
- ✅ **Smart** - Skips unavailable services/regions

## Installation

### With Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./enumerate-iam.py --help
```

### EC2 machine Quick Install
```bash
sudo apt-get update && sudo apt-get install -y python3-pip git
git clone https://github.com/Bar-EVA/EVA-enumerate-iam.git
cd EVA-enumerate-iam
pip3 install -r requirements.txt
chmod +x enumerate-iam.py
```

## Usage

### Basic
```bash
./enumerate-iam.py \
  --access-key AKIA... \
  --secret-key SECRET... \
  --region us-east-1
```

### With Session Token (Temporary Credentials)
```bash
./enumerate-iam.py \
  --access-key ASIA... \
  --secret-key SECRET... \
  --session-token TOKEN... \
  --region us-east-1
```

### With Rate Limiting
```bash
./enumerate-iam.py \
  --access-key AKIA... \
  --secret-key SECRET... \
  --rate-limit 100
```

### From Request File
Load credentials directly from an HTTP response file (e.g., AWS Cognito response):
```bash
./enumerate-iam.py -r credentials.txt
```

**Example file format:**
```
HTTP/2 200 OK
Date: Sun, 09 Nov 2025 07:25:52 GMT
Content-Type: application/x-amz-json-1.1

{"Credentials":{"AccessKeyId":"AKIA...","SecretKey":"...","SessionToken":"..."}}
```

The parser automatically extracts credentials from the JSON body, skipping HTTP headers.

## CLI Options

```
-h, --help            show this help message and exit
-r REQUEST, --request REQUEST
                      Path to file containing AWS credentials (HTTP response with JSON)
--access-key ACCESS_KEY
                      AWS access key
--secret-key SECRET_KEY
                      AWS secret key
--session-token SESSION_TOKEN
                      STS session token
--region REGION       AWS region to send API requests to (default: us-east-1)
--rate-limit RATE_LIMIT
                      Global requests per second across all threads (0 = unlimited)
```

**Note:** Either use `-r/--request` to load credentials from a file, OR provide `--access-key` and `--secret-key` directly.

## Auto-Update Feature

The tool automatically pulls the latest updates from GitHub before each run:

```bash
🔄 Checking for updates from GitHub...
✅ Already up to date

# OR if updates are available:

🔄 Checking for updates from GitHub...
📥 Updated from GitHub:
   Updating 5dd9480..78af30e
   Fast-forward
    enumerate_iam/main.py | 11 +++++++++++
    1 file changed, 11 insertions(+)
```

- **What updates:** Pulls all latest changes from the repository
- **When:** On every execution (always runs before any command)
- **How:** Runs `git pull origin master` automatically
- **Safe:** Standard git pull, won't overwrite uncommitted local changes

## Services Coverage

### Total: 311 Services | 1,999 Operations

#### AI/ML & Bedrock (19 ops)
`bedrock` `bedrock-agent` `bedrock-agent-runtime` `bedrock-data-automation` `qapps` `qconnect`

#### Compute (120+ ops)
`ec2` `lambda` `ecs` `eks` `batch` `lightsail` `autoscaling`

#### Storage & Database (90+ ops)
`s3` `rds` `dynamodb` `elasticache` `neptune-graph` `dsql` `timestream-influxdb`

#### Security & Identity (80+ ops)
`iam` `accessanalyzer` `guardduty` `security-ir` `inspector` `kms` `secretsmanager` `trustedadvisor`

#### Networking (70+ ops)
`vpc` `cloudfront` `route53` `directconnect` `globalaccelerator` `networkmonitor`

#### Cost & Billing (15+ ops)
`billing` `cost-optimization-hub` `freetier` `taxsettings` `pricing`

#### Geographic Services (6 ops)
`geo-maps` `geo-places` `geo-routes`

#### Analytics (50+ ops)
`athena` `glue` `kinesis` `redshift` `quicksight`

#### Developer Tools (40+ ops)
`codebuild` `codecommit` `codedeploy` `codepipeline`

#### And 150+ More Services...

<details>
<summary>View all 311 services</summary>

`a4b` `accessanalyzer` `acm` `aiops` `amplify` `apigateway` `application-signals` `appmesh` `appstream2` `appsync` `apptest` `arc-zonal-shift` `athena` `autoscaling` `backup` `backupsearch` `batch` `bcm-data-exports` `bcm-pricing-calculator` `bedrock` `bedrock-agent` `bedrock-agent-runtime` `bedrock-data-automation` `bedrock-data-automation-runtime` `billing` `chime` `cloud9` `clouddirectory` `cloudformation` `cloudfront` `cloudhsm` `cloudhsmv2` `cloudsearch` `cloudtrail` `codebuild` `codecommit` `codedeploy` `codepipeline` `codestar` `cognito-sync` `comprehend` `config` `controlcatalog` `cost-optimization-hub` `cur` `data.mediastore` `datapipeline` `datasync` `dax` `deadline` `devicefarm` `devices.iot1click` `directconnect` `discovery` `dlm` `dms` `ds` `ds-data` `dsql` `dynamodb` `ec2` `ecr` `ecs` `eks` `elasticache` `elasticbeanstalk` `elasticfilesystem` `elasticloadbalancing` `elasticmapreduce` `elastictranscoder` `email` `entityresolution` `es` `events` `evs` `firehose` `fms` `freetier` `fsx` `gamelift` `geo-maps` `geo-places` `geo-routes` `globalaccelerator` `glue` `greengrass` `guardduty` `health` `iam` `importexport` `inspector` `inspector-scan` `iot` `iot-data` `iot1click-projects` `iotanalytics` `kafka` `keyspaces` `kinesis` `kinesis-video-webrtc-storage` `kinesisanalytics` `kinesisvideo` `kms` `lambda` `license-manager` `lightsail` `logs` `machinelearning` `macie` `mailmanager` `marketplace-agreement` `marketplace-deployment` `marketplace-reporting` `mediaconnect` `mediaconvert` `medialive` `mediapackage` `mediastore` `mediatailor` `medical-imaging` `mgh` `mobile` `models.lex` `monitoring` `mpa` `mq` `mturk-requester` `neptune-graph` `networkflowmonitor` `networkmonitor` `notifications` `notificationscontacts` `observabilityadmin` `odb` `opsworks` `opworks` `organizations` `osis` `partnercentral-selling` `pca-connector-scep` `pcs` `pinpoint` `polly` `pricing` `projects.iot1click` `qapps` `qconnect` `ram` `rds` `redshift` `rekognition` `repostspace` `resource-groups` `robomaker` `route53` `route53domains` `route53profiles` `route53resolver` `s3` `s3express` `s3outposts` `s3tables` `sagemaker` `sagemaker-edge` `sagemaker-metrics` `sdb` `secretsmanager` `security-ir` `securityhub` `serverlessrepo` `servicecatalog` `shield` `signer` `sms` `sms-voice.pinpoint` `snowball` `sns` `socialmessaging` `sqs` `ssm` `ssm-contacts` `ssm-guiconnect` `ssm-incidents` `ssm-quicksetup` `states` `storagegateway` `streams.dynamodb` `sts` `supplychain` `support` `tagging` `taxsettings` `timestream-influxdb` `transcribe` `transfer` `translate` `trustedadvisor` `voice-id` `waf` `waf-regional` `workdocs` `worklink` `workmail` `workspaces` `workspaces-thin-client` `workspaces-web` `xray`

</details>

## Example Output

```
2025-10-28 10:30:15 - INFO - Starting permission enumeration for access-key-id "AKIA..."
2025-10-28 10:30:16 - INFO - User "admin" has 2 attached policies
2025-10-28 10:30:17 - INFO - Attempting common-service describe / list brute force.
2025-10-28 10:30:18 - INFO - -- bedrock.list_foundation_models() worked!
2025-10-28 10:30:19 - INFO - -- s3.list_buckets() worked!
2025-10-28 10:30:20 - INFO - -- ec2.describe_instances() worked!
2025-10-28 10:30:21 - INFO - -- iam.list_users() worked!
```

## Comparison with Other Tools

| Feature | EVA enumerate-iam | cliam | enumerate-iam (original) |
|---------|------------------|-------|-------------------------|
| **AWS Services** | 311 | ~100 | ~139 |
| **Operations** | 1,999 | ~500 | ~879 |
| **Auto-Update** | ✅ | ❌ | ❌ |
| **Language** | Python | Go | Python |
| **Multi-Cloud** | AWS only | AWS/GCP/Azure | AWS only |
| **Latest Services** | ✅ Bedrock, etc | ❌ | ❌ |

## Contributing

Found a missing AWS service? Add it to `enumerate_iam/bruteforce_tests.py`:

```python
"service-name": [
    "list_resources",
    "describe_config",
    "get_status"
],
```

## Regenerating Service List

To regenerate the complete list of AWS services and operations from the AWS SDK:

```bash
cd enumerate_iam/
git clone https://github.com/aws/aws-sdk-js.git
python generate_bruteforce_tests.py
rm -rf aws-sdk-js
```

This will analyze the AWS SDK and generate an updated `bruteforce_tests.py` with all available read-only operations.

## Credits

- **Original Author**: Andrés Riancho ([@andresriancho](https://github.com/andresriancho))
- **Original Repo**: [andresriancho/enumerate-iam](https://github.com/andresriancho/enumerate-iam)
- **This Fork**: Enhanced with 68+ new services and auto-update
- **Comparison**: Analyzed against [cliam](https://github.com/securisec/cliam) for completeness

## License

GPL-3.0 - See [LICENSE](LICENSE)

## Links

- **Repository**: https://github.com/Bar-EVA/EVA-enumerate-iam
- **Issues**: https://github.com/Bar-EVA/EVA-enumerate-iam/issues
- **Original Tool**: https://github.com/andresriancho/enumerate-iam

---

**EVA enumerate-iam v2.0.0** | 311 Services | 1,999 Operations | Industry-Leading Coverage
