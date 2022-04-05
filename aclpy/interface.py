#!/usr/bin/env python3
# interface.py
"""Arrowhead interface definition for the library.
"""

class ArrowheadInterface(object):
    """ArrowheadInterface class to store configuration about an interface.

    Attributes:
    name (str) -- name of the interface
    id (int) -- identification number of the interface, default -1 (not known)
    created_at (str) -- timestamp of interface creation, default ""
    updated_at (str) -- timestamp of the last interface update, default ""

    Note: Timestamp is given as '%Y-%m-%d %H-%M-%S'.
    """

    __slots__ = ["__name", "__id", "__created_at", "__updated_at"]

    def __init__(self, *,
            name: str,
            id: int = -1,
            created_at: str = "",
            updated_at: str = "",
    ):
        """Initialize ArrowheadInterface class."""
        super(ArrowheadInterface, self).__init__()

        self.__name = name
        self.__id = id
        self.__created_at = created_at
        self.__updated_at = updated_at


    # Attributes RO
    @property
    def name(self):
        return self.__name


    # Attributes RW
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, new_id):
        self.__id = new_id

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, new_value):
        self.__created_at = new_value

    @property
    def updated_at(self):
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, new_value):
        self.__updated_at = new_value


    # Attributes AHCore
    @property
    def interfaceName(self):
        return self.name

    @property
    def createdAt(self):
        return self.created_at

    @createdAt.setter
    def createdAt(self, new_value):
        self.created_at = new_value

    @property
    def updatedAt(self):
        return self.updated_at

    @updatedAt.setter
    def updatedAt(self, new_value):
        self.updated_at = new_value



    def update(self, **message):
        """Update the interface information using data received from the Arrowhead Core."""
        for key, value in message.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                pass
