# STANDARD IMPORTS
import obd
import yaml
import time
import signal
from obd import Async

# LOCAL IMPORTS
from influx   import connect_influx
from default  import set_default_watchers
from aygo     import set_aygo_watchers
from emulator import set_emulator_watchers

# SHUTDOWN OF THE ENDLESS LOOP
class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, signum, frame):
    self.kill_now = True

# CONNECT TO OBD PORT
def connect_elm327() -> obd.Async:
    return obd.Async("/dev/pts/1", delay_cmds=1)

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
killer = GracefulKiller()
connection.start()
while not killer.kill_now:
    time.sleep(1)
print("END OF PROGRAM")
connection.stop()