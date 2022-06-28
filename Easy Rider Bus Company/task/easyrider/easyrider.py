import argparse
import json
# from scheduler import Scheduler
import sys

from entity.schedule import Schedule
from entity.stop import Stop
from spec import Spec


class Scheduler:
    lines = {}

    def init(self, data: [dict]):
        for item in data:
            spec = Spec()
            if spec.check(item):
                self.add_place(item)
            else:
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
        if line_id in self.lines:
            schedule = self.lines[line_id]
            trace = schedule.trace
            stop = Stop(spec)
            stops = trace.stops
            time_0 = stops[-1].lines[line_id][-1]
            time_1 = spec['a_time']
            time_correct = time_0 < time_1
            if not time_correct:
                message = 'bus_id line {}: wrong time on station {}'.format(
                    line_id,
                    stop.stop_name
                )
                trace.messages.append(message)
            trace.add_stop(stop, line_id, time_1)
        else:
            schedule = Schedule(spec)

        if schedule.line not in self.lines.keys():
            self.lines[line_id] = schedule

    def validate(self):
        if parser.parse_args().test:
            with open('test_data.json') as test:
                tests = json.loads(test.read())

                for data in tests:
                    self.init(data)
                    self.show()
        else:
            entry = json.loads(input())
            self.init(entry).show()

    def show(self):
        messages = []
        for schedule in self.lines.values():
            if len(schedule.trace.messages):
                messages.append(schedule.trace.messages[0])

        print('Arrival time test:')
        if messages:
            print('\n'.join(messages))
        else:
            print('OK')


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', action='store_true')

scheduler = Scheduler()
scheduler.validate()
