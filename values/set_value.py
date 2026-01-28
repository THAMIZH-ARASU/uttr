from errors.run_time_error import RTError
from values.number_value import Number
from values.string_value import String
from values.value import Value


class Set(Value):
    def __init__(self, elements):
        super().__init__()
        # Convert elements to hashable types and store in Python set
        self.elements = set()
        for elem in elements:
            self.elements.add(self._make_hashable(elem))
    
    def _make_hashable(self, elem):
        """Convert value to hashable representation for set storage"""
        if isinstance(elem, Number):
            return ('number', elem.value)
        elif isinstance(elem, String):
            return ('string', elem.value)
        elif isinstance(elem, Set):
            # Sets can't contain mutable sets, convert to frozen representation
            return ('set', frozenset(elem.elements))
        else:
            # For other types, store their string representation
            return ('other', str(elem))
    
    def _from_hashable(self, hashable):
        """Convert hashable representation back to Value object"""
        type_tag, value = hashable
        if type_tag == 'number':
            result = Number(value)
        elif type_tag == 'string':
            result = String(value)
        elif type_tag == 'set':
            # Reconstruct set from frozen representation
            elements = [self._from_hashable(elem) for elem in value]
            result = Set(elements)
        else:
            result = String(value)
        
        result.set_context(self.context)
        return result

    def added_to(self, other):
        """Union operation using + operator"""
        if isinstance(other, Set):
            new_set = Set([])
            new_set.elements = self.elements | other.elements
            new_set.set_pos(self.pos_start, other.pos_end)
            new_set.set_context(self.context)
            return new_set, None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        """Difference operation using - operator"""
        if isinstance(other, Set):
            new_set = Set([])
            new_set.elements = self.elements - other.elements
            new_set.set_pos(self.pos_start, other.pos_end)
            new_set.set_context(self.context)
            return new_set, None
        else:
            return None, Value.illegal_operation(self, other)
    
    def intersected_with(self, other):
        """Intersection operation using & operator"""
        if isinstance(other, Set):
            new_set = Set([])
            new_set.elements = self.elements & other.elements
            new_set.set_pos(self.pos_start, other.pos_end)
            new_set.set_context(self.context)
            return new_set, None
        else:
            return None, Value.illegal_operation(self, other)
    
    def symmetric_diff_with(self, other):
        """Symmetric difference operation using ^ operator"""
        if isinstance(other, Set):
            new_set = Set([])
            new_set.elements = self.elements ^ other.elements
            new_set.set_pos(self.pos_start, other.pos_end)
            new_set.set_context(self.context)
            return new_set, None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        """Check equality - sets are equal if they have the same elements"""
        if isinstance(other, Set):
            result = Number(1 if self.elements == other.elements else 0)
        else:
            result = Number(0)
        result.set_context(self.context)
        return result, None

    def get_comparison_ne(self, other):
        """Check inequality"""
        if isinstance(other, Set):
            result = Number(1 if self.elements != other.elements else 0)
        else:
            result = Number(1)
        result.set_context(self.context)
        return result, None

    def dived_by(self, other):
        """Indexing not supported for sets (they are unordered)"""
        return None, RTError(
            self.pos_start, self.pos_end,
            'Sets are unordered and do not support indexing',
            self.context
        )

    def copy(self):
        new_set = Set([])
        new_set.elements = self.elements.copy()
        new_set.set_pos(self.pos_start, self.pos_end)
        new_set.set_context(self.context)
        return new_set

    def __str__(self):
        if len(self.elements) == 0:
            return "{: :}"
        # Convert back to Value objects for display
        value_objects = [self._from_hashable(elem) for elem in sorted(self.elements, key=str)]
        return "{: " + ", ".join([str(x) for x in value_objects]) + " :}"

    def __repr__(self):
        if len(self.elements) == 0:
            return "{: :}"
        value_objects = [self._from_hashable(elem) for elem in sorted(self.elements, key=str)]
        return "{: " + ", ".join([repr(x) for x in value_objects]) + " :}"
