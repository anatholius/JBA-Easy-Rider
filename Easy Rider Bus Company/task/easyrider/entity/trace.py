from .stop import Stop


class Trace:

    def __init__(self):
        self._index = 0
        # self.message = None
        self.messages = []
        self.stops: list[Stop] | list = []

    def __next__(self):
        if self._index < len(self.stops):
            result = self.stops[self._index]
            self._index += 1
            return result

        raise StopIteration

    def __str__(self):
        if self.message:
            return self.message
        # return 'Trace:'

    def add_stop(self, stop: Stop, line_id, time):
        if stop not in self.stops:
            line = stop.lines[line_id]

            # prev_time = self.stops[line][-1]
            # is_time_correct = prev_time < time
            if not line or line[-1] < time:
                # line_hours = stop.lines[line_id]
                line.append(time)
                self.stops.append(stop)
            # else:
            #     message = 'bus_id line {}: wrong time on station {}'.format(
            #         time,
            #         stop.stop_name
            #     )
            #     self.messages.append(message)

            # prev_time = self.stops[line][-1]
            #
            # stop_time = list(stop.lines.items())[-1]
            # if len(self.stops) > 1:
            #     last_time = list(self.stops[-1].lines.items())[-1]
            #     last_ = last_time[1][-1]
            #     stop_ = stop_time[1][-1]
            #     is_correct = last_ < stop_
            #
            #     # if last_time[1][-1] > stop_time[1][-1] and not
            #     self.message:
            #     if last_time[1][-1] >= stop_time[1][-1]:
            #         message = f'bus_id line {stop_time[0]}: wrong time on ' \
            #                   f'station {stop.stop_name}'
            #         self.message = message
            #         # return message
            #         # self.stops.append(message)
            # else:
            #     self.stops.append(stop)

    def is_valid_time(self, stop):
        if len(self.stops):
            last_time = list(self.stops[-1].lines.values())[-1][-1]
            stop_time = list(stop.lines.values())[-1][-1]
            return last_time < stop_time
