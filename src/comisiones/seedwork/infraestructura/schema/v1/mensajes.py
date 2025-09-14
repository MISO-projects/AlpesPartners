import uuid
from pulsar.schema import *

def time_millis():
    import time
    return int(time.time() * 1000)

class Mensaje(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()