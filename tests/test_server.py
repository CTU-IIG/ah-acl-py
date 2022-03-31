#!/usr/bin/env python3
# test_server.py
"""Test Arrowhead Server.
"""

import unittest

from aclpy.server import ArrowheadServer



class TestServer(unittest.TestCase):

    def test_server(self):
        server = ArrowheadServer()

        server.get_url("orchestrator")


if __name__ == "__main__":
    unittest.main()
