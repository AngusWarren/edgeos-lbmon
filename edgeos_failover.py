
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

OID_BASE = '.1.3.6.1.4.1.56751.1.1'
OIDS = [
    '0', # load balance group name
    '1', # interface name
    '2', # state
]

def discovery_edgeos_failover(section):
    groups = set([x[0] for x in section])
    for group in groups:
        yield Service(item=group)

def check_edgeos_failover(item, section):
    interfaces = [ x for x in section if x[0] == item ]
    summary = []
    overall_state = State.OK
    for interface in interfaces:
        summary.append(f"{interface[1]}={interface[2]}")
        if interface[2] != "OK":
            overall_state = State.WARN
    yield Result(state=overall_state, summary=" ".join(summary))

register.snmp_section(
    name = "edgeos_failover",
    detect = all_of(
        startswith(".1.3.6.1.2.1.1.1.0", "EdgeOS"), # first check sysDescr
        equals(OID_BASE, "Watchdog Status"),  # fetch vendor specific OID
    ),
    fetch = SNMPTree(base=OID_BASE, oids=OIDS)
)

register.check_plugin(
    name = 'edgeos_failover',
    service_name = 'Failover %s',
    discovery_function = discovery_edgeos_failover,
    check_function = check_edgeos_failover,
)
