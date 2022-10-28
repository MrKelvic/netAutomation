#!/home/kels/Documents/projects/netAutomation/autoMate/test_napalm/bin/python3
from lib2to3.pgen2 import driver
import napalm

#Local imports
import functions.engine as engine
# import engine #test


def index(nodes,type=False,engineFn="info",params=[],timeout=60):
    """
        nodes Expects filtered inventory list, generate Napalm instances and push to array 
        type True// making config //False getting configs
        params //parameters 
        returns {"engineFn":String,"devices":DEVICES(variable)}
    """
    napalmDeviceInstances=[]#List of Napalm devices
    # print(len(nodes)," BASE")
    for node in nodes:
        driver=napalm.get_network_driver(node["OS"])
        nodeNapalmInstance=driver(hostname=node["IP"]["ip"],username="admin",password="admin",timeout=timeout,
        optional_args=({'global_delay_factor': 4} if engineFn=="cli" else {})
        )
        napalmDeviceInstances.append({"napalmInstance":nodeNapalmInstance,"node":node})

    return engine.index({"engineFn":engineFn,"params":params,"nodes":napalmDeviceInstances})
    # engine.index({"engineFn":"cli","params":params,"nodes":napalmDeviceInstances})






if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
   print()