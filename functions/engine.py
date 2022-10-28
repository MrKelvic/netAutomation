#!/home/kels/Documents/projects/netAutomation/autoMate/test_napalm/bin/python3
import napalm
from ntc_templates.parse import parse_output
import functions.filter as filter
# import filter #test
from tabulate import tabulate
from yaspin import yaspin
spiner=yaspin(color="green")


TEMPLATEDICTIONARY={
    "ios": "cisco_ios",
    "nxos": "cisco_nxos",
    "nxos_ssh": "cisco_nxos",
    "iosxr": "cisco_iosxr",
    "eos": "arista_eos",
    "junos": "juniper_junos",
}


def engineFnMap(key):
    maps={
        "isAlive":isAlive,
        "info":info,
        "interfaces":interfaces,
        "macTable":macTable,
        "getVlans":getVlans,
        "ping":ping,
        "traceroute":traceroute,
        "findRouteTo":findRouteTo,
        "getConfig":getConfig,
        "cli":cli,
    }
    if key in maps:
        return maps[key]
    else:
        return maps["info"]

def index(action):
    """ expects {"engineFn":String,params:None,"nodes":napalmDeviceInstances(variable)} """
    proccessedRequest=[]
    for node in action["nodes"]:
        #node=> {"napalmInstance":nodeNapalmInstance,"node":node}
        print('\n')
        # print(node['node'])
        spiner.text=("#"*3)+node['node']["hostname"]+" "+node['node']["IP"]["ip"]+("#"*3)
        spiner.start()
        try:
            node=engineFnMap(action["engineFn"])(node,action["params"])
            proccessedRequest.append(node)
            print("#"*3,node.node["hostname"],node.node["IP"]["ip"],"#"*3," -done ")
        except Exception as e:
            print(str(e))
        spiner.stop()
        # if node.filtered:
        #     print(node.filtered)
        # print(tabulate(node.cli))
        # print(node.output)
    # return []
    return proccessedRequest

class isAlive:
    def __init__(self, node,params=None):
        self.device=node["napalmInstance"]
        self.node=node["node"]
        self.device.open()
        self.isAlive=self.device.is_alive()
        self.device.close()
    def getOutput(self):
        self.node["isAlive"]=self.isAlive["is_alive"]
        return self.node

class info:
    def __init__(self, node,params=None):
        self.device=node["napalmInstance"]
        self.node=node["node"]
        self.device.open()
        self.output = self.device.get_facts()
        temp=filter.filtersFnMap("info")(self.output)
        self.device.close()
        self.cli=temp[0]
        self.web=temp[1]
    def getOutput(self):
        return self.output

class interfaces:
    def __init__(self, node,params=None):
        self.device=node["napalmInstance"]
        self.node=node["node"]
        self.device.open()
        self.output = self.device.get_interfaces()
        self.device.close()
        temp=filter.filtersFnMap("interfaces")(self.output,params)
        self.cli=temp[0]
        self.web=temp[1]
    def getOutput(self):
        return self.output

class macTable:
    def __init__(self, node,params=None):
        self.device=node["napalmInstance"]
        self.node=node["node"]
        self.device.open()
        self.output = self.device.get_mac_address_table()
        self.device.close()
        temp=filter.filtersFnMap("macTable")(self.output,params)
        self.cli=temp[0]
        self.web=temp[1]
    def getOutput(self):
        return self.output

class getVlans:
    def __init__(self, node,params=None):
        self.device=node["napalmInstance"]
        self.node=node["node"]
        self.device.open()
        self.output = self.device.get_vlans()
        self.device.close()
        temp=filter.filtersFnMap("getVlans")(self.output,params)
        self.cli=temp[0]
        self.web=temp[1]
    def getOutput(self):
        return self.output


class findRouteTo:
    def __init__(self, node,params=None):
        self.device=node["napalmInstance"]
        self.node=node["node"]
        self.device.open()
        if not params: params=["8.8.8.8"]
        self.output = self.device.get_route_to(destination=params[0])
        self.device.close()
        temp=filter.filtersFnMap("findRouteTo")(self.output)
        self.cli=temp[0]
        self.web=temp[1]
    def getOutput(self):
        return self.output

        
class ping:
    def __init__(self, node,params=None):
        self.device=node["napalmInstance"]
        self.node=node["node"]
        self.device.open()
        if not params: params=["8.8.8.8"]
        # print((params[1] if len(params)>1 else None))
        self.output = self.device.ping(
            destination=params[0] or "8.8.8.8",
            # source=(params[1] if len(params)>1 else ""),
            source_interface=(params[1] or "" if len(params)>1 else ""),
            count=(params[2] or 3 if len(params)>2 else 3),
        )
        # self.output = self.device.ping(
        #     destination=params[0],
        #     # source=(params[1] if len(params)>1 else ""),
        #     source_interface=(params[1] if len(params)>1 else ""),
        #     count=(params[2] if len(params)>2 else 3),
        # )
        self.device.close()
        temp=filter.filtersFnMap("ping")(self.output,params)
        self.cli=temp[0]
        self.web=temp[1]
    def getOutput(self):
        return self.output

class traceroute:
    def __init__(self, node,params=None):
        self.device=node["napalmInstance"]
        self.node=node["node"]
        self.device.open()
        if not params: params=["8.8.8.8"]
        # print((params[1] if len(params)>1 else None))
        self.output = self.device.traceroute(
            destination=params[0],
            # source=(params[1] if len(params)>1 else ""),
            # ttl=(params[2] if len(params)>2 else 64),
        )
        self.device.close()
        temp=filter.filtersFnMap("traceroute")(self.output)
        self.cli=temp[0]
        self.web=temp[1]
    def getOutput(self):
        return self.output

class getConfig:
    def __init__(self, node,params=None):
        self.device=node["napalmInstance"]
        self.node=node["node"]
        self.device.open()
        self.output = self.device.get_config()["running"]
        self.device.close()
        if len(params)>0: filter.filtersFnMap("getConfig")(self.output,node["node"]["hostname"]) 
        self.cli=self.output
        self.web=[{"title":"config","value":self.output}]
        # store configs
    def getOutput(self):
        return self.output

class cli:
    def __init__(self, node,params=None):
        self.device=node["napalmInstance"]
        self.node=node["node"]
        self.device.open()
        self.output = self.device.cli(params)
        self.device.close()
        filtered=[]
        for out in self.output:
            try:
                filtered.append({
                    out:parse_output(platform=TEMPLATEDICTIONARY[self.node["OS"]],command=out,data=self.output[out])
                })
                # print("Passed parsing for ",out)
            except Exception:
                # print("Failed to parse ",out)
                filtered.append({
                    out:self.output[out]
                })
        temp=filter.filtersFnMap("cli")(self.output,filtered)
        self.filtered=filtered
        self.cli=temp[0]
        self.web=temp[1]
    def getOutput(self):
        return self.output


#group what is in the self in a function
# def get_lldp_neighbors #def get_lldp_neighbors_detail(self, interface="")
# def get_bgp_neighbors  # def get_bgp_config(self, group="", neighbor="")
# def get_environment
# def get_interfaces_counters #get interface layer 2 stats
# def get_arp_table(self, vrf="") #get arp table from devices
# def get_interfaces_ip(self): #get ip addresses on interfaces
# def (self):

if __name__ == '__main__':
    print("MAIN FN in engine.py file")