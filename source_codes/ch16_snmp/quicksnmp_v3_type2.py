from pysnmp import hlapi
from pysnmp.hlapi import UsmUserData

def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]

def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types

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

usm_user_data = hlapi.UsmUserData(
    'SNMPUser1',
    authKey='AUTHPass1',
    privKey='PRIVPass1',
    authProtocol=hlapi.usmHMACSHAAuthProtocol,
    privProtocol=hlapi.usmAesCfb128Protocol
)

print(get('192.168.127.3', ['1.3.6.1.2.1.1.5.0'], usm_user_data))
print(get('192.168.127.3', ['1.3.6.1.2.1.2.2.1.7.4'], usm_user_data))
