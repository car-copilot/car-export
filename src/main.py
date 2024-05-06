# STANDARD IMPORTS
import obd
import yaml
import time
from obd import Async

# LOCAL IMPORTS
from default  import set_default_watchers
from aygo     import set_aygo_watchers
from emulator import set_emulator_watchers

# CONNECT TO OBD PORT
def connect_elm327() -> obd.Async:
    return obd.Async("/dev/pts/3", delay_cmds=1)

connection = connect_elm327()

# GET THE CONFIG FILE
with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

vehicle_profile = cfg["vehicle_profile"]

# GET DATA FROM THE PIDs
def get_from_obd(vehicle_profile):
    match vehicle_profile :
        case 'aygo':
            set_aygo_watchers(connection)
        case 'emulator':
            set_emulator_watchers(connection)
    set_default_watchers(connection, cfg)

# SETUP THE WATCHERS
get_from_obd(vehicle_profile)
    
# HANDLE EXECUTION
connection.start()
time.sleep(1)
connection.stop()