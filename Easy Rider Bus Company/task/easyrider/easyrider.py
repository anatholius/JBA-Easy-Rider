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
        self.errors = None
        self.correct_data = []
        self.schedule = {}

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

            bus_id = object_['bus_id']
            del object_['bus_id']
            stop_id = object_['stop_id']
            del object_['stop_id']

            self.schedule[bus_id][stop_id] = object_

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

    def stops(self):
        print(*[
            'Line names and number of stops:',
            *[f'bus_id: {bus_id}, stops: {len(sch.items())}'
              for bus_id, sch in self.schedule.items()]
        ], sep='\n', end='\n\n')


class Scheduler:
    db = []
    data = []

    def validate(self, db):
        spec = Spec()
        self.db = db
        for record in self.db:
            spec.check(record)

        if not spec.is_satisfied():
            spec.report()
        else:
            spec.stops()


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

else:
    entry = json.loads(input())
    schedule.validate(entry)
