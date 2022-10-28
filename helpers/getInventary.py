#!/home/kels/Documents/projects/netAutomation/autoMate/test_napalm/bin/python3
import json,yaml
from webbrowser import get
from IPy import IP
import functions.engineBase as engineInteractor

import helpers.files as files
# import files #test
ASSET_PATH="./assets/TESTDATA.json"
# ASSET_PATH="./assets/INVENTORYJSON.json"
    
def getState(name):
    try:
        path='./store/intents/'+name+".json"
        state=open(path)
        state=json.load(state)
        return state
    except Exception:
        print("ERROR")
        return {}

def findDevice(ip,index=None):
    devices=getDevices(0)
    for i,device in enumerate(devices):
        if device["IP"]["ip"]==ip:
            if index:
                return i+1 #index +1 to prevent boolean casting of 0
            else:
                return device
    return {}

def writeUpdate(devices):
    with open(ASSET_PATH, 'w', encoding='utf-8') as f:
        json.dump(devices, f, ensure_ascii=False, indent=4)

def addDevice(device):
    devices=getDevices(0)
    devices.insert(0,device)
    writeUpdate(devices)

def updateDevice(device):
    index=findDevice(device["oldIp"],index=True)
    del device["oldIp"]
    devices=getDevices(0)
    if index:
        index=index-1
        devices[index]=device
        writeUpdate(devices)

def deleteDevice(ip):
    index=findDevice(ip,index=True)
    devices=getDevices(0)
    if index:
        index=index-1
        del devices[index]
        writeUpdate(devices)

def getDevices(filter,checkIsAlive=False):
    """ 
        expects filters 
        0=>all devices
        1=>All routers
        2=>All switches
    """
    # ASSETS=open(ASSET_PATH)
    ASSETS=open(ASSET_PATH)

    # ASSETS=open("../assets/TESTDATA.json")

    ASSETS=json.load(ASSETS)
    list=[]
    if filter==0:
        list=ASSETS
    elif filter==1:
        for dev in ASSETS:
            if dev["deviceType"]=="router":
                list.append(dev)
    elif filter==2:
        for dev in ASSETS:
            if dev["deviceType"]=="switch":
                list.append(dev)

    if(checkIsAlive):
        temp= engineInteractor.index(nodes=list,type='get',engineFn='isAlive',params=[],timeout=1)
        list=[]
        for t in temp:
            # print(t)
            list.append(t.getOutput())
    return list


def takeInputs(notUsed):
    # "iosxr": "cisco_iosxr",
    print("""
enter IP-OS example 192.168.10.1-nxos,192.168.10.3-ios seperate each device with ','
[ios] would be used for IPs without OS specified 192.168.10.5 would become 192.168.10.5-ios 
IOS Guide
"ios" => Cisco ios, "nxos" => Cisco nexus, "eos" => Huawie, "junos" => Juniper junos
\n
    """)
    temps=input("Enter IPs-os: ").split(",")
    devices=[]
    try:
        for temp in temps:
            if temp:
                temp=temp.split('-')
                devOs=temp[1] if len(temp)>1 else "ios"
                devices.append({"hostname":str(IP(temp[0])),"decription":'------',"deviceType":None,"IP":{"ip":str(IP(temp[0]))},"Name":None,"OS":devOs})
        return devices
    except Exception:
        print("Invalid IP address provided")
        return takeInputs(1)


def generateInv():
    devices=getDevices(0)
    template={}
    for device in devices:
        if device['deviceType'] not in template:
            template[device['deviceType']]=[]
            template[device['deviceType']+':vars']=[
                'ansible_python_interpreter=/home/kels/Documents/projects/netAutomation/autoMate/test_napalm/bin/python3',
                'ansible_connection=network_cli',
                'ansible_ssh_pass=admin',
                'ansible_user=admin'
            ]
        
        # {'hostname': 'hubsw', 'decription': '', 'deviceType': 'switch', 'IP': {'ip': '192.168.122.167', 'mask': '255.255.255.0'}, 'Name': None, 'OS': 'ios'}
        template[device['deviceType']].append(
            '%s ip=%s ansible_network_os=%s'
            %(device['hostname'],device['IP']['ip'],device['OS'])
        )
    # create HOSTFILE
    STRING=''
    for key in template:
        STRING+='\n'
        STRING+='['+key+']\n'
        for line in template[key]:
            STRING+=line+'\n'
    # print(STRING)
    files.writeToTemp(STRING,name="host",tempdir='/store/temp/host/',extension="",MaxDays=0)
    # with open(STOREDIR+buffer['title']+'.json', 'w', encoding='utf-8') as f:
    #     json.dump(buffer, f, ensure_ascii=False, indent=4)



if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    # print("get inventory file")
    generateInv()