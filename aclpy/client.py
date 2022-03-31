#!/usr/bin/env python3
# client.py
"""Arrowhead Client class.
"""

from aclpy.service import ArrowheadService
from aclpy.system import ArrowheadSystem


class ArrowheadClient(ArrowheadSystem):

    def __init__(self, name: str, address: str, port: int, p12file: str, p12pass: str, pubfile: str, cafile: str):
        # Read pubkey first
        with open(pubfile, "r") as f:
            pubkey = f.read()

        super(ArrowheadClient, self).__init__(name, address, port, "".join(pubkey.split("\n")[1:-2]))

        self.p12file = p12file
        self.p12pass = p12pass
        self.pubfile = pubfile
        self.cafile = cafile


    def register_service(self, service: ArrowheadService) -> bool:
        pass


    def unregister_service(self, service: ArrowheadService) -> bool:
        pass


    def register_system(self) -> bool:
        pass
