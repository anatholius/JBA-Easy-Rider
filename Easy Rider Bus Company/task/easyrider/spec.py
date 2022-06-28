import re


class Spec:
    """
    Specification pattern based class 🚀.

    Here are predefined requirements, which are checked for given value.
    """

    requirements = {
        'bus_id': {'type': type(1), 'required': True},
        'stop_id': {'type': type(1), 'required': True},
        'stop_name': {
            'type': type(''),
            'required': True,
            'match': lambda v: not re.match(
                r'[A-Z]([\w\s]+)(Road|Avenue|Boulevard|Street)$', v)
        },
        'next_stop': {'type': type(1), 'required': True},
        'stop_type': {
            'type': type('d'),
            'match': lambda v: bool(
                # if not in 'SOF' or not empty -> increment errors
                re.match('([^SOF])|(^"")', v)
                or
                # not len=1 + required=False (len=0) -> increment errors
                len(re.findall('([SOF])', str(v))) > 1
            )
        },
        'a_time': {
            'type': type(''),
            'required': True,
            'match': lambda v: not re.match(r'([0-1]\d|2[0-3]):([0-5]\d)$', v),
        },
    }
    report_support = False

    def __init__(self):
        self.error_messages = {}
        self.errors = None

    def fields(self):
        return self.requirements.items()

    def is_satisfied_by(self, name, value) -> bool:
        """
        Pattern: Specification.

        Checks basic propriety conditions:
         - type,
         - correct value if required
         - match regex conditions specified in requirements for field format

        When spec is not satisfied by given value, function increases field
        errors count.
        Local tests prints detail data with error messages pointed to failed
        fields
        """

        # check spec `type`
        incorrect_type = type(value) != self.requirements[name]['type']
        # check spec `required`
        incorrect_required = (
                'required' in self.requirements[name] and
                self.requirements[name]['required'] and not len(str(value))
        )
        # check value `match` spec format
        incorrect_regex = (
                'match' in self.requirements[name] and
                self.requirements[name]['match'](str(value))
        )
        has_errors = bool(
            incorrect_type or incorrect_required or incorrect_regex
        )
        if has_errors:
            self.error_messages[name] = []
            if incorrect_type:
                self.error_messages[name].append(f'Incorrect type')
            if incorrect_required:
                self.error_messages[name].append(f'Missing required value')
            if incorrect_regex:
                self.error_messages[name].append(f'Incorrect format')

        self.errors[name] += int(has_errors)

        return has_errors

    def check(self, object_: dict) -> bool:
        if self.errors is None:
            self.errors = {p: 0 for p, t in self.fields()}

        valid_schedule = True
        for name, value in object_.items():
            if self.is_satisfied_by(name, value):
                valid_schedule = False

        return valid_schedule

    def is_satisfied(self):
        return (
                not self.errors
                or self.errors
                and sum(self.errors.values()) == 0
        )
