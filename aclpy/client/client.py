#!/usr/bin/env python3
# client.py
"""Arrowhead Client class.
"""

import json

from aclpy.connector.connectorabc import ConnectorABC
from aclpy.messages import *
from aclpy.service import ArrowheadService
from aclpy.system import ArrowheadSystem


class ArrowheadClient(ArrowheadSystem):

    def __init__(self, name: str, address: str, port: int, pubkey: str, connector: ConnectorABC):
        super(ArrowheadClient, self).__init__(name, address, port, pubkey)

        self.connector = connector


    def register_service(self, service: ArrowheadService) -> bool:
        msg = build_register_service("HTTP-INSECURE-JSON", self, service)

        success, status_code, payload = self.connector.register_service(self, msg)

        return success


    def unregister_service(self, service: ArrowheadService) -> bool:
        msg = build_unregister_service(self, service)

        success, status_code, payload = self.connector.unregister_service(self, msg)

        return success


    def register_system(self) -> bool:
        msg = build_register_system(self)

        success, status_code, payload = self.connector.register_system(self, msg)

        return success


    def orchestrate(self, service: ArrowheadService) -> ArrowheadSystem:
        msg = build_orchestration_request("HTTP-INSECURE-JSON", self, service)

        success, status_code, payload = self.connector.orchestrate(self, msg)

        if not success:
            return None
        else:
            system = payload.get("response")[0].get("provider")
            return ArrowheadSystem(
                address = system.get("address"),
                port = system.get("port"),
                name = system.get("name"),
                pubkey = system.get("authenticationInfo"),
            )
