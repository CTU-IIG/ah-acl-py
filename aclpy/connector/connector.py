#!/usr/bin/env python3
# connector.py
"""Connector class for handling requests to Arrowhead Core.
"""

import sys

from typing import Dict, Tuple

from aclpy.server import ArrowheadServer
from aclpy.system import ArrowheadSystem


class Error:
    """Error class for storing information about error received from Arrowhead Core.

    Attributes:
    error_code (int) -- HTTP error code
    exception_type (str) -- type of the exception raised from the Core
    error_message (str) -- description of the error
    """
    __slots__ = ["error_code", "exception_type", "error_message"]


    def __init__(self, **kwargs):
        """Initialize Error class."""
        self.error_code = kwargs.get("errorCode")
        self.exception_type = kwargs.get("exceptionType")
        self.error_message = kwargs.get("errorMessage")


    def report_error(self):
        """Report this error."""
        report_error(self.error_code, self.system_name, self.operation)


    def __str__(self):
        """Format the error as string.

        Returns:
        str -- error as a string
        """
        return "Error code: %d\nException: %s\nMessage: %s" % (
            self.error_code,
            self.exception_type,
            self.error_message
        )


def report_error(self, status_code: int, system_name: str, operation: str):
    """Report an error from responses.

    Arguments:
    status_code (int) -- HTTP code from the response
    system_name (str) -- name of the core system
    operation (str) -- short description of the operation done
    """
    if status_code == 400:
        print ("Unable to %s." % operation, file=sys.stderr)

    elif status_code == 401:
        print ("Client is not authorized for communication with the %s." % system_name, file=sys.stderr)

    elif status_code == 500:
        print ("Core service %s is not available." % system_name, file=sys.stderr)

    else:
        print ("Unknown error with code %d when trying to %s with the %s." % (status_code, system_name, operation), file=sys.stderr)


class ArrowheadConnector(object):
    """ArrowheadConnector class for handing requests to the Arrowhead Core.

    Attributes:
    server (ArrowheadServer) -- configuration of the Arrowhead Core server
    last_error (Error) -- last received error
    """

    def __init__(self, server: ArrowheadServer):
        """Initialize ArrowheadConnector class."""
        super(ArrowheadConnector, self).__init__()

        self.server = server
        self.last_error = None


    def orchestrate(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[bool, int, Dict[str, any]]:
        """Request available providers from the Orchestrator.

        Arguments:
        system (ArrowheadSystem) -- system requesting the orchestration
        message (Dict[str, any]) -- message to be sent to the Orchestrator

        Returns:
        success (bool) -- True when orchestration is successful
        status_code (int) -- HTTP code from the response
        response (Dict[str, any]) -- message received from the Orchestrator

        Note: 'message' is created by 'aclpy.messages.build_orchestration_request'.
        """
        status_code, payload = self._orchestrate(system, message)

        success = status_code < 300

        if not success:
            self.last_error = Error(**payload)
            self.last_error.report_error(status_code, "Orchestrator", "orchestrate")

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
        """Register a service for 'system' to the Service Registry.

        Arguments:
        system (ArrowheadSystem) -- system for service registration
        message (Dict[str, any]) -- message to be sent to the Service Registry

        Returns:
        success (bool) -- True when registration is successful
        status_code (int) -- HTTP code from the response
        response (Dict[str, any]) -- message received from the Service Registry

        Note: 'message' is created by 'aclpy.messages.build_register_service'.
        """
        status_code, payload = self._register_service(system, message)

        success = status_code < 300

        if not success:
            self.last_error = Error(**payload)
            self.last_error.report_error(status_code, "Service Registry", "register service")

            return False, status_code, payload

        print ("Service registered.\nInterface ID: %d\nProvider ID: %d\nService ID: %d" % (
            payload["interfaces"][0]["id"],
            payload["provider"]["id"],
            payload["serviceDefinition"]["id"],
        ))

        return True, status_code, payload


    def unregister_service(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[bool, int, Dict[str, any]]:
        """Unregister a service for 'system' to the Service Registry.

        Arguments:
        system (ArrowheadSystem) -- system for service unregistration
        message (Dict[str, any]) -- message to be sent to the Service Registry

        Returns:
        success (bool) -- True when unregistration is successful
        status_code (int) -- HTTP code from the response
        response (Dict[str, any]) -- message received from the Service Registry

        Note: 'message' is created by 'aclpy.messages.build_unregister_service'.
        """
        status_code, payload = self._unregister_service(system, message)

        success = status_code < 300

        if not success:
            self.last_error = Error(**payload)
            self.last_error.report_error(status_code, "Service Registry", "unregister service")

            return False, status_code, payload

        return True, status_code, payload


    def register_system(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[bool, int, Dict[str, any]]:
        """Register a 'system' to Arrowhead Core via Service Registry.

        Arguments:
        system (ArrowheadSystem) -- system for registration
        message (Dict[str, any]) -- message to be sent to the Service Registry

        Returns:
        success (bool) -- True when registration is successful
        status_code (int) -- HTTP code from the response
        response (Dict[str, any]) -- message received from the Service Registry

        Note: 'message' is created by 'aclpy.messages.build_register_system'.
        """
        status_code, payload = self._register_system(system, message)

        success = status_code < 300

        if not success:
            self.last_error = Error(**payload)
            self.last_error.report_error(status_code, "Service Registry", "register system")

            return False, status_code, payload

        print ("System registered with ID: %d." % payload["id"])

        return True, status_code, payload


    ## Implemented by the subclass
    def _orchestrate(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        """Request available providers from the Orchestrator. (Implemented by the derived class.)

        Arguments:
        system (ArrowheadSystem) -- system requesting the orchestration
        message (Dict[str, any]) -- message to be sent to the Orchestrator

        Returns:
        status_code (int) -- HTTP code from the response
        response (Dict[str, any]) -- message received from the Orchestrator

        Note: 'message' is created by 'aclpy.messages.build_orchestration_request'.
        """
        raise NotImplementedError


    def _register_service(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        """Register a service for 'system' to the Service Registry. (Implemented by the derived class.)

        Arguments:
        system (ArrowheadSystem) -- system for service registration
        message (Dict[str, any]) -- message to be sent to the Service Registry

        Returns:
        status_code (int) -- HTTP code from the response
        response (Dict[str, any]) -- message received from the Service Registry

        Note: 'message' is created by 'aclpy.messages.build_register_service'.
        """
        raise NotImplementedError


    def _unregister_service(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        """Unregister a service for 'system' to the Service Registry. (Implemented by the derived class.)

        Arguments:
        system (ArrowheadSystem) -- system for service unregistration
        message (Dict[str, any]) -- message to be sent to the Service Registry

        Returns:
        status_code (int) -- HTTP code from the response
        response (Dict[str, any]) -- message received from the Service Registry

        Note: 'message' is created by 'aclpy.messages.build_unregister_service'.
        """
        raise NotImplementedError


    def _register_system(self, system: ArrowheadSystem, message: Dict[str, any]) -> Tuple[int, Dict[str, any]]:
        """Register a 'system' to Arrowhead Core via Service Registry. (Implemented by the derived class.)

        Arguments:
        system (ArrowheadSystem) -- system for registration
        message (Dict[str, any]) -- message to be sent to the Service Registry

        Returns:
        status_code (int) -- HTTP code from the response
        response (Dict[str, any]) -- message received from the Service Registry

        Note: 'message' is created by 'aclpy.messages.build_register_system'.
        """
        raise NotImplementedError
