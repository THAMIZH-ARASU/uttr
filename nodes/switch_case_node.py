class SwitchCaseNode:
    def __init__(self, switch_expr, cases, default_case):
        self.switch_expr = switch_expr
        self.cases = cases  # List of (value_expr, body, should_return_null) tuples
        self.default_case = default_case  # (body, should_return_null) or None
        
        self.pos_start = self.switch_expr.pos_start
        if self.default_case:
            self.pos_end = self.default_case[0].pos_end
        elif len(self.cases) > 0:
            self.pos_end = self.cases[-1][1].pos_end
        else:
            self.pos_end = self.switch_expr.pos_end
