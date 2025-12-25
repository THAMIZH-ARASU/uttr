from values.value import Value


class ErrorValue(Value):
    def __init__(self, error_message, error_type, error_details=None):
        super().__init__()
        self.error_message = error_message
        self.error_type = error_type
        self.error_details = error_details

    def __repr__(self):
        return f'<Error: {self.error_type}: {self.error_message}>'
    
    def copy(self):
        copy = ErrorValue(self.error_message, self.error_type, self.error_details)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
