# This code utilizes the High-Level API module included in the pysnmp library.
from pysnmp import hlapi

"""
The first function, `get()`, defines prerequisite information to initiate and make device information requests. Typically, you need to provide the target IP (or DNS name), Object ID (OID), Credentials, SNMP port number (161), EngineID, or SNMP context. This script forms a handler, enabling the server to communicate with the agent to retrieve information about itself.
"""

def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]

# The second function, `construct_object_types`, needs a single argument `list_of_oids`. A blank list is used to collect and return object types information.

def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types

# The third function, `fetch`, requires two arguments and uses the result list to handle any errors in the script.

def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result

# The fourth function, `cast()`, uses the information received from PySNMP to pass the values, changing the value into int, float, or string type.

def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value

# This code is written for SNMPv2c and uses a community string named 'ICTSHORE'.
hlapi.CommunityData('ICTSHORE')

# If SNMPv3 is used, a user ID and two authentication keys should be used. The script uses this information to communicate with the desired SNMP Agent to get device information.

hlapi.UsmUserData('testuser', authKey='authenticationkey', privKey='encryptionkey',
authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol)

# Specifies the specific OID to obtain specified information from the SNMP Agent. '1.3.6.1.2.1.1.5.0' denotes the dot IOD for a hostname.
print(get('192.168.47.10', ['1.3.6.1.2.1.1.5.0'], hlapi.CommunityData('ICTSHORE')))
