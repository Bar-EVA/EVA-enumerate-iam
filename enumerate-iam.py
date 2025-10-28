#!/usr/bin/env python
import argparse

from enumerate_iam.main import enumerate_iam
from enumerate_iam.version_checker import check_and_notify
from enumerate_iam.__version__ import __version__


def main():
    parser = argparse.ArgumentParser(
        description=f'Enumerate IAM permissions (v{__version__})'
    )

    parser.add_argument('--access-key', help='AWS access key', required=True)
    parser.add_argument('--secret-key', help='AWS secret key', required=True)
    parser.add_argument('--session-token', help='STS session token')
    parser.add_argument('--region', help='AWS region to send API requests to', default='us-east-1')
    parser.add_argument('--no-version-check', action='store_true', 
                       help='Skip checking for newer versions')

    args = parser.parse_args()

    # Check for updates (unless disabled)
    if not args.no_version_check:
        try:
            check_and_notify()
        except Exception:
            # Silently fail if version check fails - don't block the main functionality
            pass

    enumerate_iam(args.access_key,
                  args.secret_key,
                  args.session_token,
                  args.region)


if __name__ == '__main__':
    main()
