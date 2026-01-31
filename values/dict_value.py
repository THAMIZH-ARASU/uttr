from errors.run_time_error import RTError
from values.number_value import Number
from values.string_value import String
from values.value import Value


class Dict(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements  # Python dict storing key-value pairs

    def added_to(self, other):
        # Add a key-value pair (expects a list with [key, value])
        if hasattr(other, 'elements') and isinstance(other.elements, list) and len(other.elements) == 2:
            # Create a new dict with copied elements for immutable operation
            new_dict = Dict(self.elements.copy())
            new_dict.set_pos(self.pos_start, self.pos_end)
            new_dict.set_context(self.context)
            
            key = self._get_hashable_key(other.elements[0])
            if key is None:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Dictionary key must be a string or number',
                    self.context
                )
            new_dict.elements[key] = other.elements[1]
            return new_dict, None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        # Remove a key from dictionary (returns new dict)
        key = self._get_hashable_key(other)
        if key is None:
            return None, RTError(
                other.pos_start, other.pos_end,
                'Dictionary key must be a string or number',
                self.context
            )
        
        # Create a new dict with copied elements for immutable operation
        new_dict = Dict(self.elements.copy())
        new_dict.set_pos(self.pos_start, self.pos_end)
        new_dict.set_context(self.context)
        
        if key in new_dict.elements:
            del new_dict.elements[key]
            return new_dict, None
        else:
            return None, RTError(
                other.pos_start, other.pos_end,
                f'Key "{key}" not found in dictionary',
                self.context
            )

    def dived_by(self, other):
        # Access value by key (using @ operator)
        key = self._get_hashable_key(other)
        if key is None:
            return None, RTError(
                other.pos_start, other.pos_end,
                'Dictionary key must be a string or number',
                self.context
            )
        
        if key in self.elements:
            return self.elements[key], None
        else:
            return None, RTError(
                other.pos_start, other.pos_end,
                f'Key "{key}" not found in dictionary',
                self.context
            )

    def _get_hashable_key(self, value):
        """Convert UTTR value to hashable Python key"""
        if isinstance(value, String):
            return value.value
        elif isinstance(value, Number):
            return value.value
        else:
            return None

    def copy(self):
        # Shallow copy that shares the same elements dict
        # This allows in-place modifications like remove() to work
        copy = Dict(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return len(self.elements) > 0

    def __str__(self):
        pairs = [f"{self._format_key(k)}: {v}" for k, v in self.elements.items()]
        return ", ".join(pairs)

    def _format_key(self, key):
        """Format key for display"""
        if isinstance(key, str):
            return f'"{key}"'
        return str(key)

    def __repr__(self):
        pairs = [f"{self._format_key(k)}: {repr(v)}" for k, v in self.elements.items()]
        return f'{{{", ".join(pairs)}}}'
