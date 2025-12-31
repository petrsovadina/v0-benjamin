"""
Pytest configuration and fixtures for backend tests.

This file sets up warning filters for third-party library deprecation warnings
that are unrelated to our LangChain upgrade.
"""
import warnings
import sys


def pytest_configure(config):
    """
    Configure warning filters before test collection.

    This hook runs before pytest collects tests, allowing us to filter
    third-party deprecation warnings that occur at import time.
    """
    # Filter third-party deprecation warnings at import time
    # These warnings come from the supabase -> storage3 -> pyiceberg -> pyparsing chain
    # and are unrelated to our LangChain code
    warnings.filterwarnings(
        "ignore",
        message=".*enablePackrat.*",
        category=DeprecationWarning,
    )
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        module=r"pyparsing.*"
    )
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        module=r"pyiceberg.*"
    )


# Also apply filters immediately at module import
warnings.filterwarnings(
    "ignore",
    message=".*enablePackrat.*",
    category=DeprecationWarning,
)
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module=r"pyparsing.*"
)
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module=r"pyiceberg.*"
)
