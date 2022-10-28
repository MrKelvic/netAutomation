#!/home/kels/Documents/projects/netAutomation/autoMate/test_napalm/bin/python3
import controller.initInteract as interactor 
import functions.engineBase as engineInteractor
import helpers.writeToExcel as writeToExcel


def index(isCLI):
    fuel=interactor.index()
    output =engineInteractor.index(nodes=fuel["nodes"],type=fuel["action"],engineFn=fuel["engineFn"],params=fuel["params"])
    if isCLI:
        writeToExcel.index(output)





if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    index(True)