import os

if os.name == "nt":
    os.system("python -m pip install -r requirements.txt") #If you have installed python via Microsoft Store change python to python3
else:
    os.system("python3 -m pip install -r requirements.txt")
