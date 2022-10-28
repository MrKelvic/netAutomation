import constants.commandsDictionary as cliReferences
import json
from yaspin import yaspin
from ntc_templates import parse
from textfsm import clitable
from termcolor import colored
spiner=yaspin(color="green")
INFO_CLOR="#217fb7"
DANG_CLOR="#eb0d0d"
ADD_CLOR="#389e0d"
# INTENT_PATH='/store/intents/'

def referenceInstruction(obj,instruction,interfaceId,nodeState):
    for refPoint in ['old','value']:
        # print(obj[instruction[1][0]])
        if refPoint in obj[instruction[1][0]]:
            additional=''
            for i in range(1,len(instruction[1])):
                if instruction[1][i] in obj:
                    additional+=' '+obj[instruction[1][i]][refPoint]
                else:
                    intSplit=[interfaceId[0:-1],int(interfaceId[-1])]
                    # print(nodeState['L3'][intSplit[0]]['members']) #[interfaceId[1]][instruction[1][i]]
                    additional+=' '+nodeState['L3'][intSplit[0]]['members'][intSplit[1]][instruction[1][i]]
            obj[instruction[1][0]][refPoint] = obj[instruction[1][0]][refPoint] + additional
    return obj

def handleRoutes():
    print("Handle routes")

def handleInterfaces(intCode,os,nodeState):
    print("Handle interfaces ",os)
    cli=[]
    for interfaceCode in intCode:
        # interface gig0/0
        cli.append({"data":'interface {}'.format(interfaceCode["id"]),"color":INFO_CLOR})
        print(colored(str('interface {}').format(interfaceCode["id"]), 'blue'))
        interfaceRef=interfaceCode["id"]
        interfaceCode=interfaceCode["changes"] #all changes
        # interface configs would not have ADDED nor REMOVED only CHANHED
        # Loop through CLI refrence for data plane
        refs=cliReferences.references('interfaces') or {}
        for ref in refs:
            # main loop
            for changesChild in ['added','changed','removed']:
                if ref not in interfaceCode[changesChild]:
                    # print("Skipping->> ",ref," in ",interfaceCode[changesChild])
                    continue

                # print("cONTINUE <<-- ",ref," in ",interfaceCode[changesChild])
                codeValues=interfaceCode[changesChild][ref] #{old:'',value:''}
                cmdLine=refs[ref][os]
                
                if type(cmdLine).__name__=="list":
                    # reference is an instruction
                    codeValues=referenceInstruction(interfaceCode[changesChild],cmdLine,interfaceRef,nodeState['interfaces'])[ref]
                    cmdLine=cmdLine[0]

                # check if type of value is boolean
                if type(codeValues["value"]).__name__ == 'bool':
                    negate='no ' if codeValues["old"] else ''
                    cli.append({"data":str(negate+cmdLine),"color":DANG_CLOR})
                    print(colored(str(negate+cmdLine), 'red'))
                    negate='no ' if codeValues["value"] else ''
                    cli.append({"data":str(negate+cmdLine),"color":ADD_CLOR})
                    print(colored(str(negate+cmdLine), 'green'))
                else:
                    if changesChild in ['added','changed']:
                        if 'old' in codeValues:
                            cli.append({"data":str('no '+cmdLine).format(codeValues['old']),"color":DANG_CLOR})
                            print(colored(str('no '+cmdLine).format(codeValues['old']), 'red'))
                            cli.append({"data":str(cmdLine).format(codeValues['value']),"color":ADD_CLOR})
                            print(colored(str(cmdLine).format(codeValues['value']), 'green'))
                        else:
                            cli.append({"data":str(cmdLine).format(codeValues['value']),"color":ADD_CLOR})
                            print(colored(str(cmdLine).format(codeValues['value']), 'green'))
                    else:
                        # removing
                        cli.append({"data":str('no '+cmdLine).format(codeValues['value']),"color":DANG_CLOR})
                        print(colored(str('no '+cmdLine).format(codeValues['value']), 'red'))

        # Loop through changed
        # for change in interfaceCode[changesChild]


def index(code,node):
    configArray=[]
    # print(code)
    interfacesConfig=handleInterfaces(code['interfaces'],node['node']["OS"],node['state'])


if __name__ == '__main__':
    print(" -- Convert code to config -- ")




