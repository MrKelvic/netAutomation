#!/home/kels/Documents/projects/netAutomation/autoMate/test_napalm/bin/python3
import sys
from IPy import IP

#import write to temp helper
import helpers.files as fileHelper

def filtersFnMap(key):
    maps={
        "info":infoFilters,#dictionary
        "interfaces":interfacesFilters,
        "macTable":macTableFilters,
        "getVlans":getVlansFilters,
        "ping":pingFilters,
        "findRouteTo":findRouteToFilters,
        "traceroute":tracerouteFilters,
        "cli":cliFilters,
        # No params
        "getConfig":getConfigFilters,
    }
    if key in maps:
        return maps[key]
    else:
        return maps["info"]

def regroupArray(arr,lim,strin):
    ret=[]
    temp=[]
    for item in arr:
        if len(temp) > lim:
            ret.append(strin.join(temp))
            temp=[]
        else:
            temp.append(item)
    if (len(temp)<lim+1) and (len(temp)>0):
        ret.append(strin.join(temp))
    return ret

def CLIDictionary(data):
    cliOut=[[]]
    for attrib in data:
        if type(data[attrib]).__name__ == "list":
            cliOut.append([attrib,'\n'.join(regroupArray(data[attrib],4,'\t'))])
        else:
            cliOut.append([attrib,data[attrib]])
    return cliOut

def CLIArrayDictionary(data):
    cliOut=[]
    if len(data)<1: return []
    # headers
    m=[]
    for header in data[0]:
        m.append(header)
    cliOut.append(m)
    for out in data:
        m=[]
        for attrib in out:
            m.append(out[attrib])
        cliOut.append(m)
    return cliOut

def WebDictionary(data):
    # print("THIS IS WebDictionary")
    # print(data)
    return [
        {
            "title":"result",
            "value":[data]
        }
    ]
    # webOut=[]
    # for attrib  in data:
    #     webOut.append({
    #         "title":attrib,
    #         "value":data[attrib]
    #     })
    # return webOut 

def WebArrayDictionary(data):
    # print("THIS IS WebArrayDictionary")
    """ 
    //Interface
    [{'interface': 'GigabitEthernet0/0', 'state': True, 'connected': True, 'description': '', 'mac_address': '0C:0F:5D:53:00:00', 'speed': 1000.0}]

    """
    webOut=[]
    # for item in data:
    # return webOut
    webOut=[]
    for item in data:
        for attrib  in item:
            webOut.append({
                "title":attrib,
                "value":item[attrib]
            })
    return webOut



# ###########################################################
def infoFilters(raw):
    # print(raw)
    # print(WebDictionary(raw))
    return [CLIDictionary(raw),WebDictionary(raw)]

def titleValuePair(raw):
    filtered=[]
    for attrib  in raw:
        filtered.append({
            "title":attrib,
            "value":raw[attrib]
        })
    # print(filtered)
    return filtered 

def interfacesFilters(raw,params):
    # print(params)
    # print("\n")
    # print("\n")
    # print("\n")
    # print("\n")
    if len(params)>0:
        if params[0]:
            raw={params[0]:raw[params[0]]}
    map={"is_up":"connected","is_enabled":"state"}
    remove=["mtu","last_flapped","speed"]
    preped=[]
    for out in raw:
        obj={}
        obj["interface"]=out
        for attrib in raw[out]:
            if attrib not in remove:
                if attrib in map:
                    obj[map[attrib]]=raw[out][attrib]
                else:
                    obj[attrib]=raw[out][attrib]
        preped.append(obj)
    return [CLIArrayDictionary(preped),WebArrayDictionary([{"result":preped}])]


def macTableFilters(raw,params):
    retData=raw
    if len(params)>0:
        # loop search
        if params[0]:
            retData=[]
            for item in raw:
                if item['mac'] == params[0]:
                    retData=[item]
    # print(tabulate(CLIArrayDictionary(raw)))
    # [{"result":raw}]
    return [CLIArrayDictionary(raw),WebArrayDictionary([{"result":retData}])]

def getVlansFilters(raw,params):
    # print(params,raw[str(params[0])])
    if len(params)>0:
        raw={str(params[0]):raw[str(params[0])]}
    preped=[]
    for attrib in raw:
        raw[attrib]["VLAN_ID"]=attrib
        raw[attrib]["interfaces"]='\n'.join(regroupArray(raw[attrib]["interfaces"],2,','))
        preped.append(raw[attrib])
    # print(tabulate(CLIArrayDictionary(preped)))
    return [CLIArrayDictionary(preped),WebArrayDictionary([{"result":preped}])]

def findRouteToFilters(raw):
    remove=["inactive_reason","last_active","protocol_attributes"]
    map={"preference":"Administrative_Distance","current_active":"is_active"}
    preped=[]
    for attrib in raw:
        for item in raw[attrib]:
            obj={"destination":attrib}
            for attr in item:
                if attr not in remove:
                    if attr in map:
                        obj[map[attr]]=item[attr]
                    else:
                        obj[attr]=item[attr]
            preped.append(obj)

    # print(tabulate(CLIArrayDictionary(preped)))
    return [CLIArrayDictionary(preped),WebArrayDictionary([{"result":preped}])]

def pingFilters(raw,params):
    """ 
     File "/home/kels/Documents/projects/netAutomation/autoMate/functions/filter.py", line 166, in pingFilters
    "successful_pings":len(raw["success"]["results"])+"/"+raw["success"]["probes_sent"],
TypeError: unsupported operand type(s) for +: 'int' and 'str'
    """
    if "success" in raw:
        # print(raw)
        p=int(raw["success"]["probes_sent"]) or 1
        raw={
            "probes_sent":raw["success"]["probes_sent"],
            "sourced":params[1] if len(params)>1 else "Default",
            "target":params[0],
            "successful_pings":str(len(raw["success"]["results"]))+"/"+str(raw["success"]["probes_sent"]),
            "packet_loss":str(float(int(raw["success"]["packet_loss"])/p)*100)+'%',
            # "max_return_time":raw["success"]["rtt_max"],
            "avg_return_time":str(raw["success"]["rtt_avg"])+"ms",
            }
    
    # print(tabulate(CLIDictionary(raw)))
    return [CLIDictionary(raw),WebDictionary(raw)]
    

def tracerouteFilters(raw):
    preped=[]
    if "error" in raw:
        return [CLIDictionary(raw),WebDictionary(raw)]
    else:
        for req in raw["success"]:
            for item in raw["success"][req]["probes"]:
                obj={}
                for probe in raw["success"][req]["probes"][item]:
                    obj[probe]=raw["success"][req]["probes"][item][probe] if raw["success"][req]["probes"][item][probe] else "*"*14
                preped.append(obj)

    # print(tabulate(CLIArrayDictionary(preped)))
    return [CLIArrayDictionary(preped),WebArrayDictionary([{"result":preped}])] 


# expects config and nodeName
def getConfigFilters(raw,name="test"):
    fileHelper.writeToTemp(raw,name)
    return None 

def cliFilters(raw,cleanedForWeb):
    # print("cleanForWeb ",cleanedForWeb)
    for outAr,output in enumerate(cleanedForWeb):
        for commandOutput in output:
            # print(commandOutput)
            if type(output[commandOutput]).__name__ == 'list':
                for inAr,obj in enumerate(output[commandOutput]):
                    newObj={}
                    for key in obj:
                        filtered=[
                            "uptime_years","uptime_weeks","uptime_days","uptime_hours","uptime_minutes","reload_reason","restarted","rommon",
                            "hardware_type","bia","mtu","media_type","encapsulation","last_input","last_output","last_output_hang","queue_strategy",
                            "abort","output_rate","input_rate"
                            ]
                        if key not in filtered:
                            newObj[key]=obj[key] if type(obj[key]).__name__ =="str" else (obj[key][0] if len(obj[key])>0 else "")
                            # print(type(obj[key])," ",obj[key])
                            #  if type(obj[key]) =="str" else obj[key][0]
                            # print(key)
                    cleanedForWeb[outAr][commandOutput][inAr]=newObj
        # print(output)

    print('\n \n')
    return [CLIDictionary(raw),WebArrayDictionary(cleanedForWeb)]


if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    print("Params file")