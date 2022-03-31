#!/usr/bin/env python3
# service.py
"""Service class for Arrowhead.
"""

class ArrowheadService(object):

    __slots__ = ["name", "version"]

    def __init__(self, name: str, version: int = 1):
        super(ArrowheadService, self).__init__()

        self.name = name
        self.version = version
