#!/usr/bin/env python3
# messages.py
"""Definition of various Arrowhead-related messages.
"""

from typing import Dict, List

from aclpy.interface import ArrowheadInterface
from aclpy.system import ArrowheadSystem
from aclpy.service import ArrowheadService


def build_register_service(*,
        interfaces: List[ArrowheadInterface],
        system: ArrowheadSystem,
        service: ArrowheadService,
    ) -> Dict[str, any]:
    """Build a message for registering a service.

    Arguments:
    interface (List[ArrowheadInterface]) -- list of the interfaces used for the communication
    system (ArrowheadSystem) -- system for attaching the service
    service (ArrowheadService) -- service to be registered

    Returns:
    message (Dict[str, any])
    """
    return {
        # *Which interface do we use?
        # The convention (name pattern is) PROTOCOL-SECURE/INSECURE-DATA_FORMAT
        # I assume that SECURE = encrypted by the TOKEN/CERTIFICATE
        "interfaces": [
            interface.name for interface in interfaces
        ],

        # *Who are we?
        # Here we introduce the system providing the service.
        # 'systemName' should be same as the name in the certificate.
        #   - Otherwise, we get an SSL error.
        # 'authenticationInfo' is required with 'CERTIFICATE' and 'TOKEN'
        #   - For 'CERTIFICATE' I put there public key (so it should be asymmetric encryption).
        # 'address' is an IP address / name? of the server
        # 'port' is port used for the communication
        "providerSystem": {
            "systemName": system.name,
            "authenticationInfo": system.pubkey,
            "address": system.address,
            "port": system.port,
        },

        # *Which service we provide?
        "serviceDefinition": service.name,

        # Security info (probably just showing what can be used for authorization?)
        #  - Default is 'NOT_SECURE', other options are: 'CERTIFICATE' and 'TOKEN'
        "secure": "CERTIFICATE",

        # Version of the service
        "version": service.version,

        ## Other parts we do not use (even though some of them are mandatory*):

        # *URI of the service
        # "serviceUri": "string",

        # Service is available until this UTC timestamp
        # "endOfValidity": "string",

        # Various optional metadata
        # "metadata": {
        #     "additionalProperty1": "string",
        # },
    }


def build_unregister_service(*,
        system: ArrowheadSystem,
        service: ArrowheadService,
    ) -> Dict[str, any]:
    """Build a message for unregistering a service.

    Arguments:
    system (ArrowheadSystem) -- system with the service
    service (ArrowheadService) -- service to be unregistered

    Returns:
    message (Dict[str, any])
    """
    return {
        # *Who are we and what we want to unregister?
        #  - We are allowed to unregister only our services.
        # 'address': IP address of the provider
        # 'port': port of the provider
        # 'system_name': name of the provider
        "address": system.address,
        "port": system.port,
        "system_name": system.name,

        # *'service_definition': service to be removed
        "service_definition": service.name,
    }


def build_register_system(*,
        system: ArrowheadSystem,
    ) -> Dict[str, any]:
    """Build a message for registering a system to Arrowhead Core.

    Arguments:
    system (ArrowheadSystem) -- system to be registered

    Returns:
    message (Dict[str, any])
    """
    return {
        # *Who are we?
        # 'systemName': name of the client
        # 'authenticationInfo' is required with 'CERTIFICATE' and 'TOKEN'
        #   - For 'CERTIFICATE' I put there public key (so it should be asymmetric encryption).
        # 'address': IP address of the client
        # 'port': port is not used for client, so can be zero (we are consuming)
        "systemName": system.name,
        "authenticationInfo": system.pubkey,
        "address": system.address,
        "port": system.port,
    }


def build_orchestration_request(*,
        interfaces: List[ArrowheadInterface],
        system: ArrowheadSystem,
        service: ArrowheadService,
    ) -> Dict[str, any]:
    """Build a message for locating providers via orchestration.

    Arguments:
    interface (List[ArrowheadInterface]) -- list of the interfaces requested for the communication
    system (ArrowheadSystem) -- system requesting the orchestration
    service (ArrowheadService) -- service to be located

    Returns:
    message (Dict[str, any])
    """
    return {
        # *Who are we?
        # Here we introduce the system asking the service.
        # 'systemName' should be same as the name in the certificate.
        #   - Otherwise, we get an SSL error.
        # 'authenticationInfo' is required with 'CERTIFICATE' and 'TOKEN'
        #   - For 'CERTIFICATE' I put there public key (so it should be asymmetric encryption).
        # 'address' is an IP address / name? of the system
        # 'port' is port used for the communication
        "requesterSystem": {
            "systemName": system.name,
            "authenticationInfo": system.pubkey,
            "address": system.address,
            "port": system.port, # I assume that 0 means that we are not listening
        },

        # Dynamic Orchestration
        #  - By passing this value we say that we want to find the counterpart dynamically,
        #  skipping any pre-set configuration in the Orchestrator.
        "orchestrationFlags": {
            "overrideStore": "true"
        },

        # Which service do we want?
        # Since the dynamic orchestration is enabled, this is mandatory*.
        "requestedService": {
            # Which interface we want to use?
            #  - This is optional.
            # In here, you can use 'interfaceRequirement' (string). But it is not supported by Orchestrator (anymore?).
            "interfaceRequirements": [
                interface.name for interface in interfaces
            ],

            # *What is the name of the service?
            "serviceDefinitionRequirement": service.name,
        }
    }
