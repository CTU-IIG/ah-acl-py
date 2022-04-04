#!/usr/bin/env python3
# service.py
"""Arrowhead service definition for the library.
"""

class ArrowheadService(object):
    """ArrowheadService class to store configuration about a service.

    Attributes:
    name (str) -- name of the service
    version (int) -- version of the service, 1 by default
    """

    __slots__ = ["name", "version"]

    def __init__(self, *,
            name: str,
            version: int = 1
    ):
        """Initialize ArrowheadService class."""
        super(ArrowheadService, self).__init__()

        self.name = name
        self.version = version
