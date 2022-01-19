import os
import sys

import rrdtool

from rrd import get_sensors, get_sensor_files, inspect_sensor

COLORS = ['#0b84a5', '#f6c85f', '#6f4e7c', '#9dd866', '#ca472f', '#ffa056', '#8dddd0']

INTERVALS = ['1day', '1week', '1month', '6months']

def rrd_graph(datadir, htmldir, field):
    sensors = []
    for sensor in get_sensors(datadir):
        fields, first_ts = inspect_sensor(datadir, sensor)
        if field in fields:
            sensors.append(sensor)

    defs = ['DEF:%s_%d=%s:%s:AVERAGE' % (field, i, os.path.join(datadir, '%s.rrd' % sensor), field) for i, sensor in enumerate(sensors, 1)]
    lines = ['LINE1:%s_%d%s:%s' % (field, i, COLORS[i - 1], "%s @%s" % (field, sensor)) for i, sensor in enumerate(sensors, 1)]

    generated_files = []

    for interval in INTERVALS:
        filename = '%s_%s.png' % (field, interval)
        rrdtool.graph(os.path.join(htmldir, filename),
                '-w', '800', '-h', '120', '-a', 'PNG', '--slope-mode',
                '--start', '-%s' % interval,
                *(defs + lines))
        generated_files.append(filename)

    with open(os.path.join(htmldir, '%s.html' % field), 'w') as html_file:
        html_file.write("<html><body>\n")
        for filename in generated_files:
            html_file.write("<img src='%s' />\n" % filename)
        html_file.write("</body></html>\n")

if __name__ == '__main__':
    rrd_graph(sys.argv[1], sys.argv[2], 'temp')
