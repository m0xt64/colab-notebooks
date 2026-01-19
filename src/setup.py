"""
Shared setup utilities for Colab notebooks.
Handles environment setup, secrets management, and API client initialization.
"""

import os
import sys

def is_colab() -> bool:
    """Check if running in Google Colab."""
    return 'google.colab' in sys.modules


def setup_environment(repo_url: str = None, install_requirements: bool = True):
    """
    Set up the Colab environment.

    Args:
        repo_url: GitHub repo URL to clone (optional, uses current repo if None)
        install_requirements: Whether to install requirements.txt
    """
    if not is_colab():
        print("Not running in Colab, skipping environment setup")
        return

    from google.colab import userdata

    # Clone repo if URL provided and not already cloned
    if repo_url and not os.path.exists('/content/repo'):
        os.system(f'git clone {repo_url} /content/repo')
        sys.path.insert(0, '/content/repo')
        os.chdir('/content/repo')

    # Install requirements
    if install_requirements and os.path.exists('requirements.txt'):
        os.system('pip install -q -r requirements.txt')

    print("Environment setup complete!")


def get_secret(key: str, default: str = None) -> str:
    """
    Get a secret from Colab Secrets or environment variables.

    Args:
        key: The secret key name (e.g., 'OPENAI_API_KEY')
        default: Default value if secret not found

    Returns:
        The secret value
    """
    # Try Colab Secrets first
    if is_colab():
        try:
            from google.colab import userdata
            return userdata.get(key)
        except (ImportError, Exception):
            pass

    # Fall back to environment variable
    return os.environ.get(key, default)


def get_openai_client():
    """
    Initialize and return an OpenAI client using Colab Secrets.

    Returns:
        OpenAI client instance
    """
    from openai import OpenAI

    api_key = get_secret('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in Colab Secrets. "
                        "Add it via the key icon in the left sidebar.")

    return OpenAI(api_key=api_key)


def get_anthropic_client():
    """
    Initialize and return an Anthropic client using Colab Secrets.

    Returns:
        Anthropic client instance
    """
    from anthropic import Anthropic

    api_key = get_secret('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in Colab Secrets. "
                        "Add it via the key icon in the left sidebar.")

    return Anthropic(api_key=api_key)


def make_api_request(url: str, method: str = 'GET', headers: dict = None,
                     json: dict = None, api_key_secret: str = None):
    """
    Make an HTTP request to a custom API.

    Args:
        url: The API endpoint URL
        method: HTTP method (GET, POST, etc.)
        headers: Optional headers dict
        json: Optional JSON body for POST/PUT requests
        api_key_secret: Name of the Colab Secret containing the API key

    Returns:
        Response object
    """
    import requests

    headers = headers or {}

    if api_key_secret:
        api_key = get_secret(api_key_secret)
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'

    response = requests.request(method, url, headers=headers, json=json)
    response.raise_for_status()
    return response
