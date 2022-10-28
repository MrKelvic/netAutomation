# import functions.filter as filter
# import filter #test
# from tabulate import tabulate
import json
from yaspin import yaspin
spiner=yaspin(color="green")
# from jinja2 import Template
from jinja2 import Environment, FileSystemLoader


def preprocessIntent(intentPath):
    intent=open(intentPath)
    intent=json.load(intent)

    mapInt={"G":"GigabitEthernet","F":"FastEthernet","L":"Loopback","V":"Vlan","P":"Port-channel","C":"Cellular","T":"Tunnel"}

    for interface in intent['interfaces']:
        if 'extras' not in interface:
            interface['extras']=['!']
        if len(interface['extras']) <1:
            interface['extras']=['!']
        processed=[]
        for intRange in interface['ranges']:
            # print(intRange)
            for intNo in range(intRange[0],(intRange[1]+1 if len(intRange)>1 else intRange[0]+1)):
                # print(intNo)
                temp=list(str.upper(interface["identifier"]))
                # print(interface['identifier'])
                idenv=mapInt[temp.pop(0)]
                temp=idenv+(''.join(temp))
                processed.append(temp+str(intNo))
        del interface['ranges']
        # print(processed)
        interface['interfaces']=processed
    return intent
    
    # print(intent['interfaces'])



def index(intentPath):
    # configJSON
    file_loader = FileSystemLoader('../store/templates/')
    env = Environment(loader=file_loader)
    env.lstrip_blocks = True
    template = env.get_template('test.j2')
    intent=preprocessIntent(intentPath)
    output = template.render(config=intent,trim_blocks=True)

    # write to file
    print(output)
    # return proccessedRequest



if __name__ == '__main__':
    # print("MAIN FN in engine.py file")
    index("/home/kels/Documents/projects/netAutomation/autoMate/store/intents/basebranchsw.json")