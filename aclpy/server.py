#!/usr/bin/env python3
# server.py
"""Arrowhead server configuration for the library.
"""

class ArrowheadServer(object):
    """ArrowheadServer class for storing configuration about used Arrowhead Core server.

    Attributes:
    address (str) -- IP address of the core server, localhost by default
    orchestrator_port (int) -- port of the Orchestrator system, 8441 by default
    orchestrator_url (str) -- direct url to the Orchestrator master endpoint, None
    serviceregistry_port (int) -- port of the Service Registry system, 8443 by default
    serviceregistry_url (str) -- direct url to the Service Registry master endpoint, None
    authorization_port (int) -- port of the Authorization system, 8445 by default
    authorization_url (str) -- direct url to the Authorization master endpoint, None

    Note: When '_url' is not provided, it is generated from 'address' and '_port'.
    """

    __slots__ = ["address", "orchestrator", "serviceregistry", "authorization"]

    def __init__(self, *,
            address: str = "127.0.0.1",
            orchestrator_port: int = 8441,
            orchestrator_url: str = None,
            serviceregistry_port: int = 8443,
            serviceregistry_url: str = None,
            authorization_port: int = 8445,
            authorization_url: str = None,
        ):
        """Initialize ArrowheadServer class."""
        super(ArrowheadServer, self).__init__()

        # Core IP
        self.address = address


        # Core Systems
        self.orchestrator = {
            "port": orchestrator_port,
            "endpoint": "orchestrator",
            "url": orchestrator_url,
        }
        self.serviceregistry = {
            "port": serviceregistry_port,
            "endpoint": "serviceregistry",
            "url": serviceregistry_url,
        }
        self.authorization = {
            "port": authorization_port,
            "endpoint": "authorization",
            "url": authorization_url,
        }


    def get_url(self, core_system: str):
        """Get URL for the 'core_system'.

        Arguments:
        core_system -- name of the system, str

        Returns:
        url -- URL to the system (with trailing slash), str
        """

        if hasattr(self, core_system):
            system = getattr(self, core_system)
            if system.get("url"):
                return system.get("url")
            return "https://" + self.address + ":" + str(system.get("port")) + "/" + system.get("endpoint") + "/"
        else:
            raise ValueError("Undefined core system '%s'." % core_system)
