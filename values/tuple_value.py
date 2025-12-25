from errors.run_time_error import RTError
from values.number_value import Number
from values.value import Value


class Tuple(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = tuple(elements)  # Ensure immutability

    def added_to(self, other):
        # Tuples are immutable, cannot append
        return None, RTError(
            other.pos_start, other.pos_end,
            'Tuples are immutable and cannot be modified',
            self.context
        )

    def subbed_by(self, other):
        # Tuples are immutable, cannot remove elements
        return None, RTError(
            other.pos_start, other.pos_end,
            'Tuples are immutable and cannot be modified',
            self.context
        )

    def multed_by(self, other):
        # Tuple concatenation creates a new tuple
        if isinstance(other, Tuple):
            new_tuple = Tuple(list(self.elements) + list(other.elements))
            new_tuple.set_pos(self.pos_start, self.pos_end)
            new_tuple.set_context(self.context)
            return new_tuple, None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        # Access by index
        if isinstance(other, Number):
            try:
                element = self.elements[int(other.value)]
                return element, None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Element at this index could not be retrieved from tuple because index is out of bounds',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = Tuple(list(self.elements))
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return ", ".join([str(x) for x in self.elements])

    def __repr__(self):
        return f'<{", ".join([repr(x) for x in self.elements])}>'
