from typing import Union
from urllib.parse import ParseResult, urlparse

import tldextract


def bytes_to_gigabytes(bytes_value: int) -> float:
    """Convert bytes to gigabytes."""
    return bytes_value / (1024**3)


def humanize_bytes(num_bytes: Union[int, float]) -> str:
    """
    Convert a number of bytes into a human-readable
    """
    result = humanize_bytes_0(num_bytes)
    # 505.00 Kb -> 505 Kb
    result = result.replace(".00", "")
    return result


def humanize_bytes_0(num_bytes: Union[int, float]) -> str:
    """
    Convert a number of bytes into a human-readable format (e.g., KB, MB, GB).

    Args:
        num_bytes: Number of bytes

    Return:
        Human-readable string
    """
    if num_bytes < 1024:
        return f"{num_bytes} bytes"
    elif num_bytes < 1024**2:
        return f"{num_bytes / 1024:.2f} Kb"
    elif num_bytes < 1024**3:
        return f"{num_bytes / 1024**2:.2f} Mb"
    elif num_bytes < 1024**4:
        return f"{num_bytes / 1024**3:.2f} Gb"
    else:
        return f"{num_bytes / 1024**4:.2f} Tb"


def get_tld(url: str) -> str:
    """
    Get the top-level domain (TLD) of a URL.

    Args:
        url: The URL to extract the TLD from.

    Returns:
        The TLD of the URL, or an empty string if it cannot be determined.

    Examples:
    > get_tld("https://api.epa.gov/easey/bulk-files")
    "gov"
    > get_tld("https://www.example.com")
    "com"
    > get_tld("http://example.co.uk")
    "co.uk"
    > get_tld("ftp://example")
    ""
    """
    extracted = tldextract.extract(url)
    return extracted.suffix


def is_valid_url(url: str) -> Union[bool, ParseResult]:
    """
    Is this a valid URL, for our puposes?

    Args:
        url: The URL to check.

    Returns:
        True if the URL is valid, False otherwise.

    Examples:
    > is_valid_url("https://api.epa.gov/easey/bulk-files")
    True
    > is_valid_url("https://api.epa.gov/easey/bulk-files/")
    True
    > is_valid_url("Bob")
    False
    """
    parsed = urlparse(url)
    if all([parsed.scheme, parsed.netloc]) and get_tld(url):
        return parsed
    return False
