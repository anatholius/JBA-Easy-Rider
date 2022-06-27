# line.py
from .trace import Trace


class Line:
    trace: Trace = None

    def __init__(self, spec):
        self.bus_id = spec['bus_id']
        if not self.trace:
            self.trace = Trace()

    def show(self, stop_id: str | int = None):
        if stop_id is not None:
            return f'Print line for stop({stop_id})'

        if self.trace.message:
            return self.trace.message

        string = 'Line "{bus_id}":\n{stops}'.format(
            bus_id=self.bus_id,
            stops='\n'.join(
                ["   - [{stop_id}] \"{stop_name}\": {hours}".format(
                    stop_id=stop.stop_id,
                    stop_name=stop.stop_name,
                    hours=f''.join([
                        f'{", ".join(hours)}'
                        for line, hours in stop.lines.items()
                    ])
                ) for stop in self.trace.stops])
        )

        return string

    # def add_stop(self, stop: Stop):
    #     self.stops.append(stop)

# print('__name__', __name__)
