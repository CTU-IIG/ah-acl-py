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


    def orchestrate(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[bool, int, Dict[str, any]]:
        status_code, payload = self._orchestrate(system, message)

        if status_code >= 400:
            print ("Client is not authorized for communication with the Orchestrator.", file=sys.stderr)

            return False, status_code, payload

        # List providers
        print ("Found %d service providers." % len(payload["response"]))

        for _i, provider in enumerate(payload["response"]):
            print ("%d: %s:%d" % (
                _i + 1,
                provider["provider"]["address"],
                provider["provider"]["port"])
            )

        return True, status_code, payload


    def register_service(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[bool, int, Dict[str, any]]:
        status_code, payload = self._register_service(system, message)

        if status_code >= 400:
            print ("Client is not authorized for communication with the Service Registry.", file=sys.stderr)

            return False, status_code, payload

        print ("Service registered with id %d using interface ID: %d. System ID: %d." % (
            payload["serviceDefinition"]["id"],
            payload["interfaces"][0]["id"],
            payload["provider"]["id"])
        )

        return True, status_code, payload


    def unregister_service(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[bool, int, Dict[str, any]]:
        status_code, payload = self._unregister_service(system, message)

        if status_code >= 400:
            print ("Client is not authorized for communication with the Service Registry.", file=sys.stderr)

            return False, status_code, payload

        return True, status_code, payload


    def register_system(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[bool, int, Dict[str, any]]:
        status_code, payload = self._register_system(system, message)

        if status_code >= 400:
            print ("Unable to create the system.", file=sys.stderr)

            return False, status_code, payload

        print ("System registered with ID: %d." % text)

        return True, status_code, payload


    ## Implemented by the subclass
    def _orchestrate(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        raise NotImplementedError


    def _register_service(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        raise NotImplementedError


    def _unregister_service(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        raise NotImplementedError


    def _register_system(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        raise NotImplementedError
