# Arrowhead Client Library for Python
_Very lightweight version for quick projects._

Based on [ah-echo-py](https://github.com/jara001/ah-echo-py).

- [Requirements](#requirements)
- [Getting started](#getting-started)
- [Implemented features](#implemented-features)
- [Usage](#usage)
  - [Arrowhead Server](#arrowheadserver)
  - [Arrowhead Service](#arrowheadservice)
  - [Arrowhead Client](#arrowheadclient)
- [Example](#example)


## Requirements

- `Python 3`
- `requests_pkcs12`


## Getting started

Download the package and install it using:
```sh
python3 -m pip install aclpy-*.whl
```

Or if you have [wagon](https://github.com/cloudify-cosmo/wagon) you can install it along with the dependencies using:
```sh
wagon install aclpy-*.wgn
```


## Implemented features

- [ ] ArrowheadConnector + ArrowheadClient
  - [ ] Features
    - [X] Register a service
    - [X] Unregister a service
    - [X] Register a system
    - [X] Orchestrate
  - [ ] Methods
    - [X] PKCS#12
- [ ] ArrowheadServer
  - [X] Set IP address
  - [ ] Core Systems features
    - [X] Change port
    - [ ] Change endpoint
    - [X] Set URL
  - [ ] Core Systems
    - [X] Orchestrator
    - [X] ServiceRegistry
    - [X] Authorization
- [ ] ArrowheadService
  - [X] Name
  - [X] Version
  - [ ] Interface
  - [ ] Security
  - [ ] URI
  - [ ] End of Validity
  - [ ] Metadata
- [ ] ArrowheadSystem
  - [X] Name
  - [X] Address
  - [X] Port
  - [ ] AuthenticationInfo
    - [X] Public key
    - [ ] Token


## Usage

### ArrowheadServer

```python
from aclpy.server import ArrowheadServer

server = ArrowheadServer()
```


### ArrowheadService

```python
from aclpy.service import ArrowheadService

service = ArrowheadService(
    name = "NAME_OF_THE_SERVICE",
)
```


### ArrowheadClient
_PKCS#12 version_

```python
from aclpy.client.client_pkcs12 import ArrowheadClient

client = ArrowheadClient(
    name = "NAME_OF_THE_CLIENT",
    address = "IP_ADDRESS_OF_THE_CLIENT",
    port = PORT_OF_THE_CLIENT,
    pubfile = "PATH_TO_THE_PUB_FILE",
    p12file = "PATH_TO_THE_P12_FILE",
    p12pass = "PASSWORD_TO_P12_FILE",
    cafile = "PATH_TO_THE_CA_FILE",
    server = server,
)

# Register a service
success = client.register_service(service)

# Unregister a service
success = client.unregister_service(service)

# Register the system
success = client.register_system()

# Run the orchestration for service
success, providers = client.orchestrate(service)
```


## Example

```python
# Server configuration
from aclpy.server import ArrowheadServer

# Client / system configuration
from aclpy.client.client_pkcs12 import ArrowheadClient

# Service configuration
from aclpy.service import ArrowheadService


# Define the components
server = ArrowheadServer(
    #address = "127.0.0.1",     # Localhost is default
)

client = ArrowheadClient(
    name = "echoclient",
    address = "127.0.0.1",
    port = 0,                   # As we are only listening
    pubfile = "echoclient.pub", # Path to the public key
    p12file = "echoclient.p12", # Path to the private key
    p12pass = "1111111",        # Password
    cafile = "sysop.ca",        # Path to .ca file
    server = server,
)

service = ArrowheadService(
    name = "echo",
)


# Look for the echo server
success, providers = client.orchestrate(service)

print ("Orchestration was %s." % ("SUCCESSFUL" if success else "NOT SUCCESSFUL"))
print ("Found %d providers." % len(providers))

if len(providers) > 0:
    for _i, provider in enumerate(providers):
        print ("%d: %s:%d" % (_i, provider.address, provider.port))
```
