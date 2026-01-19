# Colab Notebooks

A collection of Google Colab notebooks with shared setup and utilities.

## Project Structure

```
colab-notebooks/
├── notebooks/          # Your Colab notebooks
│   └── template.ipynb  # Template to copy for new notebooks
├── src/                # Shared Python utilities
│   ├── __init__.py
│   └── setup.py        # Environment setup and API helpers
├── requirements.txt    # Python dependencies
└── README.md
```

## Setup

### 1. Push to GitHub

```bash
cd colab-notebooks
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/m0xt64/colab-notebooks.git
git push -u origin main
```

### 2. Configure Colab Secrets

In Google Colab, add your API keys using the Secrets feature:

1. Open any notebook in Colab
2. Click the **key icon** in the left sidebar
3. Add your secrets:
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `ANTHROPIC_API_KEY` - Your Anthropic API key
   - Add any other custom API keys you need

Secrets are stored securely in your Google account and available across all your Colab sessions.

### 3. Using in Notebooks

Copy `notebooks/template.ipynb` for new notebooks. Each notebook starts with:

```python
# Clone repo and install dependencies
!git clone https://github.com/m0xt64/colab-notebooks.git /content/repo 2>/dev/null || true
%cd /content/repo
!pip install -q -r requirements.txt

# Add src to path
import sys
sys.path.insert(0, '/content/repo')

# Import shared utilities
from src import get_secret, get_openai_client, get_anthropic_client
```

## Available Utilities

### `get_secret(key)`
Retrieve a secret from Colab Secrets:
```python
api_key = get_secret('MY_CUSTOM_API_KEY')
```

### `get_openai_client()`
Get an initialized OpenAI client:
```python
client = get_openai_client()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### `get_anthropic_client()`
Get an initialized Anthropic client:
```python
client = get_anthropic_client()
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### `make_api_request(url, method, headers, json, api_key_secret)`
Make HTTP requests to custom APIs:
```python
from src.setup import make_api_request

response = make_api_request(
    url='https://api.example.com/data',
    method='POST',
    json={'query': 'test'},
    api_key_secret='MY_API_KEY'
)
```

## Adding Dependencies

Add new packages to `requirements.txt` and commit to GitHub. The setup cell will install them automatically.
