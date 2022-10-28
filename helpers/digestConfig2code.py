#!/home/kels/Documents/projects/netAutomation/autoMate/test_napalm/bin/python3
import sys
from IPy import IP
import helpers.confparser as confparser
import helpers.interfaceMapper as interfaceMapper



def mapper(plane):
    m= {
        "interfaces":interfaces,
        "routes":routes,
        "policies":policies,
    }
    if plane in m:
        return m[plane]

def index(state):
    for plane in state:
        state[plane]=mapper(plane)(state[plane])
    return state


def policies(param):
    # print(param)
    return param

def routes(param):
    # print(param)
    return param
        


def interfaces(param):

    interfaceDict={
        "L2":{},
        "L3":{}
    }
    for interface in param:
        # print(interface,param[interface])
        #Skip default vlans
        skip=["1002","1003","1004","1005"]
        if param[interface]["type"]=="Vlan" and param[interface]["id"] in skip:
            continue

        #check interface type
        type="L3" #L3 =>true
        if "isSwitchport" in param[interface]:
            type="L2" #L2 => false
        #check if module exists
        module=param[interface]["module"]#param[interface]["type"]+param[interface]["identifier"]
        if module not in interfaceDict[type]:
            interfaceDict[type][module]={
                "members":[]
            }
        tempForshNm=interfaceMapper.breakDown(module+param[interface]["id"])
        baseState={
            "id":param[interface]["id"],
            "shortName":interfaceMapper.reverse(tempForshNm[0])+tempForshNm[1]+tempForshNm[2],
            "fullName":module+param[interface]["id"],
            "module":module,
            "state":False if "admin" in param[interface]["state"] else True,
            "connected":False if "down" in param[interface]["connected"] else True,
            # "layer":type,
            "routed":True if type=="L3" else False,
            "description":param[interface]["description"],
            "outgoing_acl":param[interface]["outgoing_acl"],
            "inbound_acl":param[interface]["inbound_acl"],
        }
        if type=="L2":
            baseState["mode"]="access" if param[interface]["mode"] !="trunk" else "trunk"
            baseState["allowedVlans"]=param[interface]["trunking_vlans"]
            baseState["voice"]=str.lower(param[interface]["trunking_vlans"][0])
            baseState["data"]=param[interface]["access_vlan"]
            baseState["nativeVlan"]=param[interface]["native_vlan"]
        else:
            baseState["ip"]=param[interface]["ip"]
            baseState["mask"]=param[interface]["mask"]
            baseState["ip_helper"]=param[interface]["ip_helper"]

        # check if interface is a sub interface
        if 'parent' in param[interface]:
            baseState['parent']=param[interface]['parent']
            baseState['subId']=param[interface]['subId']

        if param[interface]["type"]=="Vlan":
            baseState["name"]=param[interface]["name"]
        # print('\n')
        interfaceDict[type][module]["members"].append(baseState)
        

    # print(interfaceDict)
    return interfaceDict


if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    print("Params file")