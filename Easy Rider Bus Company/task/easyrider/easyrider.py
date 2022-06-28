"""
Run program with `-t` or `--test` parameter to use predefined `test_data.json`
for testing locally
"""

import argparse
import json
import sys

from entity.schedule import Schedule
from entity.stop import Stop
from spec import Spec
from stage import Stage


class Scheduler:
    lines = {}
    stops = {}

    def stage(self, no: int):
        stage = Stage(no)
        stage.lines = self.lines
        stage.stops = self.stops
        return stage

    def init(self, data: [dict]):
        self.lines = {}
        self.stops = {}
        for item in data:
            spec = Spec()
            if spec.check(item):
                self.add_place(item)
            else:
                # incorrect data for schedule
                def errors(field):
                    if spec.errors[field] > 0:
                        suffix = 'Errors: ' if (
                                field in spec.error_messages.keys() and
                                len(spec.error_messages[field]) > 1
                        ) else 'Error: '

                        return ' -> {suffix}{messages}'.format(
                            suffix=suffix,
                            messages=", ".join(spec.error_messages[field])
                        )
                    else:
                        return ''

                if parser.parse_args().test:
                    print('\n'.join([
                        'Incorrect place specification:',
                        '{',
                        '\n'.join([
                            f'   {field}: {value}{errors(field)}' for
                            field, value in item.items()
                        ]),
                        '}'
                    ]), file=sys.stderr)

        return self

    def add_place(self, spec: dict):
        line_id = spec['bus_id']
        current_stop_time = spec['a_time']
        if line_id in self.lines:
            schedule = self.lines[line_id]

            if spec['stop_id'] not in self.stops.keys():
                stop = Stop(spec)
                self.stops[stop.stop_id] = stop
            else:
                stop: Stop = self.stops[spec['stop_id']]
                stop.add_line(spec)
            prev_stop_time = schedule.trace.stops[-1].lines[line_id][-1]
            # check time departure <-> arrive between stops
            if prev_stop_time >= current_stop_time:
                message = 'bus_id line {}: wrong time on station {}'.format(
                    line_id,
                    stop.stop_name
                )
                schedule.trace.messages.append(message)
            schedule.trace.add_stop(stop, line_id, current_stop_time)
        else:
            schedule = Schedule(spec)
            if spec['stop_id'] not in self.stops.keys():
                stop = Stop(spec)
                self.stops[stop.stop_id] = stop
            else:
                stop: Stop = self.stops[spec['stop_id']]
                stop.add_line(spec)

        if schedule.line not in self.lines.keys():
            self.lines[line_id] = schedule

    def validate(self):
        if parser.parse_args().test:
            with open('test_data.json') as test:
                tests = json.loads(test.read())

                for data in tests:
                    self.init(data)
                    self.stage(6).report()
        else:
            entry = json.loads(input())
            self.init(entry)
            self.stage(6).report()


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', action='store_true')

scheduler = Scheduler()
scheduler.validate()
