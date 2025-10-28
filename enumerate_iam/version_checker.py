"""
Service database checker for enumerate-iam
Checks GitHub for updates to bruteforce_tests.py and auto-downloads if needed
"""
import logging
import requests
import os
import tempfile
import shutil

from enumerate_iam.__version__ import __repo_url__


def check_and_update_services(timeout=5):
    """
    Check GitHub for updates to bruteforce_tests.py and download if more services available
    
    Args:
        timeout: HTTP request timeout in seconds
        
    Returns:
        dict: {
            'updated': bool,
            'current_services': int,
            'new_services': int,
            'added_services': list
        }
    """
    logger = logging.getLogger()
    
    result = {
        'updated': False,
        'current_services': 0,
        'new_services': 0,
        'added_services': []
    }
    
    try:
        # Get current service count
        from enumerate_iam.bruteforce_tests import BRUTEFORCE_TESTS
        current_services = set(BRUTEFORCE_TESTS.keys())
        result['current_services'] = len(current_services)
        
        # Extract repo path
        repo_path = __repo_url__.replace('https://github.com/', '').strip('/')
        
        # GitHub raw content URL for bruteforce_tests.py
        raw_url = f"https://raw.githubusercontent.com/{repo_path}/master/enumerate_iam/bruteforce_tests.py"
        
        logger.debug(f"Checking for service updates at {raw_url}")
        
        # Download the file from GitHub
        response = requests.get(raw_url, timeout=timeout)
        response.raise_for_status()
        
        github_content = response.text
        
        # Parse the GitHub version to count services
        github_services = parse_services_from_content(github_content)
        result['new_services'] = len(github_services)
        
        # Check if GitHub has more services
        new_services = github_services - current_services
        
        if new_services:
            result['added_services'] = sorted(list(new_services))
            logger.info("")
            logger.info("=" * 70)
            logger.info(f"🎉 SERVICE DATABASE UPDATE AVAILABLE!")
            logger.info(f"Current services: {result['current_services']}")
            logger.info(f"GitHub services:  {result['new_services']}")
            logger.info(f"New services:     {len(new_services)}")
            logger.info("")
            logger.info("New services found:")
            for svc in sorted(new_services)[:10]:
                logger.info(f"  + {svc}")
            if len(new_services) > 10:
                logger.info(f"  ... and {len(new_services) - 10} more")
            logger.info("")
            logger.info("Downloading updated service database...")
            
            # Download and replace the file
            if download_and_replace_bruteforce(github_content):
                result['updated'] = True
                logger.info("✅ Service database updated successfully!")
                logger.info(f"   Added {len(new_services)} new services")
                logger.info("")
                logger.info("⚠️  Please restart the tool to use new services")
            else:
                logger.info("⚠️  Could not update service database automatically")
                logger.info("   Run: git pull origin master")
            
            logger.info("=" * 70)
            logger.info("")
        else:
            logger.debug(f"Service database is up to date ({result['current_services']} services)")
        
        return result
        
    except requests.exceptions.Timeout:
        logger.debug("Service check timed out")
    except requests.exceptions.RequestException as e:
        logger.debug(f"Could not check for service updates: {e}")
    except Exception as e:
        logger.debug(f"Unexpected error checking services: {e}")
    
    return result


def parse_services_from_content(content):
    """
    Parse service names from bruteforce_tests.py content
    
    Args:
        content: File content as string
        
    Returns:
        set: Set of service names
    """
    services = set()
    
    # Simple parser - look for lines like:    "service-name": [
    import re
    pattern = r'^\s*"([^"]+)":\s*\['
    
    for line in content.split('\n'):
        match = re.match(pattern, line)
        if match:
            service_name = match.group(1)
            # Exclude the dict name itself
            if service_name != 'BRUTEFORCE_TESTS':
                services.add(service_name)
    
    return services


def download_and_replace_bruteforce(content):
    """
    Replace the local bruteforce_tests.py with new content
    
    Args:
        content: New file content
        
    Returns:
        bool: True if successful
    """
    try:
        # Get the path to bruteforce_tests.py
        import enumerate_iam.bruteforce_tests as bf_module
        bf_path = bf_module.__file__
        
        # Create backup
        backup_path = bf_path + '.backup'
        shutil.copy2(bf_path, backup_path)
        
        # Write new content
        with open(bf_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Verify it's valid Python
        try:
            compile(content, bf_path, 'exec')
            return True
        except SyntaxError:
            # Restore backup if invalid
            shutil.copy2(backup_path, bf_path)
            return False
        
    except Exception as e:
        logging.getLogger().debug(f"Could not replace bruteforce_tests.py: {e}")
        return False


def check_and_notify():
    """
    Main entry point - check for service updates and auto-download
    """
    return check_and_update_services()

