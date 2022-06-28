from entity.schedule import Schedule
from entity.stop import Stop
from spec import Spec


class Scheduler:
    def __init__(self, data):
        self.lines = {}

        for item in data:
            if Spec().check(item):
                self.add_place(item)

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

    # def validate(self, data):
    #     self.spec = Spec()
    #     self.data = data
    #
    #     self.spec.check_time()
    #
    #     # Make sure each bus line has exactly one starting point (S) and one
    #     for line_id, line in self.spec.lines.items():
    #         start = False
    #         end = False
    #         for s in line["stops"]:
    #             if not start and s['stop_type'] == 'S':
    #                 start = True
    #             elif not end and s['stop_type'] == 'F':
    #                 end = True
    #             elif s['stop_type'] == 'S':
    #                 print(s['stop_type'])
    #                 print((start, end))
    #                 exit('So now start what?')
    #             elif s['stop_type'] == 'F':
    #                 print(s['stop_type'])
    #                 print((start, end))
    #                 exit('So now end what?')
    #
    #         if not start or not end:
    #             m = f'There is no start or end stop for the line: {line_id}.'
    #             print(m)
    #             line['message'] = m
    #             return False
    #
    #     for stop_id, stop_spec in self.spec.stops.items():
    #         if len(stop_spec['lines']) > 1:
    #             for line_id in stop_spec['lines']:
    #                 if self.spec.stops[stop_id]['name'] \
    #                         not in self.spec.rtf['transfer']:
    #                     self.spec.rtf['transfer'][stop_id] = self.spec.stops[
    #                         stop_id]
    #
    #     show_stops = False
    #     if self.spec.is_satisfied():
    #         if show_stops:
    #             self.spec.stops_report()
    #         else:
    #             self.spec.lines_report()
    #     else:
    #         self.spec.report()


if __name__ == '__main__':
    exit('Unavailable direct execution!')
