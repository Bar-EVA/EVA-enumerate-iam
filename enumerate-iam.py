#!/usr/bin/env python
"""
EVA enumerate-iam - AWS IAM Permission Enumerator

Automatically pulls latest updates from GitHub before execution.
"""
import argparse
import sys
import subprocess
import os


def main():
    # Auto-update: Pull latest changes from GitHub BEFORE any imports
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
            if 'Already up to date' not in output and output:
                print(f"📥 Updated from GitHub:")
                print(f"   {output}")
                print()
    except Exception:
        # Silently fail if git pull fails - don't block main functionality
        pass

    # Import after git pull to ensure latest code is loaded
    from enumerate_iam.main import enumerate_iam
    from enumerate_iam.__version__ import __version__

    # Parse arguments
    parser = argparse.ArgumentParser(
        description=f'Enumerate IAM permissions (v{__version__})'
    )

    parser.add_argument('--access-key', help='AWS access key', required=True)
    parser.add_argument('--secret-key', help='AWS secret key', required=True)
    parser.add_argument('--session-token', help='STS session token')
    parser.add_argument('--region', help='AWS region to send API requests to', default='us-east-1')
    parser.add_argument('--rate-limit', type=float, default=0.0,
                       help='Global requests per second across all threads (0 = unlimited)')

    args = parser.parse_args()

    # Run the enumeration
    enumerate_iam(args.access_key,
                  args.secret_key,
                  args.session_token,
                  args.region,
                  rate_limit=args.rate_limit)


if __name__ == '__main__':
    main()
