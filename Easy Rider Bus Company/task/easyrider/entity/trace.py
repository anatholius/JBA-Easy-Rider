import sys

from .stop import Stop


class Trace:

    def __init__(self):
        self._index = 0
        self.message = None
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
            # exit()
        return 'Trace:'

    def add_stop(self, stop, line=None):
        print()
        print()
        print(f'Adding stop(line: {line})', stop, self.stops)
        if stop not in self.stops:
            stop_time = list(stop.lines.items())[-1]
            if len(self.stops) > 1:
                print()
                print('self.stops')
                # print(self.stops)
                [print(s) for s in self.stops]
                print()
                print()
                last_time = list(self.stops[-1].lines.items())[-1]
                # print(self.stops[-1].stop_name, ' :: ', stop.stop_name)
                # print(last_time[0], ' :: ', stop_time[0])
                # print(last_time[1][-1], ' > ', stop_time[1][-1], last_time[1][-1] > stop_time[1][-1])

                # if last_time[1][-1] > stop_time[1][-1] and not self.message:
                if last_time[1][-1] > stop_time[1][-1]:
                    message = f'Time for line("{stop_time[0]}") between ("' \
                              f'{self.stops[-1].stop_name}" -> "' \
                              f'{stop.stop_name}"): '
                    print(message, last_time[1][-1] > stop_time[1][-1], file=sys.stderr)
                    message = f'bus_id line {stop_time[0]}: wrong time on ' \
                              f'station {stop.stop_name}'
                    self.message = message
                    # return message
                    # self.stops.append(message)
            else:
                self.stops.append(stop)

    def is_valid_time(self, stop):
        if len(self.stops):
            last_time = list(self.stops[-1].lines.values())[-1][-1]
            stop_time = list(stop.lines.values())[-1][-1]
            return last_time < stop_time
