# STANDARD IMPORT
import influxdb_client, os, yaml
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv    
from obd import OBDResponse, Unit

# GET THE CONFIG FILE
with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)  

# GET CREDENTIALS
load_dotenv()
token  = os.getenv("token")
org    = os.getenv("org")
url    = os.getenv("url")
bucket = os.getenv("bucket")

# DB CONNECTION
def connect_influx() -> InfluxDBClient:
    return influxdb_client.InfluxDBClient(url=url, token=token, org=org)

influx = connect_influx()
write_api = influx.write_api()  

# WRITE RESPONSE TO DB
def write_to_influx(r: OBDResponse):
    print(f"Writing to InfluxDB: {r.command.name} = {r.value.magnitude if (type(r.value) is Unit.Quantity) else r.value} {cfg['PIDs'][r.command.name.lower()]['unit']}")
    point = Point(r.command.name).tag("unit", cfg["PIDs"][r.command.name.lower()]["unit"]).field("value", r.value.magnitude if (type(r.value) is Unit.Quantity) else r.value)
    write_api.write(bucket=bucket, org=org, record=point)
