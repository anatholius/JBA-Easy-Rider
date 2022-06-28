class Stage:
    lines = None
    stops = None

    def __init__(self, no):
        self.no = no

    def report(self):
        if self.no == 5:
            self.report_timing()
        elif self.no == 6:
            self.report_stops()

    def report_timing(self):
        messages = []
        for schedule in self.lines.values():
            if len(schedule.trace.messages):
                messages.append(schedule.trace.messages[0])

        print('Arrival time test:')
        if messages:
            print('\n'.join(messages))
        else:
            print('OK')

    def report_stops(self):
        wrong_types = [
            stop.stop_name
            for stop_id, stop in self.stops.items()
            if stop.has_wrong_type()
        ]
        if len(wrong_types):
            print(''.join([
                'On demand stops test:\n',
                'Wrong stop type: ',
                str(sorted(wrong_types))
            ]))
        else:
            print('\n'.join(['On demand stops test:', 'OK']))
