import argparse
import json


class Spec:
    requirements = {
        'bus_id': {'type': type(1), 'required': True},
        'stop_id': {'type': type(1), 'required': True},
        'stop_name': {'type': type(''), 'required': True},
        'next_stop': {'type': type(1), 'required': True},
        'stop_type': {'type': type('d'), 'required': False, 'len': 1},
        'a_time': {'type': type(''), 'required': True},
    }

    def __init__(self):
        self.errors = None
        self.correct_data = []

    def fields(self):
        return self.requirements.items()

    def is_satisfied_by(self, name, value) -> int:
        return int(
            type(value) != self.requirements[name]['type']
            or
            self.requirements[name]['required'] and not len(str(value))
            or
            'len' in self.requirements[name] and
            len(str(value)) > self.requirements[name]['len']
        )

    def check(self, object_: dict):
        if self.errors is None:
            self.errors = {p: 0 for p, t in self.fields()}
        for name, value in object_.items():
            error = self.is_satisfied_by(name, value)
            self.errors[name] += error
            if not bool(error):
                self.correct_data.append(object_)

    def is_satisfied(self):
        return not self.errors or not len(self.errors)

    def report(self):
        count = sum(self.errors.values())
        print(*[
            f'Type and required field validation: {count} errors',
            *[f'{p}: {e}' for p, e in self.errors.items()]
        ], sep='\n', end='\n\n')

    def get_correct(self):
        return self.correct_data


class Scheduler:
    db = []
    data = []

    def validate(self, db):
        spec = Spec()
        self.db = db
        for record in self.db:
            spec.check(record)

        # if not self.spec.is_satisfied():
        spec.report()

        # get only correct data
        # self.data = self.spec.get_correct()


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
