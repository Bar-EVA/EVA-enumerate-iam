#!/usr/bin/env python
"""
EVA enumerate-iam - AWS IAM Permission Enumerator

Automatically checks GitHub for service database updates and downloads new services.
"""
import argparse

from enumerate_iam.main import enumerate_iam
from enumerate_iam.__version__ import __version__


def main():
    parser = argparse.ArgumentParser(
        description=f'Enumerate IAM permissions (v{__version__})'
    )

    parser.add_argument('--access-key', help='AWS access key', required=True)
    parser.add_argument('--secret-key', help='AWS secret key', required=True)
    parser.add_argument('--session-token', help='STS session token')
    parser.add_argument('--region', help='AWS region to send API requests to', default='us-east-1')
    parser.add_argument('--no-update-check', action='store_true', 
                       help='Skip checking for service database updates')
    parser.add_argument('--rate-limit', type=float, default=0.0,
                       help='Global requests per second across all threads (0 = unlimited)')

    args = parser.parse_args()

    # Check for service database updates (unless disabled)
    if not args.no_update_check:
        try:
            from enumerate_iam.version_checker import check_and_notify
            update_result = check_and_notify()
            
            # If services were updated, warn and exit so user can restart
            if update_result.get('updated'):
                print("\n⚠️  Service database was updated. Please run the command again.")
                print("   This ensures the new services are loaded properly.\n")
                return
                
        except Exception as e:
            # Silently fail if update check fails - don't block main functionality
            pass

    # Run the enumeration
    enumerate_iam(args.access_key,
                  args.secret_key,
                  args.session_token,
                  args.region,
                  rate_limit=args.rate_limit)


if __name__ == '__main__':
    main()
