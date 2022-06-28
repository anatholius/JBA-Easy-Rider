from .stop import Stop
from .trace import Trace


class Schedule:
    """
    Schedule for given bus line
    """

    line = None
    trace = None

    def __init__(self, spec):
        if not self.line:
            self.line = spec['bus_id']
        time = spec['a_time']
        stop = Stop(spec)
        if not self.trace:
            self.trace = Trace()

        self.trace.add_stop(stop, self.line, time)

    def show(self, stop_id: str | None = None):
        if stop_id is None:
            return ', '.join([f'{stop}' for stop in self.trace.stops])
        else:
            return [stop for stop in self.trace.stops][0]

    def add(self, spec):
        self.trace.add_stop(Stop(spec), spec['bus_id'], spec['a_time'])
