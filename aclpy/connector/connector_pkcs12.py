#!/usr/bin/env python3
# connector_pkcs12.py
"""Connector / interface to Arrowhead Core using .p12 certificates.
"""
import requests_pkcs12

from typing import Dict, Tuple

from aclpy.connector.connectorabc import ConnectorABC
from aclpy.server import ArrowheadServer
from aclpy.system import ArrowheadSystem


class ArrowheadConnector(ConnectorABC):

    def orchestrate(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[int, str]:
        res = requests_pkcs12.post(
            self.server.get_url("orchestrator") + "orchestration",
            json = message,
            pkcs12_filename = system.p12file,
            pkcs12_password = system.p12pass,
            verify = system.cafile,
        )

        return (res.status_code, res.text)
