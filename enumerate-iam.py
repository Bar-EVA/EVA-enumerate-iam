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
from datetime import datetime, timezone


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
        
        # Debug: Show what keys are available
        print(f"🔍 Found credential keys: {list(creds.keys())}")
        
        # Map the fields (note: AWS Cognito uses "SecretKey" not "SecretAccessKey")
        access_key = creds.get('AccessKeyId')
        secret_key = creds.get('SecretKey') or creds.get('SecretAccessKey')
        session_token = creds.get('SessionToken')
        
        # Strip whitespace and validate
        if access_key:
            access_key = str(access_key).strip()
        if secret_key:
            secret_key = str(secret_key).strip()
        if session_token:
            session_token = str(session_token).strip()
        
        if not access_key or not secret_key:
            print("❌ Error: AccessKeyId or SecretKey not found in credentials")
            sys.exit(1)
        
        # Check if temporary credentials (starting with ASIA) require session token
        if access_key.startswith('ASIA'):
            if not session_token:
                print("❌ Error: AccessKeyId starts with 'ASIA' (temporary credentials) but no SessionToken found")
                print("   Temporary credentials REQUIRE a SessionToken to work")
                sys.exit(1)
        elif not session_token:
            print("⚠️  Warning: No SessionToken found (may be required for temporary credentials)")
        
        print(f"✅ Loaded credentials from file: {file_path}")
        print(f"   AccessKeyId:   {access_key}")
        print(f"   SecretKey:     {secret_key[:30]}...{secret_key[-10:]}")
        if session_token:
            print(f"   SessionToken:  {session_token[:80]}...{session_token[-20:]}")
        
        # Check expiration time if available
        expiration = creds.get('Expiration')
        if expiration:
            try:
                # Handle both Unix timestamp (as number) and ISO format strings
                if isinstance(expiration, (int, float)):
                    expire_time = datetime.fromtimestamp(expiration, tz=timezone.utc)
                else:
                    expire_time = datetime.fromisoformat(str(expiration).replace('Z', '+00:00'))
                
                now = datetime.now(timezone.utc)
                time_remaining = expire_time - now
                minutes_remaining = int(time_remaining.total_seconds() / 60)
                
                if minutes_remaining < 0:
                    print(f"   ⚠️  Expiration:   ALREADY EXPIRED!")
                    print(f"   Note: Get fresh credentials before running scan")
                elif minutes_remaining < 30:
                    print(f"   ⚠️  Expiration:   {minutes_remaining} minutes remaining (may not complete scan)")
                else:
                    print(f"   ⏰ Expiration:   {minutes_remaining} minutes remaining")
            except Exception as e:
                print(f"   ⏰ Expiration:   {expiration} (could not parse)")
        
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
