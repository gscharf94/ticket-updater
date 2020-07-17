import os
from logger import append_to_file, success_file
import time

append_to_file('Checking completion of previous script','CHK')

with open('success','r') as f:
    status = f.read()

if status == "NO":
    append_to_file('WAS NOT COMPLETED. Restarting','CHK')
    os.system('runPython.bat')
else:
    append_to_file('WAS COMPLETED. Going to sleep.. ','CHK')

time.sleep(4)