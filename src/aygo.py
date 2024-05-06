# STANDARD IMPORTS
from obd import OBDCommand

# LOCAL IMPORTS
from default import *

def set_aygo_watchers(connection):   
    print("VEHICLE MODEL : AYGO")
    
    aygo_cmds = []
    
    for i in aygo_cmds:
        connection.watch(i, callback=display_values, force=True) 