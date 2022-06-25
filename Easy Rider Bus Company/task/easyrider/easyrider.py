import argparse
import json
import re


class Spec:
    """
    Run program with `-t` or `--test` parameter to test with
    `test_data.json` test sets
    """

    requirements = {
        'bus_id': {'type': type(1), 'required': True},
        'stop_id': {'type': type(1), 'required': True},
        'stop_name': {
            'type': type(''),
            'required': True,
            'match': lambda v: not re.match(
                r'[A-Z]([\w\s]+)(Road|Avenue|Boulevard|Street)$', v)
        },
        'next_stop': {'type': type(1), 'required': True},
        'stop_type': {
            'type': type('d'),
            'match': lambda v: bool(
                # if not in 'SOF' or not empty -> increment errors
                re.match('([^SOF])|(^"")', v)
                or
                # not len=1 + required=False (len=0) -> increment errors
                len(re.findall('([SOF])', str(v))) > 1
            )
        },
        'a_time': {
            'type': type(''),
            'required': True,
            'match': lambda v: not re.match(r'([0-1]\d|2[0-3]):([0-5]\d)$', v),
        },
    }

    def __init__(self):
        self.rtf = {
            "start": [],
            "transfer": {},
            "end": [],
        }
        self.errors = None
        self.correct_data = []
        self.schedule = {}
        self.stops = {}
        self.lines = {}

    def __str__(self):
        strings = [f'--- test ---']

        messages = [line['message']
                    for line_id, line in self.lines.items()
                    if 'message' in line]

        if len(messages):
            strings.append(messages[0])
        else:
            # stops
            strings.append('STOPS:')
            for stop_id, stops in self.stops.items():
                strings.append(f'{stop_id}: {stops}')
            strings.append('\n\n')

            # lines
            strings.append('LINES:')
            for line_id, line in self.lines.items():
                strings.append(f'{line_id}:')
                if 'message' in line:
                    strings.append(f'  message: {line["message"]}')
                strings.append(f'  stops:')
                for s in line["stops"]:
                    strings.append(f'        {s["stop_id"]}: {s}')

        strings.append('\n\n')
        return '\n'.join(strings)

    def fields(self):
        return self.requirements.items()

    @staticmethod
    def is_important(name):
        return name in ('stop_name', 'stop_type', 'a_time')

    def is_satisfied_by(self, name, value) -> int:
        return int(bool(
            # check spec `type`
            type(value) != self.requirements[name]['type']
            or
            # check spec `required`
            'required' in self.requirements[name] and
            self.requirements[name]['required'] and not len(str(value))
            or
            # check value `match` spec format
            'match' in self.requirements[name] and
            self.requirements[name]['match'](str(value))
        ))

    def check(self, object_: dict):
        if self.errors is None:
            self.errors = {p: 0 for p, t in self.fields()}

        valid_schedule = True
        for name, value in object_.items():
            error = self.is_satisfied_by(name, value)
            self.errors[name] += error
            if bool(error):
                valid_schedule = False

        # if object_ is valid schedule
        if valid_schedule:
            if object_['bus_id'] not in self.schedule:
                self.schedule[object_['bus_id']] = {}
            if object_['bus_id'] not in self.lines:
                self.lines[object_['bus_id']] = {
                    'spec': object_,
                    'stops': [],
                }

            bus_id = object_['bus_id']
            stop_id = object_['stop_id']
            self.lines[object_['bus_id']]['stops'].append(object_)

            self.schedule[bus_id][stop_id] = object_

            if object_['stop_type'] == 'S':
                self.rtf['start'].append(object_)
            elif object_['stop_type'] == 'F':
                self.rtf['end'].append(object_)

            if stop_id not in self.stops:
                self.stops[stop_id] = {
                    "name": object_['stop_name'],
                    "lines": {}
                }
            if stop_id in self.stops:
                self.stops[stop_id]['lines'][bus_id] = list(
                    self.schedule[bus_id].keys())

    def is_satisfied(self):
        return not self.errors or self.errors and sum(
            self.errors.values()) == 0

    def report(self):
        count = sum(self.errors.values())
        print(*[
            f'Format validation: {count} errors',
            *[f'{p}: {errors}'
              for p, errors in self.errors.items()
              if self.is_important(p)]
        ], sep='\n', end='\n\n')

    def stops_report(self):
        print(*[
            'Line names and number of stops:',
            *[f'bus_id: {bus_id}, stops: {len(sch.items())}'
              for bus_id, sch in self.schedule.items()]
        ], sep='\n', end='\n\n')

    def lines_report(self):
        messages = [line['message']
                    for line_id, line in self.lines.items()
                    if 'message' in line]

        if len(messages):
            print(messages[0])
            exit()
        else:
            unique_ends = {e['stop_id']: e for e in self.rtf['end']}
            print(*[
                'Start stops: {} {}'.format(
                    len(self.rtf['start']),
                    sorted([s['stop_name'] for s in self.rtf['start']])
                ),
                'Transfer stops: {} {}'.format(
                    len(self.rtf['transfer']),
                    sorted([self.stops[stop_id]['name']
                            for stop_id in
                            self.rtf['transfer']])
                ),
                'Finish stops: {} {}'.format(
                    len(unique_ends.values()),
                    sorted([s['stop_name'] for s in unique_ends.values()])
                )
            ], sep='\n', end='\n\n')


class Scheduler:
    db = []
    data = []
    spec = None

    def validate(self, db):
        self.spec = Spec()
        self.db = db

        start_points = 0
        end_points = 0

        for record in self.db:
            if record['stop_type'] == 'S':
                start_points += 1
            if record['stop_type'] == 'F':
                end_points += 1
            self.spec.check(record)

        # Make sure each bus line has exactly one starting point (S) and one
        for line_id, line in self.spec.lines.items():
            start = False
            end = False
            for s in line["stops"]:
                if not start and s['stop_type'] == 'S':
                    start = True
                elif not end and s['stop_type'] == 'F':
                    end = True
                elif s['stop_type'] == 'S':
                    print(s['stop_type'])
                    print((start, end))
                    exit('So now start what?')
                elif s['stop_type'] == 'F':
                    print(s['stop_type'])
                    print((start, end))
                    exit('So now end what?')

            if not start or not end:
                m = f'There is no start or end stop for the line: {line_id}.'
                print(m)
                line['message'] = m
                return False

        for stop_id, stop_spec in self.spec.stops.items():
            if len(stop_spec['lines']) > 1:
                for line_id in stop_spec['lines']:
                    # print()
                    if self.spec.stops[stop_id]['name'] \
                            not in self.spec.rtf['transfer']:
                        self.spec.rtf['transfer'][stop_id] = self.spec.stops[
                            stop_id]

        show_stops = False
        if self.spec.is_satisfied():
            if show_stops:
                self.spec.stops_report()
            else:
                self.spec.lines_report()
        else:
            self.spec.report()


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', action='store_true')

schedule = Scheduler()

if parser.parse_args().test:
    with open('test_data.json') as test:
        entry = json.loads(test.read())
        if isinstance(entry[0], dict):
            exit('stop')
            schedule.validate(entry)
        else:
            for e in entry:
                schedule.validate(e)
                # if not schedule.validate(e):
                #     print(schedule.spec)
                #     pass

else:
    entry = json.loads(input())
    schedule.validate(entry)
