#!/usr/bin/env python3
# connector_pkcs12.py
"""Connector / interface to Arrowhead Core using .p12 certificates.
"""
import requests_pkcs12

from typing import Dict, Tuple

from aclpy.connector.connectorabc import ConnectorABC
from aclpy.server import ArrowheadServer
from aclpy.client import ArrowheadClient


class ArrowheadConnector(ConnectorABC):

    def _orchestrate(self, system: ArrowheadClient, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        res = requests_pkcs12.post(
            self.server.get_url("orchestrator") + "orchestration",
            json = message,
            pkcs12_filename = system.p12file,
            pkcs12_password = system.p12pass,
            verify = system.cafile,
        )

        return (res.status_code, res.json())


    def _register_service(self, system: ArrowheadClient, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        res = requests_pkcs12.post(
            self.server.get_url("serviceregistry") + "register",
            json = message,
            pkcs12_filename = system.p12file,
            pkcs12_password = system.p12pass,
            verify = system.cafile,
        )

        return (res.status_code, res.json())


    def _unregister_service(self, system: ArrowheadClient, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        res = requests_pkcs12.delete(
            self.server.get_url("serviceregistry")
                + "unregister?"
                + "&".join(
                    ["%s=%s" % (key, value) for key, value in message.items()]
                ),
            pkcs12_filename = system.p12file,
            pkcs12_password = system.p12pass,
            verify = system.cafile,
        )

        return (res.status_code, res.json())


    def _register_system(self, system: ArrowheadClient, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        res = requests_pkcs12.post(
            self.server.get_url("serviceregistry") + "register-system",
            json = message,
            pkcs12_filename = system.p12file,
            pkcs12_password = system.p12pass,
            verify = system.cafile,
        )

        return (res.status_code, res.json())
