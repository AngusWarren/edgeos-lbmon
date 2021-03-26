
#from cmk.base.plugins.agent_based.agent_based_api.v1 import (
from .agent_based_api.v1 import (
    register,
    Result,
    Service,
    State,
    SNMPTree,
    OIDEnd,
    all_of,
    equals,
    startswith,
)

register.snmp_section(
    name = "edgeos_failover",
    detect = all_of(
        startswith(".1.3.6.1.2.1.1.1.0", "EdgeOS"),           # first check sysDescr
        equals(".1.3.6.1.4.1.56751.1.1", "Watchdog Status"),  # fetch vendor specific OID
    ),
    fetch = SNMPTree(base = '.1.3.6.1.4.1.56751.1',
            	     oids=[OIDEnd(),"1"])
            	     #oids=['1','2'])
)

def process_oids(section):
    lookup = dict((k,v) for k,v in section)
    groups = dict()
    for element in section:
        parts = element[0].split('.')
        if len(parts) == 3:
            group_name = lookup.get(parts[0])
            interface_name = lookup.get('.'.join(parts[0:2]))
            status = element[1]
            #print(f"{group_name}:{interface_name}:{status}")
            if group_name not in groups:
                groups[group_name] = dict()
            if interface_name not in groups[group_name]:
                groups[group_name][interface_name] = status
    return groups

def discovery_edgeos_failover(section):
    groups = process_oids(section)
    for group in groups.keys():
        yield Service(item=group)

def check_edgeos_failover(item, section):
    groups = process_oids(section)
    group = groups[item]
    
    overall_state = State.OK
    for state in group.values():
        if state != "OK":
            overall_state = State.WARN

    pairs = []
    for interface,status in group.items():
        pairs.append(f"{interface}={status}")
    yield Result(state=overall_state, summary=" ".join(pairs))

register.check_plugin(
    name = 'edgeos_failover',
    service_name = 'Failover %s',
    discovery_function = discovery_edgeos_failover,
    check_function = check_edgeos_failover,
)
