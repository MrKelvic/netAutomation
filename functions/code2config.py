import constants.commandsDictionary as cliReferences
import json
from yaspin import yaspin
from ntc_templates import parse
from textfsm import clitable
from termcolor import colored
spiner=yaspin(color="green")
INFO_CLOR="#239ae1"
DANG_CLOR="#e33030"
ADD_CLOR="#6acf40"
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
                            if not codeValues['value']:
                                continue
                            cli.append({"data":str(cmdLine).format(codeValues['value']),"color":ADD_CLOR})
                            print(colored(str(cmdLine).format(codeValues['value']), 'green'))
                        else:
                            if not codeValues['value']:
                                continue
                            cli.append({"data":str(cmdLine).format(codeValues['value']),"color":ADD_CLOR})
                            print(colored(str(cmdLine).format(codeValues['value']), 'green'))
                    else:
                        # removing
                        if not codeValues['value']:
                            continue
                        cli.append({"data":str('no '+cmdLine).format(codeValues['value']),"color":DANG_CLOR})
                        print(colored(str('no '+cmdLine).format(codeValues['value']), 'red'))
    return cli

        # Loop through changed
        # for change in interfaceCode[changesChild]

def referenceInstructionCntrl(codeValues,instruction):
    baseCmd=instruction[0]
    for child in instruction[1]:
        if child in codeValues:
            baseCmd+=' '+str(codeValues[child])
    return ('' if baseCmd==instruction[0] else baseCmd)


def handleRoutes(intCode,os,nodeState):
    print("Handle Routes ",os)
    cli=[]
    refs=cliReferences.references('routes') or {}
    # Jump straight into changes objs
    for actionType in ['added','changed','removed']:
        if len(intCode) == 0:
            return []
        for actionObj in intCode[actionType]:#loop action array
            # changed:{key:'',value:{AD:1,mask:0}}
            topRefs=refs[actionObj['key']][os]#get reference from dict using actioObj key
            # can have "value" or "old"
            for varType in ['old',"value"]:
                if varType in actionObj:
                    valueDict=actionObj[varType] #list of values in actionObj
                    for ref in topRefs:
                        clr=ADD_CLOR
                        # print(topRefs[ref])
                        if not valueDict[ref]:
                            continue
                        cmd=str(topRefs[ref]).format(valueDict[ref])
                        if type(topRefs[ref]).__name__=="list":
                            cmd=referenceInstructionCntrl(valueDict,topRefs[ref])

                        if ref in ['asn','pid']:
                            if varType in ['old']:
                                continue

                            clr=INFO_CLOR
                        if (varType in ['old'] or actionType in ['removed']) and ref not in ['pid']:
                            clr=DANG_CLOR
                            cmd='no '+cmd

                        prClrMap={
                            "#239ae1":'blue',
                            "#e33030":'red',
                            "#6acf40":'green'
                        }
                        print(colored(cmd,prClrMap[clr]))
                        cli.append({"data":cmd,"color":clr})
    return cli
                            


def index(code,node):
    dataPlanePlaneConfig=handleInterfaces(code['interfaces'],node['node']["OS"],node['state'])
    controlConfig=handleRoutes(code['routes'],node['node']["OS"],node['state'])
    return dataPlanePlaneConfig+controlConfig



if __name__ == '__main__':
    print(" -- Convert code to config -- ")




