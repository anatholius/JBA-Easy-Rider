import argparse
import json
from scheduler import Scheduler


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
                if not schedule.validate(e):
                    print(schedule.spec)

else:
    entry = json.loads(input())
    schedule.validate(entry)
