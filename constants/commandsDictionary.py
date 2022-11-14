
def controlPlane():
    return {
        # if type LIST [command,[key1,key2]]
        # ROUTES
        "eigrp":{
            'ios':{
                "asn":'router eigrp {}',
                "network":'network {}'
            }
        },
        "ospf":{
            "ios":{
                "pid":'router ospf {}',
                "network":['network ',['network','wildcard']]
            }
        },
        "static":{
            "ios":{
                "network":['ip route ',['network','mask','next_hop','AD']] #[Write "AD" ?,'AD']
            }
        }
    }


def dataPlane():
    return {
        # if type LIST [command,[key1,key2]]
        # INTERFACES
        "routed":{
            'ios':'switchport'
        },
        "mode":{
            'ios':'switchport mode {}'
        },
        "nativeVlan":{
            'ios':'switchport trunk native vlan {}'
        },
        # "outgoing_acl":{},
        # "inbound_acl":{},
        "allowedVlans":{
            'ios':'switchport trunk allowed vlan {}'
        },
        "voice":{
            'ios':'switchport voice vlan {}'
        },
        "data":{
            'ios':'switchport access vlan {}'
        },
        "ip":{
            'ios':['ip address {}',['ip','mask']]#' {}'
        },
        "ip_helper":{
            'ios':'ip helper-address {}'
        },
        "description":{
            'ios':'description {}'
        },
        "state":{
            'ios':'shutdown'
        },
    }

def references(source):
    if source == "interfaces":
        return dataPlane()
    elif source == "routes":
        return controlPlane()


if __name__ == '__main__':
    # print("MAIN FN in engine.py file")
    refs=references('interfaces') or {}
    # print(refs)
    for ref in refs:
        print(str(refs[ref]['ios']).format("YAAAYY!!"))