import sys

import rrdtool

from rrd import get_sensors, get_sensor_files, inspect_sensor

def rrd_graph(datadir, filename):
    start = None
    for sensor in get_sensors(datadir):
        all_fields, first_ts = inspect_sensor(datadir, sensor)
        start = min(start, first_ts) if start is not None else first_ts

    rrdtool.graph(filename,
            '-w', '785', '-h', '120', '-a', 'PNG', '--slope-mode',
            '--start', str(start),
            '--end', 'now',
            '--vertical-label', "temperature (°C)",
            'DEF:tatami_in_temp=data/stable.rrd:temperature:MAX',
            'LINE1:tatami_in_temp#ff0000:"Tatami IN"')

if __name__ == '__main__':
    rrd_graph(sys.argv[1], sys.argv[2])

