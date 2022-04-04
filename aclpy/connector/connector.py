#!/usr/bin/env python3
# connector.py
"""Abstract class for Connectors.
"""

import sys

from typing import Dict, Tuple

from aclpy.server import ArrowheadServer
from aclpy.system import ArrowheadSystem


def report_error(status_code: int, system_name: str, operation: str):
    if status_code == 400:
        print ("Unable to %s." % operation, file=sys.stderr)

    elif status_code == 401:
        print ("Client is not authorized for communication with the %s." % system_name, file=sys.stderr)

    elif status_code == 500:
        print ("Core service %s is not available." % system_name, file=sys.stderr)

    else:
        print ("Unknown error with code %d when trying to %s with the %s." % (status_code, system_name, operation), file=sys.stderr)


class ArrowheadConnector(object):

    def __init__(self, server: ArrowheadServer):
        super(ArrowheadConnector, self).__init__()

        self.server = server


    def orchestrate(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[bool, int, Dict[str, any]]:
        status_code, payload = self._orchestrate(system, message)

        success = status_code < 300

        if not success:
            report_error(status_code, "Orchestrator", "orchestrate")

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

        success = status_code < 300

        if not success:
            report_error(status_code, "Service Registry", "register service")

            return False, status_code, payload

        print ("Service registered.\nInterface ID: %d\nProvider ID: %d\nService ID: %d" % (
            payload["interfaces"][0]["id"],
            payload["provider"]["id"],
            payload["serviceDefinition"]["id"],
        ))

        return True, status_code, payload


    def unregister_service(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[bool, int, Dict[str, any]]:
        status_code, payload = self._unregister_service(system, message)

        success = status_code < 300

        if not success:
            report_error(status_code, "Service Registry", "unregister service")

            return False, status_code, payload

        return True, status_code, payload


    def register_system(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[bool, int, Dict[str, any]]:
        status_code, payload = self._register_system(system, message)

        success = status_code < 300

        if not success:
            report_error(status_code, "Service Registry", "register system")

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
