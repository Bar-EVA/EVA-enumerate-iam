"""
Version checker for enumerate-iam
Checks for updates from the GitHub repository
"""
import logging
import requests
import json
from packaging import version as pkg_version

from enumerate_iam.__version__ import __version__, __repo_url__


def check_for_updates(timeout=3):
    """
    Check if a newer version is available on GitHub
    
    Args:
        timeout: HTTP request timeout in seconds
        
    Returns:
        dict: {
            'update_available': bool,
            'current_version': str,
            'latest_version': str,
            'download_url': str,
            'release_notes': str
        }
    """
    logger = logging.getLogger()
    
    result = {
        'update_available': False,
        'current_version': __version__,
        'latest_version': None,
        'download_url': None,
        'release_notes': None
    }
    
    try:
        # Extract owner and repo from URL
        # https://github.com/Bar-EVA/EVA-enumerate-iam -> Bar-EVA/EVA-enumerate-iam
        repo_path = __repo_url__.replace('https://github.com/', '').strip('/')
        
        # GitHub API endpoint for latest release
        api_url = f"https://api.github.com/repos/{repo_path}/releases/latest"
        
        logger.debug(f"Checking for updates at {api_url}")
        
        response = requests.get(api_url, timeout=timeout)
        
        if response.status_code == 404:
            # No releases yet, check commits instead
            logger.debug("No releases found, checking commits")
            return check_for_commits_update(repo_path, timeout)
        
        response.raise_for_status()
        
        release_data = response.json()
        latest_version = release_data.get('tag_name', '').lstrip('v')
        
        if not latest_version:
            logger.debug("Could not determine latest version")
            return result
        
        result['latest_version'] = latest_version
        result['download_url'] = release_data.get('html_url', __repo_url__)
        result['release_notes'] = release_data.get('body', '')
        
        # Compare versions
        try:
            if pkg_version.parse(latest_version) > pkg_version.parse(__version__):
                result['update_available'] = True
        except Exception as e:
            logger.debug(f"Version comparison failed: {e}")
            # Fallback to string comparison
            if latest_version != __version__:
                result['update_available'] = True
        
        return result
        
    except requests.exceptions.Timeout:
        logger.debug("Version check timed out")
    except requests.exceptions.RequestException as e:
        logger.debug(f"Could not check for updates: {e}")
    except Exception as e:
        logger.debug(f"Unexpected error checking for updates: {e}")
    
    return result


def check_for_commits_update(repo_path, timeout=3):
    """
    Check for updates by comparing commits when no releases exist
    
    Args:
        repo_path: GitHub repo path (owner/repo)
        timeout: HTTP request timeout in seconds
        
    Returns:
        dict: Update information
    """
    logger = logging.getLogger()
    
    result = {
        'update_available': False,
        'current_version': __version__,
        'latest_version': 'latest commit',
        'download_url': f"https://github.com/{repo_path}",
        'release_notes': None
    }
    
    try:
        # Get latest commit from master/main branch
        api_url = f"https://api.github.com/repos/{repo_path}/commits/master"
        response = requests.get(api_url, timeout=timeout)
        
        if response.status_code == 404:
            # Try 'main' branch
            api_url = f"https://api.github.com/repos/{repo_path}/commits/main"
            response = requests.get(api_url, timeout=timeout)
        
        response.raise_for_status()
        commit_data = response.json()
        
        latest_sha = commit_data.get('sha', '')[:7]
        commit_message = commit_data.get('commit', {}).get('message', '')
        
        if latest_sha:
            result['latest_version'] = f"commit {latest_sha}"
            result['release_notes'] = commit_message
            result['update_available'] = True  # Assume update available if we can fetch commits
        
        return result
        
    except Exception as e:
        logger.debug(f"Could not check commits: {e}")
    
    return result


def print_update_notification(update_info):
    """
    Print a user-friendly update notification
    
    Args:
        update_info: dict from check_for_updates()
    """
    logger = logging.getLogger()
    
    if not update_info['update_available']:
        return
    
    logger.info("")
    logger.info("=" * 70)
    logger.info("🎉 UPDATE AVAILABLE!")
    logger.info(f"Current version: {update_info['current_version']}")
    logger.info(f"Latest version:  {update_info['latest_version']}")
    logger.info("")
    logger.info(f"Download: {update_info['download_url']}")
    
    if update_info['release_notes']:
        notes = update_info['release_notes'][:200]
        if len(update_info['release_notes']) > 200:
            notes += "..."
        logger.info(f"Release notes: {notes}")
    
    logger.info("")
    logger.info("To update, run:")
    logger.info("  cd /path/to/EVA-enumerate-iam")
    logger.info("  git pull origin master")
    logger.info("  pip install -r requirements.txt")
    logger.info("=" * 70)
    logger.info("")


def check_and_notify():
    """
    Convenience function to check for updates and print notification
    """
    update_info = check_for_updates()
    print_update_notification(update_info)
    return update_info

