class Stop:
    def __init__(self, spec, line=None):
        self.stop_id = spec['stop_id']
        self.stop_name = spec['stop_name']
        self.lines = {}
        # if line is not None and line['bus_id'] not in self.lines:
        if line is not None:
            if line.bus_id not in self.lines:
                self.lines[line.bus_id] = []
            self.lines[line.bus_id].append(spec['a_time'])
            line.trace.add_stop(self)

    def __str__(self, line_id: int = None):
        if line_id is not None:
            print('self.lines', self.lines)
            return 'Printing stop, line =', line_id
        else:
            return """   Stop({stop_id}) "{stop_name}":
    {lines}""".format(
                stop_id=self.stop_id,
                stop_name=self.stop_name,
                lines=f'\n'.join([
                    f'{line}: {", ".join(hours)}' for line, hours in
                    self.lines.items()
                ])
            )

    # def hours(self, line_id):
    #     # [print(line.__str__()) for line in self.lines]
    #     print('self.lines', self.lines)
    #     exit(f'What hours are for bus {line_id} on stop {self.stop_id}')

# print('__name__', __name__)
