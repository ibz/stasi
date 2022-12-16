#!/usr/bin/python3

from datetime import datetime
import os
import sys

import rrdtool

from rrd import get_sensors, get_sensor_files, inspect_sensor

def get_db_name(datadir, sensor):
    return os.path.join(datadir, '%s.rrd' % sensor)

def create_db(datadir, sensor):
    all_fields, first_ts = inspect_sensor(datadir, sensor)
    data_sources = ['DS:%s:GAUGE:600:U:U' % f for f in all_fields]
    rrdtool.create(get_db_name(datadir, sensor),
        '--start', str(first_ts - 1),
        '--step', '60',
        data_sources,
        'RRA:MAX:0.5:1:525600')

    return all_fields

def get_last_imported(datadir, sensor):
    imported_filename = os.path.join(datadir, sensor, 'IMPORTED')
    if not os.path.isfile(imported_filename):
        return None, None
    with open(imported_filename) as fd:
        all_fields = fd.readline().strip().split(',')
        last_imported = datetime.fromtimestamp(int(fd.readline().strip()))
        return all_fields, last_imported

def import_file(datadir, sensor, filename, all_fields, last_imported):
    with open(os.path.join(datadir, sensor, filename)) as fd:
        fields = fd.readline().strip().split(',')
        assert fields[0] == 'ts'
        line = fd.readline()
        while line:
            line_data = line.strip().split(',')
            while line_data[0].startswith('\x00'): # deal with broken data
                line_data[0] = line_data[0][1:]
            try:
                date = datetime.fromtimestamp(int(line_data[0]))
            except ValueError:
                date = None
            if date and (last_imported is None or date > last_imported):
                data = [line_data[fields.index(f)] if f in fields else 'U' for f in all_fields]
                rrdtool.update(get_db_name(datadir, sensor), '%d:%s' % (int(line_data[0]), ':'.join(data)))
                with open(os.path.join(datadir, sensor, 'IMPORTED'), 'w') as lifd:
                    lifd.write('%s\n' % ','.join(all_fields))
                    lifd.write('%d\n' % date.timestamp())
                last_imported = date
            line = fd.readline()
    return last_imported

def rrd_import(datadir):
    for sensor in get_sensors(datadir):
        all_fields, last_imported = get_last_imported(datadir, sensor)
        print(f"Importing {sensor} (last imported at {last_imported})...")
        if not last_imported:
            all_fields = create_db(datadir, sensor)
        for filename in get_sensor_files(datadir, sensor):
            filedate = datetime.strptime(filename[:-4], '%Y-%m-%d').date()
            if last_imported is None or (filedate >= last_imported.date()):
                last_imported = import_file(datadir, sensor, filename, all_fields, last_imported)

if __name__ == '__main__':
    rrd_import(sys.argv[1])
