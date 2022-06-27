from entity.schedule import Schedule
from spec import Spec


class Scheduler:
    def __init__(self, data):
        self.lines = {}

        for item in data:
            if Spec().check(item):
                self.add_schedule(item)
            else:
                exit('Something is not valid!')

    def show(self):
        # print('self.lines')
        # print(self.lines)
        # exit('exit')
        has_message = False
        message = []
        for schedule in self.lines.values():
            if schedule.line.trace.message is not None:
                message.append(schedule.line.trace.message)
            # else:
            #     continue
            # array_scheduler.append(schedule.show())
            # continue

            # print(schedule.line.trace.message)
            # print('is True:', schedule.line.trace.message is not None)


        # print('Arrival time test:', message)
        if not message:
            print('\n'.join(message))
        else:
            print('OK')
            [print((v.show(), v.line.trace.message)) for i, v in self.lines.items()]
            array_scheduler = []
            for schedule in self.lines.values():
                # print('schedule', schedule.show())
                array_scheduler.append(schedule.show())
                # print('\n'.join(array_scheduler))

    def add_schedule(self, spec: dict):
        if spec['bus_id'] in self.lines:
            schedule = self.lines[spec['bus_id']]
            schedule.add(spec)
            print(schedule.show())
        else:
            schedule = Schedule(spec)

        if schedule.line.bus_id not in self.lines.keys():
            self.lines[schedule.line.bus_id] = schedule

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


# print('__name__', __name__)
if __name__ == '__main__':
    exit('No direct instantiation!')
