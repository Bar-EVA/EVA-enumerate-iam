# Using the `-r/--request` Flag

## Overview
The `-r` or `--request` flag allows you to load AWS credentials directly from a file containing an HTTP response. This is particularly useful when working with AWS Cognito Identity Pool responses or similar credential endpoints.

## Usage

### Basic Usage
```bash
./enumerate-iam.py -r credentials.txt
```

### With Additional Options
```bash
./enumerate-iam.py -r credentials.txt --region eu-north-1 --rate-limit 100
```

### Override Credentials from File
You can load from file and override specific values:
```bash
./enumerate-iam.py -r credentials.txt --session-token "different-token"
```

## File Format

The parser automatically extracts credentials from JSON in the file, skipping any HTTP headers.

### Example 1: Full HTTP Response
```
HTTP/2 200 OK
Date: Sun, 09 Nov 2025 07:25:52 GMT
Content-Type: application/x-amz-json-1.1
Content-Length: 1509

{"Credentials":{"AccessKeyId":"ASIARO6KSBSTB7OKVJRT","SecretKey":"H4ss5lQlfO7FsfXd87erb2Yc7wwmOUSeThSvtMy3","SessionToken":"IQoJb3JpZ2lu..."}}
```

### Example 2: JSON Only
```json
{
  "Credentials": {
    "AccessKeyId": "ASIARO6KSBSTB7OKVJRT",
    "SecretKey": "H4ss5lQlfO7FsfXd87erb2Yc7wwmOUSeThSvtMy3",
    "SessionToken": "IQoJb3JpZ2lu...",
    "Expiration": 1762676752
  }
}
```

## Supported Credential Fields

The parser looks for these fields in the `Credentials` object:
- `AccessKeyId` - AWS Access Key ID (required)
- `SecretKey` or `SecretAccessKey` - AWS Secret Key (required)
- `SessionToken` - STS Session Token (optional)

## Output

When loading credentials from file, you'll see:
```
✅ Loaded credentials from file: credentials.txt
   AccessKeyId: ASIARO6KSBSTB7OKVJ...
   SessionToken: IQoJb3JpZ2luX2VjEB8aCmV1LW5vcnRoLTEiSDBGAiEA5pzD...
```

## Error Handling

The parser provides clear error messages:
- ❌ Request file not found
- ❌ No JSON found in request file
- ❌ Invalid JSON format
- ❌ Missing required credentials

## Security Note

⚠️ **Important:** Never commit credential files to version control!

The repository automatically ignores files matching `*credentials*.txt`. Always use this naming convention for your credential files.

