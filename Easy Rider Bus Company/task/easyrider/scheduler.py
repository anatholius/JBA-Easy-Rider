from spec import Spec


class Scheduler:
    db = []
    data = []
    spec = None

    def validate(self, db):
        self.spec = Spec()
        self.db = db

        start_points = 0
        end_points = 0

        for record in self.db:
            if record['stop_type'] == 'S':
                start_points += 1
            if record['stop_type'] == 'F':
                end_points += 1
            self.spec.check(record)

        self.spec.check_time()

        # Make sure each bus line has exactly one starting point (S) and one
        for line_id, line in self.spec.lines.items():
            start = False
            end = False
            for s in line["stops"]:
                if not start and s['stop_type'] == 'S':
                    start = True
                elif not end and s['stop_type'] == 'F':
                    end = True
                elif s['stop_type'] == 'S':
                    print(s['stop_type'])
                    print((start, end))
                    exit('So now start what?')
                elif s['stop_type'] == 'F':
                    print(s['stop_type'])
                    print((start, end))
                    exit('So now end what?')

            if not start or not end:
                m = f'There is no start or end stop for the line: {line_id}.'
                print(m)
                line['message'] = m
                return False

        for stop_id, stop_spec in self.spec.stops.items():
            if len(stop_spec['lines']) > 1:
                for line_id in stop_spec['lines']:
                    if self.spec.stops[stop_id]['name'] \
                            not in self.spec.rtf['transfer']:
                        self.spec.rtf['transfer'][stop_id] = self.spec.stops[
                            stop_id]

        show_stops = False
        if self.spec.is_satisfied():
            if show_stops:
                self.spec.stops_report()
            else:
                self.spec.lines_report()
        else:
            self.spec.report()


if __name__ == '__MAIN__':
    print(Scheduler())
