from errors.run_time_error import RTError
from functions.function import Function
from run_time_result import RTResult
from tokens import TT_DIV, TT_EE, TT_GT, TT_GTE, TT_KEYWORD, TT_LT, TT_LTE, TT_MINUS, TT_MOD, TT_MUL, TT_NE, TT_PLUS
from values.dict_value import Dict
from values.error_value import ErrorValue
from values.list_value import List
from values.number_value import Number
from values.string_value import String


class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return(): return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_DictNode(self, node, context):
        res = RTResult()
        elements = {}

        for key_node, value_node in node.key_value_pairs:
            key = res.register(self.visit(key_node, context))
            if res.should_return(): return res
            
            value = res.register(self.visit(value_node, context))
            if res.should_return(): return res
            
            # Convert key to hashable type
            if hasattr(key, 'value'):
                hashable_key = key.value
            else:
                return res.failure(RTError(
                    key_node.pos_start, key_node.pos_end,
                    'Dictionary key must be a string or number',
                    context
                ))
            
            elements[hashable_key] = value

        return res.success(
            Dict(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))

        # For mutable types (List, Dict), don't copy to allow in-place modifications
        # For immutable types (Number, String), copy to prevent issues
        if isinstance(value, (List, Dict)):
            value = value.set_pos(node.pos_start, node.pos_end).set_context(context)
        else:
            value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_ConstAssignNode(self, node, context):
        res = RTResult()
        const_name = node.const_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res

        context.symbol_table.set(const_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.should_return(): return res
        right = res.register(self.visit(node.right_node, context))
        if res.should_return(): return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_MOD:
            result, error = left.modded_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, 'and'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'or'):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.should_return(): return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(TT_KEYWORD, 'not'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        res = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return(): return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return(): return res
                return res.success(Number.null if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            expr_value = res.register(self.visit(expr, context))
            if res.should_return(): return res
            return res.success(Number.null if should_return_null else expr_value)

        return res.success(Number.null)

    def visit_ForNode(self, node, context):
        res = RTResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.should_return(): return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return(): return res

        # Handle optional step value
        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.should_return(): return res
            step = step_value.value
        else:
            step = 1

        i = start_value.value

        while i < end_value.value:
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step

            value = res.register(self.visit(node.body_node, context))
            if res.error: return res
            if res.loop_should_cut: break
            if res.loop_should_skip: continue
            if res.func_return_value: return res

            elements.append(value)

        return res.success(Number.null)

    def visit_ForEachNode(self, node, context):
        res = RTResult()
        elements = []

        iterable = res.register(self.visit(node.iterable_node, context))
        if res.should_return(): return res

        if not isinstance(iterable, List):
            return res.failure(RTError(
                node.iterable_node.pos_start, node.iterable_node.pos_end,
                "Can only iterate through lists",
                context
            ))

        for element in iterable.elements:
            context.symbol_table.set(node.var_name_tok.value, element)

            value = res.register(self.visit(node.body_node, context))
            if res.error: return res
            if res.loop_should_cut: break
            if res.loop_should_skip: continue
            if res.func_return_value: return res

            elements.append(value)

        return res.success(Number.null)

    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return(): return res

            if not condition.is_true():
                break

            value = res.register(self.visit(node.body_node, context))
            if res.error: return res
            if res.loop_should_cut: break
            if res.loop_should_skip: continue
            if res.func_return_value: return res

            elements.append(value)

        return res.success(Number.null)

    def visit_DoWhileNode(self, node, context):
        res = RTResult()
        elements = []

        while True:
            # Execute body first (this is the key difference from while loop)
            value = res.register(self.visit(node.body_node, context))
            if res.error: return res
            if res.loop_should_cut: break
            if res.func_return_value: return res
            
            # Skip still adds the value before continuing
            if not res.loop_should_skip:
                elements.append(value)

            # Then check condition
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return(): return res

            if not condition.is_true():
                break

        return res.success(Number.null)

    def visit_FuncDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names).set_context(context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return(): return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return(): return res

        return_value = res.register(value_to_call.execute(args))
        if res.should_return(): return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(return_value)

    def visit_ReturnNode(self, node, context):
        res = RTResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return(): return res
        else:
            value = Number.null

        return res.success_return(value)

    def visit_CutNode(self, node, context):
        return RTResult().success_cut()

    def visit_SkipNode(self, node, context):
        return RTResult().success_skip()

    def visit_ListAccessNode(self, node, context):
        res = RTResult()

        collection = res.register(self.visit(node.list_node, context))
        if res.should_return(): return res

        index = res.register(self.visit(node.index_node, context))
        if res.should_return(): return res

        # Handle list access
        if isinstance(collection, List):
            if not isinstance(index, Number):
                return res.failure(RTError(
                    node.index_node.pos_start, node.index_node.pos_end,
                    "List index must be a number",
                    context
                ))

            try:
                element = collection.elements[int(index.value)]
                return res.success(element)
            except:
                return res.failure(RTError(
                    node.index_node.pos_start, node.index_node.pos_end,
                    "Index out of bounds",
                    context
                ))
        
        # Handle dictionary access
        elif isinstance(collection, Dict):
            result, error = collection.dived_by(index)
            if error:
                return res.failure(error)
            return res.success(result)
        
        else:
            return res.failure(RTError(
                node.list_node.pos_start, node.list_node.pos_end,
                "Can only index lists and dictionaries",
                context
            ))

    def visit_AttemptHandleNode(self, node, context):
        res = RTResult()

        # Try to execute the attempt body
        attempt_result = self.visit(node.attempt_body, context)
        
        # If no error occurred, return the result
        if not attempt_result.error:
            return attempt_result
        
        # An error occurred, now execute the handle body
        # Create an ErrorValue to represent the caught error
        caught_error = attempt_result.error
        error_value = ErrorValue(
            caught_error.details,
            caught_error.error_name,
            caught_error
        ).set_context(context).set_pos(node.pos_start, node.pos_end)
        
        # If an error variable name was provided, bind it to the symbol table
        if node.error_var_name:
            context.symbol_table.set(node.error_var_name.value, error_value)
        
        # Execute the handle body
        handle_result = res.register(self.visit(node.handle_body, context))
        if res.should_return(): return res
        
        return res.success(handle_result)