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
    id (int) -- identification number of the system, default -1 (not known)
    created_at (str) -- timestamp of system creation, default ""
    updated_at (str) -- timestamp of the last system update, default ""

    Note: When using the system as connect only, feel free to use port 0.
    Note: Timestamp is given as '%Y-%m-%d %H-%M-%S'.
    """

    __slots__ = ["__name", "__address", "__port", "__pubkey", "__id", "__created_at", "__updated_at"]

    def __init__(self, *,
            name: str,
            address: str,
            port: int,
            pubkey: str = "",
            id: int = -1,
            created_at: str = "",
            updated_at: str = "",
    ):
        """Initialize ArrowheadSystem class."""
        super(ArrowheadSystem, self).__init__()

        self.__name = name
        self.__address = address
        self.__port = port
        self.__pubkey = pubkey
        self.__id = id
        self.__created_at = created_at
        self.__updated_at = updated_at
