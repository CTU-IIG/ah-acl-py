#!/usr/bin/env python3
# connectorabc.py
"""Abstract class for Connectors.
"""

from typing import Dict, Tuple

from aclpy.server import ArrowheadServer
from aclpy.system import ArrowheadSystem


class ConnectorABC(object):

    def __init__(self, server: ArrowheadServer):
        super(ConnectorABC, self).__init__()

        self.server = server


    def orchestrate(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[int, str]:
        raise NotImplementedError
