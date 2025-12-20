from functions.base_function import BaseFunction
from run_time_result import RTResult
from values.number_value import Number


class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names

    def execute(self, args):
        res = RTResult()
        # Import here to avoid circular dependency
        from interpreter import Interpreter
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.should_return(): return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value is None: return res

        ret_value = res.func_return_value or value or Number.null
        return res.success(ret_value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"