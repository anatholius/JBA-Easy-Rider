class Stop:
    def __init__(self, spec):
        self.stop_id = spec['stop_id']
        self.stop_name = spec['stop_name']

        self.lines = {}
        if spec['bus_id'] not in self.lines.keys():
            self.lines[spec['bus_id']] = []

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
