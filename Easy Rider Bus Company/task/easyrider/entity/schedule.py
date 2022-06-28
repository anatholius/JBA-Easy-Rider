
from .line import Line
from .stop import Stop
from .trace import Trace


class Schedule:
    """
    Schedule for given line
    """

    line = None
    # bus_id = None
    trace = None

    # stops: list[Stop] | list = []

    def __init__(self, spec):
        if not self.line:
            # self.line = Line(spec)
            self.line = spec['bus_id']
        time = spec['a_time']
        stop = Stop(spec)
        # self.line.trace.add_stop(stop)
        if not self.trace:
            self.trace = Trace()

        self.trace.add_stop(stop, self.line, time)

    def show(self, stop_id: str | None = None):
        if stop_id is None:
            # print(self.line.show())
            return f'{self.line.show()}'
        else:
            return [stop for stop in self.line.trace.stops][0]

    def add(self, spec):
        if self.line is None:
            self.line: Line = Line(spec)

        self.trace.add_stop(Stop(spec, self.line))
        self.line.trace.add_stop(Stop(spec, self.line))
