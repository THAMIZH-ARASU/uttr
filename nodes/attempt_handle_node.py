class AttemptHandleNode:
    def __init__(self, attempt_body, handle_body, error_var_name=None):
        self.attempt_body = attempt_body
        self.handle_body = handle_body
        self.error_var_name = error_var_name
        
        self.pos_start = self.attempt_body.pos_start
        self.pos_end = self.handle_body.pos_end
