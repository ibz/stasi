import os
import re

def get_sensors(datadir):
    return sorted(d for d in os.listdir(datadir) if os.path.isdir(os.path.join(datadir, d)))

def get_sensor_files(datadir, sensor):
    return sorted(f for f in os.listdir(os.path.join(datadir, sensor)) if re.match(r'^\d{4}\-\d{2}\-\d{2}\.csv$', f))

def get_header(datadir, sensor, filename):
    with open(os.path.join(datadir, sensor, filename)) as fd:
        fields = {f for f in fd.readline().strip().split(',')} - {'ts'}
        ts = int(fd.readline().strip().split(',')[0])
        return fields, ts

def inspect_sensor(datadir, sensor):
    all_fields = []
    first_ts = None
    for filename in get_sensor_files(datadir, sensor):
        fields, ts = get_header(datadir, sensor, filename)
        all_fields = sorted(set(all_fields) | fields)
        first_ts = min(first_ts, ts) if first_ts is not None else ts
    return all_fields, first_ts

