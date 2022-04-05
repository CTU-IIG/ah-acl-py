#!/usr/bin/env python3
# system.py
"""Arrowhead system definition for the library.
"""

from typing import List

from aclpy.interface import ArrowheadInterface


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

    __slots__ = ["__name", "__address", "__port", "__pubkey", "__id", "__created_at", "__updated_at", "__interfaces"]

    def __init__(self, *,
            name: str,
            address: str,
            port: int,
            pubkey: str = "",
            id: int = -1,
            created_at: str = "",
            updated_at: str = "",
            interfaces: List[ArrowheadInterface] = [],
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
        self.__interfaces = interfaces


    # Attributes RO
    @property
    def name(self):
        return self.__name

    @property
    def address(self):
        return self.__address

    @property
    def port(self):
        return self.__port

    @property
    def pubkey(self):
        return self.__pubkey

    @property
    def interfaces(self):
        return self.__interfaces


    # Attributes RW
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, new_id: int):
        self.__id = new_id

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, new_value: str):
        self.__created_at = new_value

    @property
    def updated_at(self):
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, new_value: str):
        self.__updated_at = new_value


    # Attributes AHCore
    @property
    def systemName(self):
        return self.name

    @property
    def authenticationInfo(self):
        return self.pubkey

    @property
    def createdAt(self):
        return self.created_at

    @createdAt.setter
    def createdAt(self, new_value: str):
        self.created_at = new_value

    @property
    def updatedAt(self):
        return self.updated_at

    @updatedAt.setter
    def updatedAt(self, new_value: str):
        self.updated_at = new_value



    def update(self, **message):
        """Update the system information using data received from the Arrowhead Core."""
        for key, value in message.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                pass
