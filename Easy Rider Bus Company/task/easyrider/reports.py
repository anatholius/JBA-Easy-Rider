class Reports:
    """
    Deprecated since stage 5/6
    """

    def __init__(self, errors):
        self.errors = errors
        self.correct_data = []
        self.schedule = {}
        self.stops = {}
        self.lines = {}
        self.rtf = {
            "start": [],
            "transfer": {},
            "end": [],
        }

    @staticmethod
    def is_important(name):
        return name in ('stop_name', 'stop_type', 'a_time')

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
                strings.append(f'   {stop_id}: {stops}')
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

    def reports(self, valid_schedule, object_):
        if valid_schedule:
            self.check_time()
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
        else:
            print('Schedule is not valid')
            self.report()
            print('---')
            self.lines_report()
            print('---')
            self.stops_report()

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

    def check_time(self):
        """
        - [x] The string containing the data in JSON format is passed to
        standard input.
        - [x] Check that the arrival time for the upcoming stops for a given
        bus line is increasing.
        - [x] If the arrival time for the next stop is earlier than or equal
        to the time of the current stop, stop checking that bus line and
        remember the name of the incorrect stop.
        - [x] Display the information for those bus lines that have time
        anomalies. For the correct stops, do not display anything.
        - [x] If all the lines are correct timewise, print OK.
        - [x] The output should have the same formatting as shown in the
        example.
        """

        print(self)

        for line_id, line in self.lines.items():
            print(f'Checking line: {line_id}', line)
            for stop in line['stops']:
                print(f'   Checking stop: {stop["stop_id"]}')
                print(f'      stop({stop["stop_name"]}):', stop["a_time"])
                time = stop['a_time']
                next_time = None
                if stop["next_stop"] not in self.stops:
                    print(
                        f'      next_stop: There is no stop "'
                        f'{stop["next_stop"]}"!!!\n\n')
                else:
                    next_stop_id = self.lines[line_id]['spec']["next_stop"]
                    next_stop = self.stops[next_stop_id]
                    print('next_stop', next_stop)
                    exit('Yeah, stop should have structure as well as lines')
                    next_time = next_stop["a_time"]
                    print(f'      next_stop({next_stop["stop_name"]}):',
                          next_time)
                    print('      is later?', time < next_time)

                if next_time:
                    if time < next_time:
                        print('Everything is ok :)', time, next_time)
                    else:
                        print(
                            f'This is not correct departure {next_time} for '
                            f'next stop !')
