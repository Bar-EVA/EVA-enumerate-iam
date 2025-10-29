#!/usr/bin/env python
"""
EVA enumerate-iam - AWS IAM Permission Enumerator

Automatically checks GitHub for service database updates and downloads new services.
"""
import argparse
import sys

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
    parser.add_argument('--update', action='store_true',
                       help='Force check and update service database, then exit')
    parser.add_argument('--rate-limit', type=float, default=0.0,
                       help='Global requests per second across all threads (0 = unlimited)')

    # If help is requested, print help and also show update status (check-only)
    if any(flag in sys.argv[1:] for flag in ('-h', '--help')):
        parser.print_help()
        try:
            from enumerate_iam.version_checker import check_services_status
            status = check_services_status(timeout=3)
            if status.get('has_update'):
                print("\nℹ️  Service database update available:")
                print(f"   Local:  {status.get('current_services', 0)} services")
                print(f"   Remote: {status.get('github_services', 0)} services")
                added = status.get('added_services') or []
                if added:
                    preview = ", ".join(sorted(added)[:5])
                    more = f" ... (+{len(added)-5})" if len(added) > 5 else ""
                    print(f"   New:    {preview}{more}")
            else:
                print(f"\n✅ Service database is up to date ({status.get('current_services', 0)} services)")
        except Exception:
            # Do not block help if status check fails
            pass
        return

    args = parser.parse_args()

    # Force update mode
    if args.update:
        try:
            from enumerate_iam.version_checker import check_and_update_services
            result = check_and_update_services()
            if result.get('updated'):
                print("\n✅ Service database updated successfully.")
                print(f"   Current services: {result.get('new_services', 0)}")
                print("   Please re-run the command to load the new services.\n")
            else:
                print("\n✅ Service database is already up to date.")
                print(f"   Services: {result.get('current_services', 0)}\n")
        except Exception:
            pass
        return

    # Default: Check for service database updates (auto)
    try:
        from enumerate_iam.version_checker import check_and_notify
        update_result = check_and_notify()
        
        # If services were updated, warn and exit so user can restart
        if update_result.get('updated'):
            print("\n⚠️  Service database was updated. Please run the command again.")
            print("   This ensures the new services are loaded properly.\n")
            return
            
    except Exception:
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
