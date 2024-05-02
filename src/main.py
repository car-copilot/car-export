import obd

connection = obd.OBD("/dev/pts/3")

engine_cmd = obd.commands.RPM

response = connection.query(engine_cmd)

print(response.value)