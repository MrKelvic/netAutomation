
def commandConst():
    maps={
        "info":"info",
        "interfaces":"interfaces",
        "cli":"cli",
        "macTable":"macTable",
        "routeTo":"routeTo"
    }
    return maps


def configOptions(device):
    devices={
        "ios":{
            "cmd":{
                ## value=>[parseFunction,key-keyPrepend,description]
                "show interfaces":["interfaces","interface",{
                    "link_status":"state",
                    "description":"description",
                    "protocol_status":"connected"
                }],
                "show interfaces switchport":["interfaces","interface",{
                    "switchport":"isSwitchport",
                    "switchport_negotiation":"negotiation",
                    "native_vlan":"native_vlan",
                    "access_vlan":"access_vlan",
                    "voice_vlan":"voice_vlan",
                    "trunking_vlans":"trunking_vlans",
                    "mode":"mode",
                }],
                "show vlan":["interfaces","vlan_id-Vlan",{
                    "vlan_id":"id",
                    "name":"name"
                }],
                "show ip interface":["interfaces","intf",{
                    "ipaddr":"ip",
                    "mask":"mask",
                    "ip_helper":"ip_helper",
                    "inbound_acl":"inbound_acl",
                    "outgoing_acl":"outgoing_acl",
                    "vrf":"vrf",
                }],
                "show dhcp lease":["interfaces","interface",{
                    "interface":"interface"
                }],
                ## routing
                ## ospf
                "show running-config | sec router ospf":["routes","ospf",{
                    "ospf":"ospf"
                },'''
                - match: router ospf (\d+)
                  child:
                  - match: router-id (?P<routerid>.*)
                  - match: network (?P<network>.*)
                  - match: passive-interface (?P<passive>.*)
                  - match: no passive-interface (?P<noPassive>.*)
                    ''',True],
                #eigrp
                "show running-config | sec router eigrp":["routes","eigrp",{
                "eigrp":"eigrp"
                },'''
                - match: router eigrp (\d+)
                  child:
                  - match: eigrp router-id (?P<routerid>.*)
                  - match: network (?P<network>.*)
                  - match: passive-interface (?P<passive>.*)
                  - match: no passive-interface (?P<noPassive>.*)
                    ''',True],
                "show running-config | sec ip route":["routes","static",{
                "static":"static"
                },'''
                - match: ip route (?P<route>.*)
                    ''',True],
                # policies
                "show ip access-lists":["policies","acl",{
                    "acl_name":"acl_no",
                    "action":"action",
                    "protocol":"protocol",
                    "src_host":"src_host",
                    "src_any":"src_any",
                    "src_network":"src_network",
                    "src_wildcard":"src_wildcard",
                    "src_port_match":"src_port_match",
                    "src_port":"src_port",
                    "dst_host":"dst_host",
                    "dst_any":"dst_any",
                    "dst_network":"dst_network",
                    "dst_wildcard":"dst_wildcard",
                    "dst_port_match":"dst_port_match",
                    "dst_port":"dst_port",
                }],
                # "show running-config partition access-list":["policy","acl",{
                #     "acl_name":"ip",
                #     "action":"mask",
                #     "protocol":"ip_helper",
                #     "src_host":"inbound_acl",
                #     "outgoing_acl":"outgoing_acl",
                #     "vrf":"vrf",
                # }],

                # "show ip nat translations":"fnString",KEEP
                # "show port-security interface interface":"fnString",
                # "show mpls interfaces":"fnString",KEEP
                # "show ip vrf interfaces":"fnString",KEEP
                # "show ip bgp neighbors advertised-routes":"fnString",KEEP
                # "show running-config partition route-map":"fnString",KEEP
                # "show capability feature routing":"fnString",
                # "show ip bgp vpnv4 all neighbors":"fnString",
                # "show authentication sessions":"fnString",
                # "show bfd neighbors details":"fnString",KEEP
                # "show crypto session detail":"fnString",KEEP
                # "show ipv6 interface brief":"fnString",KEEP
                # "show ip eigrp neighbors":"fnString",
                # "show ip eigrp topology":"fnString",KEEP
                # "show ip source binding":"fnString",KEEP
                # "show ip bgp neighbors":"fnString",
                # "show access-session":"fnString",
                # "show ip bgp summary":"fnString",
                # "show ip prefix-list":"fnString",KEEP
                # "show ipv6 neighbors":"fnString",
                # "show isis neighbors":"fnString",
                # "show lldp neighbors":"fnString",
                # "show snmp community":"fnString",KEEP
                # "show cdp neighbors":"fnString",
                # "show controller t1":"fnString",KEEP
                # "show hosts summary":"fnString",KEEP
                # "show ip cef detail":"fnString",
                # "show spanning-tree":"fnString",KEEP
                # "show standby brief":"fnString",KEEP
                # "show object-group":"fnString",KEEP
                # "show access-list":"fnString",KEEP
                # "show isdn status":"fnString",KEEP
                # "show redundancy":"fnString",
                # "show vrrp brief":"fnString",KEEP
                # "show vtp status":"fnString",KEEP
                # "show adjacency":"fnString",
                # "show dot1x all":"fnString",KEEP
                # "show inventory":"fnString",
                # "show ip mroute":"fnString",
                # "show route-map":"fnString",KEEP
                # "show snmp user":"fnString",KEEP
                # "show ip route":"fnString",#KEEP
                # "show vrrp all":"fnString",KEEP
                # "show aliases":"fnString",
                # "show archive":"fnString",
                # "show standby":"fnString",KEEP
                # "show version":"fnString",
                # "show ip bgp":"fnString",
                # "show ip cef":"fnString",
                # "show tacacs":"fnString",KEEP
                # "show dmvpn":"fnString",KEEP
                # "show vrf":"fnString"#KEEP
            }
        },
        "nxos":{
            "cmd":[
                "show interface transceiver details",
                "show environment temperature",
                "show forwarding ipv4 route",
                "show interface description",
                "show interface transceiver",
                "show interfaces switchport",
                "show ip dhcp relay address",
                "show lldp neighbors detail",
                "show cdp neighbors detail",
                "show forwarding adjacency",
                "show ip interface vrf all",
                "show ipv6 interface brief",
                "show port-channel summary",
                "show cts interface brief",
                "show ip bgp summary vrf",
                "show ip interface brief",
                "show cts interface all",
                "show ip community-list",
                "show mac address-table",
                "show interface status",
                "show ip bgp neighbors",
                "show ip ospf database",
                "show ip ospf neighbor",
                "show interface brief",
                "show flogi database",
                "show ip bgp summary",
                "show lldp neighbors",
                "show cdp neighbors",
                "show ip arp detail",
                "show license usage",
                "show processes cpu",
                "show vrf interface",
                "show access-lists",
                "show ip adjacency",
                "show ip interface",
                "show environment",
                "show interface",
                "show inventory",
                "show route-map",
                "show hostname",
                "show hsrp all",
                "show ip route",
                "show feature",
                "show version",
                "show fex id",
                "show ip arp",
                "show ip bgp",
                "show module",
                "show clock",
                "show vlan",
                "show fex",
                "show vdc",
                "show vpc",
                "show vrf"
            ]
        }
    }
    return devices[device]["cmd"]

    

if __name__ == '__main__':
    print("MAIN FN in engine.py file")