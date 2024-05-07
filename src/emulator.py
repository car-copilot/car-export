# STANDARD IMPORTS
from obd import OBDCommand

# LOCAL IMPORTS
from default import *
from influx import write_to_influx

def set_emulator_watchers(connection):   
    print("VEHICLE MODEL : EMULATOR")
    
    emulator_cmds = []
    
    emulator_cmds.append(OBDCommand(
        "FUEL_LEVEL",
        "Level of fuel",
        b'012F',
        3,
        decode_percent_0_100
    ))
    
    emulator_cmds.append(OBDCommand(
        "OIL_TEMP",
        "Engine oil temperature",
        b'015C',
        3,
        decode_temp__40_215
    ))
    
    emulator_cmds.append(OBDCommand(
        "FUEL_RATE",
        "Engine fuel rate",
        b'015E',
        4,
        decode_fuel_rate_0_3212
    ))
    
    emulator_cmds.append(OBDCommand(
        "SHORT_FUEL_TRIM_1",
        "Short Term Fuel Trim - Bank 1",
        b'0106',
        3,
        decode_percent__100_100
    ))
    
    emulator_cmds.append(OBDCommand(
        "LONG_FUEL_TRIM_1",
        "Long Term Fuel Trim - Bank 1",
        b'0107',
        3,
        decode_percent__100_100
    ))
    
    emulator_cmds.append(OBDCommand(
        "SHORT_FUEL_TRIM_2",
        "Short Term Fuel Trim - Bank 2",
        b'0108',
        3,
        decode_percent__100_100
    ))
    
    emulator_cmds.append(OBDCommand(
        "LONG_FUEL_TRIM_2",
        "Long Term Fuel Trim - Bank 2",
        b'0109',
        3,
        decode_percent__100_100
    ))
        
    emulator_cmds.append(OBDCommand(
        "DEMAND_ENGINE",
        "Driver's demand engine - percent torque",
        b'0161',
        3,
        decode_percent__125_130
    ))
    
    emulator_cmds.append(OBDCommand(
        "ACTUAL_ENGINE",
        "Actual engine - percent torque",
        b'0162',
        3,
        decode_percent__125_130
    ))
    
    emulator_cmds.append(OBDCommand(
        "REFERENCE_TORQUE",
        "Engine reference torque",
        b'0163',
        4,
        decode_torque_0_65
    ))        
    
    for i in emulator_cmds:
        connection.watch(i, callback=write_to_influx, force=True) 