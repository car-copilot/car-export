# STANDARD IMPORT
import obd
from obd import Unit
from obd.utils import bytes_to_int

# LOCAL IMPORT
from influx import write_to_influx

# DEFINE SPECIFIC UNITS
Unit.define("newton_meter = Nm = N.m")
   
# DEFAULT DECODERS
def decode_percent_0_100(message):
    d = message[0].data[2:]
    v = d[0]
    v = v * 100.0 / 255.0
    return v * Unit.percent

def decode_percent__100_100(message):
    d = message[0].data[2:]
    v = d[0]
    v = (v - 128) * 100.0 / 128.0
    return v * Unit.percent  

def decode_temp__40_215(message):
    d = message[0].data[2:]
    v = bytes_to_int(d)
    v = v - 40
    return Unit.Quantity(v, Unit.celsius)

def decode_fuel_rate_0_3212(message):
    d = message[0].data[2:]
    v = bytes_to_int(d)
    v = v * 0.05
    return v * Unit.liters_per_hour    

def decode_percent__125_130(message):
    d = message[0].data[2:]
    v = d[0]
    v = v - 125
    return v * Unit.percent

def decode_torque_0_65(message):
    d = message[0].data[2:]
    v = bytes_to_int(d)
    return v * Unit.newton_meter
    
# DEFAULT WATCHERS
def set_default_watchers(connection, cfg):
    for name, pid in cfg["PIDs"].items():
        if pid["enabled"]:
            connection.watch(obd.commands[name.upper()], callback=write_to_influx, force=True)