import subprocess
import os

venv = "netvenv"
dep_file = "depend.txt"
cur_path = os.getcwd()

venv_path = os.path.join(cur_path, venv)
dep_file_path = os.path.join(cur_path, dep_file)

if not os.path.isdir(venv_path):
    print("Creating venv", venv_path)
    subprocess.run(["python3", "-m", "venv", venv_path])
    if subprocess.check_call(["python3", "-m", "venv", venv_path]) != 0:
        print("Could not create venv at", venv_path)
        exit(0)

activate_script = os.path.join(venv_path, "bin", "activate")
subprocess.run(["source", activate_script], shell=True)

if not os.path.isfile(dep_file_path):
    exit(0)
else:
    print("Installing venv dependencies")
    subprocess.run(["pip", "install", "-r", dep_file_path])

    if subprocess.check_call(["pip", "install", "-r", dep_file_path]) != 0:
        print("Could not install dependencies")
        print("Updating python and pip!")
        print("Fix pip error and run script again :)")
        exit(0)
    else:
        print("Done !!")
        exit(0)
