from .stop import Stop


class Trace:

    def __init__(self):
        self._index = 0
        self.messages = []
        self.stops: [Stop] | list = []

    def __next__(self):
        if self._index < len(self.stops):
            result = self.stops[self._index]
            self._index += 1
            return result

        raise StopIteration

    def add_stop(self, stop: Stop, line_id, time):
        if stop not in self.stops:
            line = stop.lines[line_id]

            if not line or line[-1] < time:
                line.append(time)
                self.stops.append(stop)

    def is_valid_time(self, stop):
        if len(self.stops):
            last_stop_time = list(self.stops[-1].lines.values())[-1][-1]
            current_stop_time = list(stop.lines.values())[-1][-1]
            return last_stop_time < current_stop_time
