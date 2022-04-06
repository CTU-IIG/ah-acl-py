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


    @property
    def last_error(self):
        return self.connector.last_error


    def register_service(self, service: ArrowheadService) -> bool:
        """Register a service for this client.

        Arguments:
        service (ArrowheadService) -- service to be registered

        Returns:
        success (bool) -- True when registration is successful
        """
        msg = build_register_service(
            interfaces = self.interfaces,
            system = self,
            service = service
        )

        success, status_code, payload = self.connector.register_service(self, msg)

        if success:
            self.update(**payload.get("provider"))
            service.update(**payload.get("serviceDefinition"))

            for interface in self.interfaces:
                for _interface in payload.get("interfaces"):
                    if interface.name == _interface.get("interfaceName"):
                        interface.update(**_interface)

        return success


    def unregister_service(self, service: ArrowheadService) -> bool:
        """Unregister a service for this client.

        Arguments:
        service (ArrowheadService) -- service to be unregistered

        Returns:
        success (bool) -- True when unregistration is successful
        """
        msg = build_unregister_service(
            system = self,
            service = service
        )

        success, status_code, payload = self.connector.unregister_service(self, msg)

        return success


    def register_system(self) -> bool:
        """Register this system inside Arrowhead Core.

        Returns:
        success (bool) -- True when registration is successful
        """
        msg = build_register_system(system = self)

        success, status_code, payload = self.connector.register_system(self, msg)

        if success:
            self.update(**payload)

        return success


    def orchestrate(self, service: ArrowheadService) -> Tuple[bool, List[ArrowheadSystem]]:
        """Use Core Orchestrator to locate providers of the required 'service'.

        Arguments:
        service (ArrowheadService) -- service to be located

        Returns:
        success (bool) -- True when registration is successful
        providers (List[ArrowheadSystem]) -- list of available providers
        """
        msg = build_orchestration_request(
            interfaces = self.interfaces,
            system = self,
            service = service
        )

        success, status_code, payload = self.connector.orchestrate(self, msg)

        if not success:
            return (False, [])
        else:
            if len(payload.get("response")) > 0:
                return (True, [
                    ArrowheadSystem(
                        address = system.get("provider").get("address"),
                        port = system.get("provider").get("port"),
                        name = system.get("provider").get("systemName"),
                        pubkey = system.get("provider").get("authenticationInfo"),
                        id = system.get("provider").get("id"),
                        created_at = system.get("provider").get("createdAt"),
                        updated_at = system.get("provider").get("updatedAt"),
                    ) for system in payload.get("response")
                ])

            else:
                return (True, [])


    def obtain_id(self, service_name: str = "dummy") -> bool:
        """Obtain the ID of this client.

        Arguments:
        service_name (str) -- name of the service used to obtain system id, dummy by default

        Returns:
        success (bool) -- True when id was successfully received
        """

        service = ArrowheadService(
            name = service_name
        )

        # Register a service
        success = self.register_service(service)

        # If not successful, we try to unregister service first.
        if not success:
            if not self.unregister_service(service):
                return False

            success = self.register_service(service)

        # Clean after ourselves.
        self.unregister_service(service)

        return success and self.id >= 0
