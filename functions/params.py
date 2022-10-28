#!/home/kels/Documents/projects/netAutomation/autoMate/test_napalm/bin/python3
import sys
from IPy import IP

def paramsFnMap(key):
    maps={
        "info":noParams,
        "interfaces":interfacesParams,#DONE
        "macTable":macTableParams,
        "getVlans":getVlansParams,
        "ping":pingParams,#DONE
        "traceroute":tracerouteParams,#DONE
        "findRouteTo":tracerouteParams,#DONE
        "cli":cliParams,#DONE
        # No params
        "getConfig":getConfigParams,#DONE
    }
    if key in maps:
        return maps[key]
    else:
        return maps["info"]

def noParams():
    return None

def interfacesParams(local=None):
    mapInt={"G":"GigabitEthernet","F":"FastEthernet","L":"Loopback","V":"Vlan","P":"Port-channel","C":"Cellular","T":"Tunnel"}
    if not local:
        local="[All interfaces]"
        print("""
Enter specific interface to fetch example;
g0/0 => GigabitEthernet0/0, f0/0 => FastEthernet0/0, l2 => Loopback2, p3 => Portchannel3, t2 => Tunnel2, c1 =>Cellular1
    """)
    paramsList=input("%s : " %local)
    if paramsList:
        key=str.upper(paramsList[0])
        if key in mapInt: 
            interfaceString=mapInt[key]
            paramsList=[interfaceString+paramsList.split(paramsList[0])[1]]
        else:
            paramsList=[]
    else:
        paramsList=[]
    return paramsList

def macTableParams():
    print("""
Enter specific MAC address to fetch example; 0C:0D:4F:90:00:01
    """)
    paramsList=input("[All MAC address] : ")
    if not paramsList:
        return []

    return [paramsList]

def getVlansParams():
    paramsList=input("Enter VLAN Number [all] : ")
    if not paramsList:
        return []
    try:
        paramsList=int(paramsList)
    except Exception:
        print("Expected number")
        return []
    return [paramsList]

def pingParams():
    paramsList=[]
    # Destination IP
    value=input("Enter Ping destination IP [8.8.8.8]: ")
    try:
        value=str(IP(value))    
    except Exception:
        print("Invalid IP address provided defaulting to 8.8.8.8")
        value=str(IP("8.8.8.8"))
    paramsList.append(value)
    # source_interface
    value=interfacesParams("Enter ping source interface [None]")
    value=value[0] if len(value)>0 else ""
    paramsList.append(value)
    # ping counter
    value=input("Enter ping counter [3]: ")
    try:
        value=int(value)
        value=value+0    
    except Exception:
        print("Expected a number defaulting to 3")
        value=3
    paramsList.append(value)
    return paramsList

def tracerouteParams():
    paramsList=[]
    # Destination IP
    value=input("Enter Ping destination IP [8.8.8.8]: ")
    try:
        value=str(IP(value))    
    except Exception:
        print("Invalid IP address provided defaulting to 8.8.8.8")
        value=str(IP("8.8.8.8"))
    paramsList.append(value)
    return paramsList

def getConfigParams():
    paramsList=False
    paramsList=input("Save config in temp y/n [n]")
    paramsList = True if str.upper(paramsList)=="Y" else False  
    return [paramsList]

def cliParams():
    paramsList=[]
    print("""
Enter CLI commands in order you would have typed in a CLI seperated by ','
example interface g0/0, switch host, switch access mode vlan 10
to setup an access port (g0/0) on VLAN 10
CLI shortcuts are allowed int g0/0 == interface g0/0
    """)
    value=input("Commands : ").split(",")
    for cli in value:
        if cli: paramsList.append(cli)
        
    return paramsList



if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    print("Params file")
    interfacesParams()