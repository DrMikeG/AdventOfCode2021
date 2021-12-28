import psutil
import os
listOfProcessNames = list()
# Iterate over all running processes
for proc in psutil.process_iter():
   # Get process detail as dictionary
   pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
   # Append dict of process detail in list
   listOfProcessNames.append(pInfoDict)

found = False
for proc in listOfProcessNames:
    if proc['name'].lower() == 'smartscreen.exe':
        pid = proc['pid']
        print("Killing smartscreen process {} pid={}".format(proc,pid))
        os.kill(pid,9)
        found = True

if not found:
    print('smartscreen.exe was not running')
    