#!/home/kels/Documents/projects/netAutomation/autoMate/test_napalm/bin/python3


#local imports
import helpers.getInventary as getInventary
import functions.params as params
# seperated by ','\n Example 192.168.1.1,192.168.2.3
def index():
    PROMPTS_1={
        "hint":"What action would you want to perform",
        "options":["get data","push config"],
        "optionDictMap":["get","post"],
        "target":"action",
        "get":{
            "hint":"What devices do you want to perform action on",
            "options":["All devices in local inventory","All routers","All switches","Enter specific IPs","Read from file"],
            "optionDictMap":["gotoInventary","gotoInventary","gotoInventary","getTargets","readIpsFrmFile"],
            "gotoInventary":getInventary.getDevices,
            "getTargets":getInventary.takeInputs,
            "target":"nodes"
        }
    }
    PROMPTS_GETS={
        "hint":"Select action",
        "options":["Device Info","Check Interfaces","Check MAC Table","Get Vlans","Ping an IP","Tracert an IP","Find route used for an IP","Get Device Config","Enter CLI command"],
        "optionDictMap":["info","interfaces","macTable","getVlans","ping","traceroute","findRouteTo","getConfig","cli"],
        "target":"engineFn",
        "info":{
            "init":params.paramsFnMap("info"),
            "target":"params"
        },
        "interfaces":{
            "init":params.paramsFnMap("interfaces"),
            "target":"params"
        },
        "macTable":{
            "init":params.paramsFnMap("macTable"),
            "target":"params"
        },
        "getVlans":{
            "init":params.paramsFnMap("getVlans"),
            "target":"params"
        },
        "ping":{
            "init":params.paramsFnMap("ping"),
            "target":"params"
        },
        "traceroute":{
            "init":params.paramsFnMap("traceroute"),
            "target":"params"
        },
        "findRouteTo":{
            "init":params.paramsFnMap("findRouteTo"),
            "target":"params"
        },
        "getConfig":{
            "init":params.paramsFnMap("getConfig"),
            "target":"params"
        },
        "cli":{
            "init":params.paramsFnMap("cli"),
            "target":"params"
        }
    }
    return [PROMPTS_1,{"get":PROMPTS_GETS}]





if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    print("controller prompts.py file")