import constants.commands as constcommands
# import functions.engineBase as engineBase #test
# import helpers.getInventary as getInventary #test
import functions.engineBase as engineBase 
import helpers.getInventary as getInventary 
import helpers.parseConfigGetter as parseConfigToIntent 
import helpers.digestConfig2code as digestConfig2code 
import helpers.files as files 
# import filter #test
# from tabulate import tabulate
import json
from yaspin import yaspin
from ntc_templates import parse
from textfsm import clitable
spiner=yaspin(color="green")

INTENT_PATH='/store/intents/'


def index(nodes=[],write=True):
    nodes=nodes if len(nodes)>0 else getInventary.getDevices(1)
    ret=[]
    # configJSON

    # t=t.split('\n')
    # for line in t:
    #     # print(line.find("show"))
    #     try:
    #         l=line[line.find("show"):line.find(".textfsm")]
    #         print('"%s",'%(" ".join(l.split("_"))))
    #     except Exception:
    #         l=0
    # 192.168.122.207
    action=constcommands.configOptions('ios')
    commands=[]
    fns=[]
    for data in action:
        commands.append(data)
        fns.append(action[data])
    # print("RUNNING COMMANDS")
    cliOutPut=engineBase.index(nodes,None,"cli",commands)
    # print("COMMANDS DONE")
    for output in cliOutPut:
        STATE={}
        for i,filtered in enumerate(output.filtered):
            # print("PROCESSING PHASE 1")
            STATE=parseConfigToIntent.mapper(output.node["OS"],fns[i][0])(
                STATE,
                filtered[commands[i]],
                fns[i][1],
                fns[i][2],
                fns[i][3] if len(fns[i])>3 else None,
                fns[i][3] if len(fns[i])>4 else None
            )
        # print("PROCESSING PHASE 2")
        STATE=digestConfig2code.index(STATE)
        if write:
            files.writeToTemp(json.dumps(STATE),name=output.node["hostname"]+"_"+output.node["IP"]["ip"],tempdir=INTENT_PATH,extension=".json",MaxDays=1)
        ret.append({
            "node":output.node,
            "state":STATE
        })
    # print("COMPLETED")
    return ret

if __name__ == '__main__':
    # print("MAIN FN in engine.py file")
    index(getInventary.getDevices(1))

# username admin priv 15 secr admin
# ip domain-name auto.net
# crypto key generate rsa modulus 1024
# ip ssh version 2
# confi ter
# line vty 0 4
# login local
# transport input ssh
# exit
# end
# wr



