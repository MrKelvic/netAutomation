import subprocess
import os

venv = "netvenv"
dep_file = "depend.txt"
cur_path = os.getcwd()

venv_path = os.path.join(cur_path, venv)
dep_file_path = os.path.join(cur_path, dep_file)

print("Sourcing python from", venv_path)
subprocess.run(["source", os.path.join(venv_path, "bin", "activate")], shell=True)

print("Running test script")
subprocess.run(["python3", "testfn.py])
