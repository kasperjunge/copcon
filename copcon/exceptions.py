"""Custom Exceptions for Copcon.

This module defines custom exception classes used throughout the Copcon application.
"""


class FileReadError(Exception):
    """Exception raised when a file cannot be read."""

    pass


class ClipboardError(Exception):
    """Exception raised when clipboard operations fail."""

    pass
