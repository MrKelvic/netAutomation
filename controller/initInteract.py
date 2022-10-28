import os
import sys
from time import sleep
from yaspin import yaspin
import pyfiglet
#Local imports
import controller.prompts as prompts

NAVIGATE={
    "level":0
}

clear=lambda:os.system("clear")
spiner=yaspin(color="white")
TOENGINE={
    
}

def index():
    interact(prompts.index()[0])
    interact(prompts.index()[1][TOENGINE["action"]])
    spiner.stop()
    return TOENGINE

def interact(prompts):
    clear()
    spiner.stop()
    print(pyfiglet.figlet_format("Network spool"))
    if "options" in prompts:
        next=listAndTakeInput(prompts["options"],hint=(prompts["hint"] if "hint" in prompts else None))
        nextType=type(prompts[prompts["optionDictMap"][next]]).__name__
    else:
        # reach the end of prompts
        nextType="dict"
    target=prompts["target"] if "target" in prompts else None
    # print(prompts)
    if nextType=="dict":
        # check if it has an int
        if "init" in prompts:
            # then we about to exec a command
            TOENGINE[target]=prompts["init"]()
            spiner.start()
        else:
            TOENGINE[target]=prompts["optionDictMap"][next]
            interact(prompts[prompts["optionDictMap"][next]])
    elif nextType=='function':
        TOENGINE[target]=prompts[prompts["optionDictMap"][next]](next)
        spiner.start()
        # print()

def listAndTakeInput(options,hint):
    if hint: print(hint)
    for i,option in enumerate(options):
        print("[%s]-%s" %(i+1,option))
    try:
        selected=int(input())
        if len(options)<selected: raise Exception
        selected=selected-1
    except Exception:
        print("Invalid option")
        sleep(1)
        clear()
        listAndTakeInput(options)
    return selected



if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    # print("controller initInteract.py file")
    index()