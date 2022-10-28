from fileinput import filename
import sys,os,platform
from datetime import date, datetime

clear=lambda:os.system("clear")
DIR =(os.path.dirname(os.path.realpath(__file__))).split('/')
DIR.pop()
DIR='/'.join(DIR)



def checkDateCreated(filePath):
    if platform.system() == 'Windows':
        return os.path.getctime(filePath)
    else:
        stat = os.stat(filePath)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime


def findFile(dir,root=False):
    clear()
    if root:dir="~/"
    print("file/folder no. => open file/folder")
    print("pwd %s" %dir)
    listing=os.listdir(dir)
    print("[0]-Back")
    for i,d in enumerate(listing):
        print("[%s]-%s" %(i+1,d))
    user_input=input(":")
    if user_input=='x':
        exit(0)
    else:
        user_input=int(user_input)-1
        if user_input >=0:
            # dir input
            dir=dir+"/"+listing[user_input]
            # check if it's a dir
            if(os.path.isdir(dir)):
                findFile(dir)
            else:
                # was a file call open function
                print(dir)
                return dir
                # print("oppe")    
        else:
            # step back
            dir=dir.split("/")
            dir.pop()
            dir="/".join(str(e) for e in dir)
            findFile(dir)
            # print(dir)


def writeToTemp(content,name="test",tempdir=None,extension=".config",MaxDays=5):
    # clean OLD CONFIGS
    tempdir=tempdir if tempdir else '/store/temp/configs/'
    tempdir=DIR+tempdir
    existing =os.listdir(tempdir)
    for rmFile in existing:
        timeDiff=(datetime.today()-datetime.fromtimestamp(checkDateCreated(tempdir+rmFile))).days
        if timeDiff >= MaxDays:
            os.remove(tempdir+rmFile)
    
    if content:
        newFilePath=tempdir+name+extension
        file=open(newFilePath,"w+")
        file.write(content)
        file.close()
        print("\n stored at",newFilePath)

if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    # print("get inventory file")
    writeToTemp(DIR)