#!/home/kels/Documents/projects/netAutomation/autoMate/test_napalm/bin/python3
import sys
import uuid
from IPy import IP
import helpers.confparser as confparser
import helpers.interfaceMapper as interfaceMapper

#import write to temp helper
# import helpers.files as fileHelper
def mapper(device,key):
    m= {
        "ios":{
            "interfaces":interfaces,
            "routes":routes,
            "policies":policies,
        }
    }
    if device in m:
        if key in m[device]:
            return m[device][key]

def policies(state,values,key,description,stringToJsonRule=None,AllowString=False):
    # return state
    stateTemplate={}
    if type(values).__name__ =='str' and not AllowString:
        return state

    pKey="policies"
    if pKey not in state:
        state[pKey]={}
        stateTemplate[pKey]={}

    refKey=key
    if key not in state[pKey]:
        state[pKey][refKey]=[]
        stateTemplate[pKey][refKey]=[]

    if key=="acl":
        guard="action"

    for value in values:
        compute_value={}
        if not (value[guard] if guard else True):
            continue
        for keyPair in description:
            if value[keyPair]:
                compute_value[description[keyPair]]=value[keyPair]
        state[pKey][refKey].append(compute_value)
        stateTemplate[pKey][refKey].append(compute_value)

    # print(stateTemplate)
    return state

def cleanOSPF(dictionary,idKey,forceToObj=None):
    # print(dictionary)
    ret=[]
    for key in dictionary:
        obj={}
        obj[idKey]=key
        for force in ["passive","noPassive","network"]:
            if force in dictionary[key]:
                 if type(dictionary[key][force]).__name__!="list":
                    dictionary[key][force]=[dictionary[key][force]]

        for childEle in dictionary[key]:
            if (childEle in forceToObj):
                if type(dictionary[key][childEle]).__name__!="list":
                    dictionary[key][childEle]=[dictionary[key][childEle]]
                for iX,value in enumerate(dictionary[key][childEle]):
                    # print(value)
                    if not value:
                        continue
                    dividedValues=value.split(" ")
                    parsedObj={"uid":uuid.uuid4().hex}
                    for iV,dividedValue in enumerate(dividedValues):
                        # Loop through divided values 
                        if forceToObj[childEle][iV]:
                            parsedObj[forceToObj[childEle][iV]]=dividedValue
                    dictionary[key][childEle][iX]=parsedObj
            obj[childEle]=dictionary[key][childEle]
        ret.append(obj)
    # print(ret)
    return ret

def routes(state,values,key,description,stringToJsonRule=None,AllowString=False):
 
    if type(values).__name__ =='str' and not AllowString:
        return state

    # print(confparser.Dissector(stringToJsonRule).parse_str(values))
    if key=="ospf":
        values=cleanOSPF(confparser.Dissector(stringToJsonRule).parse_str(values),
        "pid", {
        # "passive":['interface'],
        # "noPassive":['interface'],
        "network":["network","wildcard",None,"area"]
        })
    elif key=="eigrp":
        values=cleanOSPF(confparser.Dissector(stringToJsonRule).parse_str(values),
        "asn",{
        # "passive":None,
        # "noPassive":None,
        "network":["network","wildcard"]
        })
    elif key=="static":
        values=confparser.Dissector(stringToJsonRule).parse_str(values)
        # print(key)
        if type(values["route"]).__name__=="str":
            values["route"]=[values["route"]]
        # else:
        #     values=values["route"]

        values=cleanOSPF({"0":values},
        "static",{
        "route":["network","mask","next_hop","AD"]
        })
        # print(values)

    pKey="routes"
    if pKey not in state:
        state[pKey]={}

    refKey=key
    if key not in state[pKey]:
        state[pKey][refKey]=[]
    for value in values:
        state[pKey][refKey].append(value)
    return state
        


def interfaces(state,values,key,description,stringToJsonRule=None,AllowString=False):
    """
        state,
        value => output from cli,
        key what to set as key, 
        description ( key to look for and name to give key in state obj) 
    """
    if type(values).__name__ =='str':
        return state

    pKey="interfaces"
    if pKey not in state:
        state[pKey]={}

    key=str(key).split("-")
    for value in values:
        refKey=value[key[0]]
        if len(key)>1:
            refKey=key[1]+refKey
        breakDown=interfaceMapper.breakDown(refKey)
        refKey=breakDown[-1]
        if refKey not in state[pKey]:
            state[pKey][refKey]={}
        
        state[pKey][refKey]["type"]=breakDown[0]
        state[pKey][refKey]["identifier"]=breakDown[1]
        state[pKey][refKey]["id"]=breakDown[2]
        state[pKey][refKey]["module"]=breakDown[0]+breakDown[1]
        # Check if it's a sub interface
        if len(breakDown)>5:
            state[pKey][refKey]["parent"]=breakDown[4]
            state[pKey][refKey]["subId"]=breakDown[5]
        # param[interface]["type"]+param[interface]["identifier"]
        for fKey in description:
            state[pKey][refKey][description[fKey]]=value[fKey]

        if key[0] == "intf":
            if len(value["ipaddr"])>0:
                tempIp=[
                    (value["ipaddr"] if type(value["ipaddr"]).__name__=='str' else value["ipaddr"][0]),
                    (value["mask"] if type(value["mask"]).__name__=='str' else value["mask"][0]),
                ]
                ip=str(IP(str(tempIp[0]+'/'+tempIp[1]),make_net=True).strNormal(2)).split("/")
                state[pKey][refKey]["ip"]=tempIp[0] #ip[0]
                state[pKey][refKey]["mask"]=ip[1]
            else:
                state[pKey][refKey]["ip"]=""
                state[pKey][refKey]["mask"]=""

    return state

# int gi0/2    
# ip address 172.16.40.2 255.255.255.252
# no shut
# router ospf 1
# router-id 4.4.4.4
# network 172.16.40.0 0.0.0.3 area 1
# network 192.168.122.13 0.0.0.255 area 2
# crypto key generate rsa modulus 1028
# ip ssh version 2
# config ter
# interface range gi0/1
# no shu
# end








if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    print("Params file")
#     cleanOSPF({
#     "2": {
#         "network": [
#             "10.100.130.0 0.0.0.255 area 3",
#             "10.100.200.0 0.0.0.255 area 1",
#             "10.100.230.0 0.0.0.255 area 3"
#         ]
#     },
#     "4": {
#         "passive": "default",
#         "noPassive": [
#             "GigabitEthernet0/0",
#             "GigabitEthernet0/1",
#             "GigabitEthernet0/2",
#             "GigabitEthernet0/3"
#         ],
#         "network": [
#             "180.40.10.0 0.0.0.3 area 6",
#             "190.10.10.0 0.0.0.3 area 2",
#             "190.40.10.0 0.0.0.3 area 3"
#         ]
#     }
# }, "pid", {
#         # "passive":['interface'],
#         # "noPassive":['interface'],
#         "network":["network","wildcard",None,"area"]
#         })