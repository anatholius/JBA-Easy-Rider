class Stop:
    _wrong_type = False
    transfer = False
    on_demand = False

    def __init__(self, spec):
        self.stop_id = spec['stop_id']
        self.stop_name = spec['stop_name']
        if spec['stop_type'] == 'O':
            self.on_demand = True

        self.lines = {}
        if spec['bus_id'] not in self.lines.keys():
            self.lines[spec['bus_id']] = []

    def __str__(self, line_id: int = None):
        if line_id is not None:
            return 'Printing stop for line:', line_id
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

    def add_line(self, spec):
        self.lines[spec['bus_id']] = []
        if len(self.lines.keys()) > 1:
            self.transfer = True
        if self.transfer and self.on_demand:
            self._wrong_type = True
        if spec['stop_type'] in 'SF' and self.on_demand:
            self._wrong_type = True

    def has_wrong_type(self):
        return self._wrong_type
