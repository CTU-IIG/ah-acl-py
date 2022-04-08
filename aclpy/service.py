#!/usr/bin/env python3
# service.py
"""Arrowhead service definition for the library.
"""

from typing import Dict


class ArrowheadService(object):
    """ArrowheadService class to store configuration about a service.

    Attributes:
    name (str) -- name of the service
    version (int) -- version of the service, 1 by default
    id (int) -- identification number of the service, default -1 (not known)
    created_at (str) -- timestamp of service creation, default ""
    updated_at (str) -- timestamp of the last service update, default ""
    metadata (Dict[str, any]) -- additional information about the service

    Note: Timestamp is given as '%Y-%m-%d %H-%M-%S'.
    """

    __slots__ = ["__name", "__version", "__id", "__created_at", "__updated_at", "__metadata"]

    def __init__(self, *,
            name: str,
            version: int = 1,
            id: int = -1,
            created_at: str = "",
            updated_at: str = "",
            metadata: Dict[str, any] = {},
    ):
        """Initialize ArrowheadService class."""
        super(ArrowheadService, self).__init__()

        self.__name = name
        self.__version = version
        self.__id = id
        self.__created_at = created_at
        self.__updated_at = updated_at
        self.__metadata = metadata


    # Attributes RO
    @property
    def name(self):
        return self.__name

    @property
    def version(self):
        return self.__version


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

    @property
    def metadata(self):
        return self.__metadata

    @metadata.setter
    def metadata(self, new_value):
        self.__metadata = new_value


    # Attributes AHCore
    @property
    def serviceDefinition(self):
        return self.name

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


    # Has attributes
    def has_metadata(self):
        return len(self.metadata) != 0


    def update(self, **message):
        """Update the service information using data received from the Arrowhead Core."""
        for key, value in message.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                pass
