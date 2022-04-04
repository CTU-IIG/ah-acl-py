#!/usr/bin/env python3
# system.py
"""Arrowhead system definition for the library.
"""

class ArrowheadSystem(object):
    """ArrowheadSystem class to store information about the system.

    Attributes:
    name (str) -- name of the system
    address (str) -- address IP / name of the system
    port (int) -- port that the system is attached to
    pubkey (str) -- public key of the system, "" by default

    Note: When using the system as connect only, feel free to use port 0.
    """

    __slots__ = ["name", "address", "port", "pubkey"]

    def __init__(self, *,
            name: str,
            address: str,
            port: int,
            pubkey: str = ""
    ):
        """Initialize ArrowheadSystem class."""
        super(ArrowheadSystem, self).__init__()

        self.name = name
        self.address = address
        self.port = port
        self.pubkey = pubkey
