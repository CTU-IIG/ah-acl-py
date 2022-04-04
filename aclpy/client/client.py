#!/usr/bin/env python3
# client.py
"""Arrowhead client definition.
"""

import json

from typing import Tuple, List

from aclpy.connector.connector import ArrowheadConnector
from aclpy.messages import *
from aclpy.service import ArrowheadService
from aclpy.system import ArrowheadSystem


class ArrowheadClient(ArrowheadSystem):
    """ArrowheadClient class for attaching a connector to system.

    Additional attributes:
    connector (ArrowheadConnector) -- class for handling the requests
    """

    def __init__(self, name: str, address: str, port: int, pubkey: str, connector: ArrowheadConnector):
        """Initialize ArrowheadClient class."""
        super(ArrowheadClient, self).__init__(
            name = name,
            address = address,
            port = port,
            pubkey = pubkey,
        )

        self.connector = connector


    def register_service(self, service: ArrowheadService) -> bool:
        """Register a service for this client.

        Arguments:
        service (ArrowheadService) -- service to be registered

        Returns:
        success (bool) -- True when registration is successful
        """
        msg = build_register_service("HTTP-INSECURE-JSON", self, service)

        success, status_code, payload = self.connector.register_service(self, msg)

        return success


    def unregister_service(self, service: ArrowheadService) -> bool:
        """Unregister a service for this client.

        Arguments:
        service (ArrowheadService) -- service to be unregistered

        Returns:
        success (bool) -- True when unregistration is successful
        """
        msg = build_unregister_service(self, service)

        success, status_code, payload = self.connector.unregister_service(self, msg)

        return success


    def register_system(self) -> bool:
        """Register this system inside Arrowhead Core.

        Returns:
        success (bool) -- True when registration is successful
        """
        msg = build_register_system(self)

        success, status_code, payload = self.connector.register_system(self, msg)

        return success


    def orchestrate(self, service: ArrowheadService) -> Tuple[bool, List[ArrowheadSystem]]:
        """Use Core Orchestrator to locate providers of the required 'service'.

        Arguments:
        service (ArrowheadService) -- service to be located

        Returns:
        success (bool) -- True when registration is successful
        providers (List[ArrowheadSystem]) -- list of available providers
        """
        msg = build_orchestration_request("HTTP-INSECURE-JSON", self, service)

        success, status_code, payload = self.connector.orchestrate(self, msg)

        if not success:
            return (False, [])
        else:
            if len(payload.get("response")) > 0:
                return (True, [
                    ArrowheadSystem(
                        address = system.get("provider").get("address"),
                        port = system.get("provider").get("port"),
                        name = system.get("provider").get("name"),
                        pubkey = system.get("provider").get("authenticationInfo"),
                    ) for system in payload.get("response")
                ])

            else:
                return (True, [])
