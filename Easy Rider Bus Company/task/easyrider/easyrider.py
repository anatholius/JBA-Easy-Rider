import argparse
import json

from scheduler import Scheduler

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', action='store_true')

if parser.parse_args().test:
    with open('test_data.json') as test:
        entry = json.loads(test.read())
        tests = [v for v in entry]

        scheduler = None
        for i, test_data in enumerate(tests):
            if i + 1 >= 10:
                scheduler = Scheduler(test_data)
                # print(f'---\nTest: #{i + 1}')
                # print('---\n\n')

        scheduler.show()
else:
    entry = json.loads(input())
    Scheduler(entry).show()
