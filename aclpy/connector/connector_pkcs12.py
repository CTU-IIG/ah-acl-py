#!/usr/bin/env python3
# connector_pkcs12.py
"""Connector / interface to Arrowhead Core using .p12 certificates.
"""

import requests_pkcs12

from typing import Dict, Tuple

from aclpy.connector.connector import ArrowheadConnector as ArrowheadConnectorBase
from aclpy.server import ArrowheadServer
from aclpy.client.client import ArrowheadClient


class ArrowheadConnector(ArrowheadConnectorBase):
    """ArrowheadConnector class to handle requests to Arrowhead Core using pkcs12."""

    def _orchestrate(self, system: ArrowheadClient, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        """Request available providers from the Orchestrator.

        Arguments:
        system (ArrowheadSystem) -- system requesting the orchestration
        message (Dict[str, any]) -- message to be sent to the Orchestrator

        Returns:
        status_code (int) -- HTTP code from the response
        response (Dict[str, any]) -- message received from the Orchestrator

        Note: 'message' is created by 'aclpy.messages.build_orchestration_request'.
        """
        res = requests_pkcs12.post(
            self.server.get_url("orchestrator") + "orchestration",
            json = message,
            pkcs12_filename = system.p12file,
            pkcs12_password = system.p12pass,
            verify = system.cafile,
            timeout = self.timeout,
        )

        return (res.status_code, res.json())


    def _register_service(self, system: ArrowheadClient, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        """Register a service for 'system' to the Service Registry.

        Arguments:
        system (ArrowheadSystem) -- system for service registration
        message (Dict[str, any]) -- message to be sent to the Service Registry

        Returns:
        status_code (int) -- HTTP code from the response
        response (Dict[str, any]) -- message received from the Service Registry

        Note: 'message' is created by 'aclpy.messages.build_register_service'.
        """
        res = requests_pkcs12.post(
            self.server.get_url("serviceregistry") + "register",
            json = message,
            pkcs12_filename = system.p12file,
            pkcs12_password = system.p12pass,
            verify = system.cafile,
            timeout = self.timeout,
        )

        return (res.status_code, res.json())


    def _unregister_service(self, system: ArrowheadClient, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        """Unregister a service for 'system' to the Service Registry.

        Arguments:
        system (ArrowheadSystem) -- system for service unregistration
        message (Dict[str, any]) -- message to be sent to the Service Registry

        Returns:
        status_code (int) -- HTTP code from the response
        response (Dict[str, any]) -- message received from the Service Registry

        Note: 'message' is created by 'aclpy.messages.build_unregister_service'.
        """
        res = requests_pkcs12.delete(
            self.server.get_url("serviceregistry")
                + "unregister?"
                + "&".join(
                    ["%s=%s" % (key, value) for key, value in message.items()]
                ),
            pkcs12_filename = system.p12file,
            pkcs12_password = system.p12pass,
            verify = system.cafile,
            timeout = self.timeout,
        )

        return (res.status_code, {})


    def _register_system(self, system: ArrowheadClient, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        """Register a 'system' to Arrowhead Core via Service Registry.

        Arguments:
        system (ArrowheadSystem) -- system for registration
        message (Dict[str, any]) -- message to be sent to the Service Registry

        Returns:
        status_code (int) -- HTTP code from the response
        response (Dict[str, any]) -- message received from the Service Registry

        Note: 'message' is created by 'aclpy.messages.build_register_system'.
        """
        res = requests_pkcs12.post(
            self.server.get_url("serviceregistry") + "register-system",
            json = message,
            pkcs12_filename = system.p12file,
            pkcs12_password = system.p12pass,
            verify = system.cafile,
            timeout = self.timeout,
        )

        return (res.status_code, res.json())
