#!/usr/bin/env python3
# client_pkcs12.py
"""Arrowhead Client class using .p12 certificates.
"""

from typing import List

from aclpy.client.client import ArrowheadClient as ArrowheadClientBase
from aclpy.connector.connector_pkcs12 import ArrowheadConnector
from aclpy.interface import ArrowheadInterface
from aclpy.server import ArrowheadServer


class ArrowheadClient(ArrowheadClientBase):
    """ArrowheadClient class for utilizing pkcs12 to communicate with Arrowhead Core.

    Additional attributes:
    p12file (str) -- path to the .p12 certificate
    p12pass (str) -- password to the .p12 certificate
    pubkey (str) -- public key, mutually exclusive with 'pubfile'
    pubfile (str) -- path to the public key .pub, mutually exclusive with 'pubkey'
    cafile (str) -- path to the certificate authority file .ca
    server (ArrowheadServer) -- configuration of the Arrowhead Core server
    interfaces (List[ArrowheadInterfaces]) -- list of available interfaces, [] by default

    Note: When pub* are not given, the public key is obtained from p12 file.
    """

    def __init__(self, *,
            name: str,
            address: str,
            port: int,
            p12file: str,
            p12pass: str,
            pubkey: str = None,
            pubfile: str = None,
            cafile: str,
            server: ArrowheadServer,
            interfaces: List[ArrowheadInterface] = [],
    ):
        """Initialize ArrowheadClient class."""
        if pubkey is not None and pubfile is not None:
            raise ValueError("Conflict betwen pubkey and pubfile. Provide only one of them.")

        if pubfile is not None:
            # Read pubkey first
            with open(pubfile, "r") as f:
                pubkey = f.read()

        if pubkey is None:
            from OpenSSL import crypto

            pubkey = crypto.dump_publickey(
                crypto.FILETYPE_PEM,
                crypto.load_pkcs12(
                    open(p12file, "rb").read(),
                    p12pass
                ).get_certificate().get_pubkey()
            )


        self.connector = ArrowheadConnector(server)

        super(ArrowheadClient, self).__init__(name, address, port, str(pubkey).replace("\n", ""), self.connector)

        self.p12file = p12file
        self.p12pass = p12pass
        self.pubfile = pubfile
        self.cafile = cafile

        for interface in interfaces:
            self.interfaces.append(interface)
