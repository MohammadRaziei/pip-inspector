"""Utility functions for pip-inspector."""

import urllib.request
import urllib.error
from typing import Optional


def fetch_url_content(url: str, timeout: int = 10) -> Optional[str]:
    """
    Fetch content from a URL using built-in Python libraries.
    
    This function uses urllib.request to fetch web page content and automatically
    handles redirects. It sets appropriate headers to mimic a real browser.
    
    Args:
        url: The URL to fetch content from
        timeout: Request timeout in seconds (default: 10)
        
    Returns:
        The page content as string, or None if an error occurs
        
    Raises:
        ValueError: If the URL is invalid
        urllib.error.URLError: For network-related errors
        urllib.error.HTTPError: For HTTP errors (404, 500, etc.)
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    # Set up headers to mimic a real browser
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ),
        'Accept': (
            'text/html,application/xhtml+xml,application/xml;q=0.9,'
            'image/webp,*/*;q=0.8'
        ),
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        # Create request with headers
        request = urllib.request.Request(url, headers=headers)
        
        # Open URL with timeout - urllib automatically handles redirects
        with urllib.request.urlopen(request, timeout=timeout) as response:
            # Read and decode the response
            content = response.read()
            
            # Try to detect encoding from headers, fallback to utf-8
            encoding = response.headers.get_content_charset() or 'utf-8'
            
            # Decode the content
            decoded_content = content.decode(encoding, errors='replace')
            
            return decoded_content
            
    except urllib.error.HTTPError as e:
        # Handle HTTP errors (404, 500, etc.)
        print(f"HTTP Error {e.code}: {e.reason} for URL: {url}")
        return None
    except urllib.error.URLError as e:
        # Handle URL errors (network issues, invalid URL, etc.)
        print(f"URL Error: {e.reason} for URL: {url}")
        return None
    except ValueError as e:
        # Handle invalid URL format
        print(f"Value Error: {e} for URL: {url}")
        return None
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e} for URL: {url}")
        return None
