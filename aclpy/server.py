#!/usr/bin/env python3
# server.py
"""Arrowhead server configuration for the library.
"""

class ArrowheadServer(object):

    def __init__(self, **kwargs):
        super(ArrowheadServer, self).__init__()

        # Core IP
        self.address = kwargs.get("address", "127.0.0.1")

        self.orchestrator = {
            "port": kwargs.get("orchestrator_port", 8441),
            "endpoint": "orchestrator",
        }
        self.serviceregistry = {
            "port": kwargs.get("serviceregistry_port", 8443),
            "endpoint": "serviceregistry",
        }
        self.authorization = {
            "port": kwargs.get("authorization_port", 8445),
            "endpoint": "authorization",
        }


    def get_url(self, core_service):
        if hasattr(self, core_service):
            service = getattr(self, core_service)
            return "https://" + self.address + ":" + str(service.get("port")) + "/" + service.get("endpoint") + "/"
        else:
            raise ValueError("Undefined core service '%s'." % core_service)
