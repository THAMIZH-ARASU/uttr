import re
from errors.run_time_error import RTError
from values.value import Value
from values.number_value import Number
from values.string_value import String
from values.list_value import List
from values.dict_value import Dict


class Regex(Value):
    def __init__(self, pattern):
        super().__init__()
        self.pattern = pattern
        try:
            self.compiled = re.compile(pattern)
        except re.error as e:
            self.compiled = None
            self.compile_error = str(e)

    def copy(self):
        copy = Regex(self.pattern)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return f'r"{self.pattern}"'

    def __repr__(self):
        return f'r"{self.pattern}"'


class Match(Value):
    """Represents a regex match result"""
    def __init__(self, match_obj):
        super().__init__()
        self.match_obj = match_obj
        
        # Create a dictionary representation
        if match_obj:
            self.data = {
                'matched_text': match_obj.group(0),
                'start_pos': match_obj.start(),
                'end_pos': match_obj.end(),
                'groups': list(match_obj.groups())
            }
        else:
            self.data = None

    def is_true(self):
        return self.match_obj is not None

    def get_comparison_eq(self, other):
        if isinstance(other, Match):
            result = (self.match_obj is not None) == (other.match_obj is not None)
            return Number(int(result)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = Match(self.match_obj)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        if self.match_obj:
            return f'<Match: {self.match_obj.group(0)}>'
        return '<No Match>'

    def __repr__(self):
        return self.__str__()
