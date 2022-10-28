#TEST FUNCTIONS IN DEV ENV
import functions.config2code as playRun
import api.index as apiTest

def index():
    apiTest.index()
    # playRun.index()





if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    index()