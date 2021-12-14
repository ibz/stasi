import os
import sys

import rrdtool

from rrd import get_sensors, get_sensor_files, inspect_sensor

COLORS = ['#FF0000', '#00FF00', '#0000FF']

def rrd_graph(datadir, htmldir, field):
    sensors = []
    for sensor in get_sensors(datadir):
        fields, first_ts = inspect_sensor(datadir, sensor)
        if field in fields:
            sensors.append(sensor)

    defs = ['DEF:%s_%d=%s:%s:AVERAGE' % (field, i, os.path.join(datadir, '%s.rrd' % sensor), field) for i, sensor in enumerate(sensors, 1)]
    lines = ['LINE%d:%s_%d%s' % (i, field, i, COLORS[i - 1]) for i, sensor in enumerate(sensors, 1)]

    for interval in ['day', 'week', 'month', 'year']:
        rrdtool.graph(os.path.join(htmldir, '%s_%s.png' % (field, interval)),
                '-w', '800', '-h', '120', '-a', 'PNG', '--slope-mode',
                '--start', '-1%s' % interval,
                *(defs + lines))

if __name__ == '__main__':
    rrd_graph(sys.argv[1], sys.argv[2], 'temperature')

