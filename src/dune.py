"""
Simple Dune Analytics helper.
Just pass a query ID and get your data.
"""

from .setup import get_secret


def get_dune_client():
    """Get an initialized Dune client."""
    from dune_client.client import DuneClient

    api_key = get_secret('DUNE_API_KEY')
    if not api_key:
        raise ValueError("DUNE_API_KEY not found. Add it to Colab Secrets or .env file.")

    return DuneClient(api_key)


def run_query(query_id: int):
    """
    Get the latest result for a Dune query.

    Args:
        query_id: The Dune query ID (from the URL)

    Returns:
        Query result as a pandas DataFrame
    """
    client = get_dune_client()
    result = client.get_latest_result(query_id)
    return result.result.rows


def run_query_df(query_id: int):
    """
    Get the latest result for a Dune query as a pandas DataFrame.

    Args:
        query_id: The Dune query ID (from the URL)

    Returns:
        pandas DataFrame with the query results
    """
    import pandas as pd

    rows = run_query(query_id)
    return pd.DataFrame(rows)
