#!/usr/bin/env python3
# client_pkcs12.py
"""Arrowhead Client class using .p12 certificates.
"""

import json

from aclpy.connector.connector_pkcs12 import ArrowheadConnector
from aclpy.messages import *
from aclpy.server import ArrowheadServer
from aclpy.service import ArrowheadService
from aclpy.system import ArrowheadSystem
from aclpy.client.client import ArrowheadClient as ArrowheadClientBase


class ArrowheadClient(ArrowheadClientBase):

    def __init__(self, name: str, address: str, port: int, p12file: str, p12pass: str, pubfile: str, cafile: str, server: ArrowheadServer):
        # Read pubkey first
        with open(pubfile, "r") as f:
            pubkey = f.read()

        self.connector = ArrowheadConnector(server)

        super(ArrowheadClient, self).__init__(name, address, port, "".join(pubkey.split("\n")[1:-2]), self.connector)

        self.p12file = p12file
        self.p12pass = p12pass
        self.pubfile = pubfile
        self.cafile = cafile
