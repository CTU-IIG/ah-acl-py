#!/usr/bin/env python3
# system.py
"""System class for Arrowhead.
"""

class ArrowheadSystem(object):

    __slots__ = ["name", "address", "port", "pubkey"]

    def __init__(self, name: str, address: str, port: int, pubkey: str = ""):
        super(ArrowheadSystem, self).__init__()

        self.name = name
        self.address = address
        self.port = port
        self.pubkey = pubkey
