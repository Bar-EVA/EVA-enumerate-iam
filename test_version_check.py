#!/usr/bin/env python3
"""
Test script for version checking feature
Run this to see how the version check works
"""

# Mock the version checker if dependencies aren't installed
try:
    from enumerate_iam.version_checker import check_for_updates, print_update_notification
    from enumerate_iam.__version__ import __version__
    
    print("=" * 70)
    print("Testing version check feature...")
    print("=" * 70)
    print(f"\nCurrent version: {__version__}")
    print("\nChecking for updates...")
    
    update_info = check_for_updates(timeout=5)
    
    if update_info['update_available']:
        print("\n✅ Update found!")
        print_update_notification(update_info)
    else:
        print("\n✅ No updates available - you're on the latest version!")
        print(f"   Current: {update_info['current_version']}")
        if update_info['latest_version']:
            print(f"   Latest:  {update_info['latest_version']}")
    
except ImportError as e:
    print("=" * 70)
    print("Dependencies not installed yet!")
    print("=" * 70)
    print(f"\nError: {e}")
    print("\nPlease install dependencies first:")
    print("  pip install -r requirements.txt")
    print("\nOr use uv:")
    print("  uv pip install -r requirements.txt")
    print("\n" + "=" * 70)

