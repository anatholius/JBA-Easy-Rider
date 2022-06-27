from .line import Line
from .stop import Stop


class Schedule:
    """
    Schedule for given line
    """

    line = None

    # stops: list[Stop] | list = []

    def __init__(self, spec):
        if not self.line:
            self.line = Line(spec)
        stop = Stop(spec, self.line)
        self.line.trace.add_stop(stop)

    def show(self, stop_id: str | None = None):
        if stop_id is None:
            # print(self.line.show())
            return f'{self.line.show()}'
        else:
            return [stop for stop in self.line.trace.stops][0]

    def add(self, spec):
        if self.line is None:
            self.line: Line = Line(spec)

        self.line.trace.add_stop(Stop(spec, self.line))
