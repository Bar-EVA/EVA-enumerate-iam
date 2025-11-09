#!/usr/bin/env python
"""
EVA enumerate-iam - AWS IAM Permission Enumerator

Automatically pulls latest updates from GitHub before execution.
"""
import argparse
import sys
import subprocess
import os
import json
import re


def parse_request_file(file_path):
    """
    Parse AWS credentials from a request file containing HTTP response with JSON body.
    
    Expected JSON format in the response body:
    {
        "Credentials": {
            "AccessKeyId": "...",
            "SecretKey": "...",
            "SessionToken": "...",
            ...
        }
    }
    
    Returns: tuple (access_key, secret_key, session_token)
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find JSON in the content (skip HTTP headers if present)
        # Look for the opening brace of the JSON object
        json_start = content.find('{')
        if json_start == -1:
            print("❌ Error: No JSON found in request file")
            sys.exit(1)
        
        json_content = content[json_start:]
        
        # Parse the JSON
        try:
            data = json.loads(json_content)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in request file: {e}")
            sys.exit(1)
        
        # Extract credentials
        if 'Credentials' not in data:
            print("❌ Error: 'Credentials' key not found in JSON")
            sys.exit(1)
        
        creds = data['Credentials']
        
        # Map the fields (note: AWS Cognito uses "SecretKey" not "SecretAccessKey")
        access_key = creds.get('AccessKeyId')
        secret_key = creds.get('SecretKey') or creds.get('SecretAccessKey')
        session_token = creds.get('SessionToken')
        
        if not access_key or not secret_key:
            print("❌ Error: AccessKeyId or SecretKey not found in credentials")
            sys.exit(1)
        
        print(f"✅ Loaded credentials from file: {file_path}")
        print(f"   AccessKeyId: {access_key[:20]}...")
        if session_token:
            print(f"   SessionToken: {session_token[:50]}...")
        print()
        
        return access_key, secret_key, session_token
        
    except FileNotFoundError:
        print(f"❌ Error: Request file not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error parsing request file: {e}")
        sys.exit(1)


def main():
    # Auto-update: Pull latest changes from GitHub BEFORE any imports
    print("🔄 Checking for updates from GitHub...", flush=True)
    try:
        # Get the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Run git pull
        result = subprocess.run(
            ['git', 'pull', 'origin', 'master'],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if 'Already up to date' in output:
                print("✅ Already up to date")
            elif output:
                print(f"📥 Updated from GitHub:")
                print(f"   {output}")
            print()
    except subprocess.TimeoutExpired:
        print("⚠️  Git pull timed out, continuing anyway...\n")
    except Exception as e:
        # Show error but don't block
        print(f"⚠️  Could not check for updates: {type(e).__name__}\n")

    # Import after git pull to ensure latest code is loaded
    from enumerate_iam.main import enumerate_iam
    from enumerate_iam.__version__ import __version__

    # Parse arguments
    parser = argparse.ArgumentParser(
        description=f'Enumerate IAM permissions (v{__version__})',
        epilog='''
Regenerating Service List:
  To regenerate the complete list of AWS services from the SDK:
    cd enumerate_iam/
    git clone https://github.com/aws/aws-sdk-js.git
    python generate_bruteforce_tests.py
    rm -rf aws-sdk-js
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('-r', '--request', help='Path to file containing AWS credentials (HTTP response with JSON)')
    parser.add_argument('--access-key', help='AWS access key')
    parser.add_argument('--secret-key', help='AWS secret key')
    parser.add_argument('--session-token', help='STS session token')
    parser.add_argument('--region', help='AWS region to send API requests to', default='us-east-1')
    parser.add_argument('--rate-limit', type=float, default=0.0,
                       help='Global requests per second across all threads (0 = unlimited)')

    args = parser.parse_args()

    # Determine credential source
    if args.request:
        # Parse credentials from file
        access_key, secret_key, session_token = parse_request_file(args.request)
        
        # Override with command-line args if provided
        if args.access_key:
            access_key = args.access_key
        if args.secret_key:
            secret_key = args.secret_key
        if args.session_token:
            session_token = args.session_token
    else:
        # Require credentials from command line
        if not args.access_key or not args.secret_key:
            parser.error('--access-key and --secret-key are required when not using --request')
        
        access_key = args.access_key
        secret_key = args.secret_key
        session_token = args.session_token

    # Run the enumeration
    enumerate_iam(access_key,
                  secret_key,
                  session_token,
                  args.region,
                  rate_limit=args.rate_limit)


if __name__ == '__main__':
    main()
