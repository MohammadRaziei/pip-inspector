"""Tests for pip_inspector.utils module."""

import pytest
from unittest.mock import patch, MagicMock
import urllib.request
import urllib.error

from pip_inspector.utils import fetch_url_content


class TestFetchUrlContent:
    """Test cases for fetch_url_content function."""
    
    def test_invalid_url_raises_value_error(self):
        """Test that invalid URLs raise ValueError."""
        with pytest.raises(ValueError):
            fetch_url_content("")
        
        with pytest.raises(ValueError):
            fetch_url_content(None)  # type: ignore
    
    @patch('pip_inspector.utils.urllib.request.urlopen')
    def test_successful_fetch(self, mock_urlopen):
        """Test successful URL content fetching."""
        # Mock response
        mock_response = MagicMock()
        mock_response.read.return_value = b"<html>Test content</html>"
        mock_response.headers.get_content_charset.return_value = 'utf-8'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Call function
        result = fetch_url_content("https://example.com")
        
        # Verify result
        assert result == "<html>Test content</html>"
        
        # Verify request was made with correct headers
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        assert request.get_full_url() == "https://example.com"
        assert 'User-agent' in request.headers
    
    @patch('pip_inspector.utils.urllib.request.urlopen')
    def test_fetch_with_different_encoding(self, mock_urlopen):
        """Test fetching content with different encoding."""
        # Mock response with different encoding
        mock_response = MagicMock()
        mock_response.read.return_value = "Test content with special chars: ñáéíóú".encode('utf-8')
        mock_response.headers.get_content_charset.return_value = 'utf-8'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Call function
        result = fetch_url_content("https://example.com")
        
        # Verify result
        assert result == "Test content with special chars: ñáéíóú"
    
    @patch('pip_inspector.utils.urllib.request.urlopen')
    def test_fetch_with_fallback_encoding(self, mock_urlopen):
        """Test fetching content with fallback encoding."""
        # Mock response without charset in headers
        mock_response = MagicMock()
        mock_response.read.return_value = b"Test content"
        mock_response.headers.get_content_charset.return_value = None
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Call function
        result = fetch_url_content("https://example.com")
        
        # Verify result (should use utf-8 as fallback)
        assert result == "Test content"
    
    @patch('pip_inspector.utils.urllib.request.urlopen')
    def test_http_error_handling(self, mock_urlopen):
        """Test handling of HTTP errors."""
        # Mock HTTP 404 error
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://example.com", 404, "Not Found", {}, None
        )
        
        # Call function
        result = fetch_url_content("https://example.com")
        
        # Verify None is returned for HTTP errors
        assert result is None
    
    @patch('pip_inspector.utils.urllib.request.urlopen')
    def test_url_error_handling(self, mock_urlopen):
        """Test handling of URL errors."""
        # Mock URL error (e.g., network issue)
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")
        
        # Call function
        result = fetch_url_content("https://example.com")
        
        # Verify None is returned for URL errors
        assert result is None
    
    @patch('pip_inspector.utils.urllib.request.urlopen')
    def test_timeout_parameter(self, mock_urlopen):
        """Test that timeout parameter is passed correctly."""
        # Mock response
        mock_response = MagicMock()
        mock_response.read.return_value = b"Test content"
        mock_response.headers.get_content_charset.return_value = 'utf-8'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Call function with custom timeout
        result = fetch_url_content("https://example.com", timeout=30)
        
        # Verify timeout was passed
        mock_urlopen.assert_called_once()
        call_args = mock_urlopen.call_args
        assert call_args[1]['timeout'] == 30
    
    @patch('pip_inspector.utils.urllib.request.urlopen')
    def test_headers_are_set(self, mock_urlopen):
        """Test that appropriate headers are set."""
        # Mock response
        mock_response = MagicMock()
        mock_response.read.return_value = b"Test content"
        mock_response.headers.get_content_charset.return_value = 'utf-8'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Call function
        fetch_url_content("https://example.com")
        
        # Verify headers were set
        request = mock_urlopen.call_args[0][0]
        headers = request.headers
        
        assert 'User-agent' in headers
        assert 'Accept' in headers
        assert 'Accept-language' in headers
        assert headers['User-agent'].startswith('Mozilla/5.0')
