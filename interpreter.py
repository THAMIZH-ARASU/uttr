from errors.run_time_error import RTError
from functions.function import Function
from run_time_result import RTResult
from symbol_table import SymbolTable
from tokens import TT_DIV, TT_EE, TT_GT, TT_GTE, TT_KEYWORD, TT_LT, TT_LTE, TT_MINUS, TT_MOD, TT_MUL, TT_NE, TT_PLUS
from values.dict_value import Dict
from values.error_value import ErrorValue
from values.list_value import List
from values.number_value import Number
from values.regex_value import Regex
from values.string_value import String
from values.tuple_value import Tuple


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

    def visit_RegexNode(self, node, context):
        regex = Regex(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        
        # Check if there was a compilation error
        if regex.compiled is None:
            return RTResult().failure(RTError(
                node.pos_start, node.pos_end,
                f"Invalid regex pattern: {regex.compile_error}",
                context
            ))
        
        return RTResult().success(regex)

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return(): return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_TupleNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return(): return res

        return res.success(
            Tuple(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
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

        # For mutable types (List, Dict) and functions, don't copy to preserve their context/state
        # For immutable types (Number, String), copy to prevent issues
        from functions.base_function import BaseFunction
        from functions.builtin_function import BuiltInFunction
        if isinstance(value, (List, Dict, BaseFunction)):
            value = value.set_pos(node.pos_start, node.pos_end)
            # Builtin functions should use current context
            # User-defined functions should keep their defining context (from module)
            if isinstance(value, BuiltInFunction):
                value = value.set_context(context)
            elif not isinstance(value, BaseFunction):
                value = value.set_context(context)
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

    def visit_SwitchCaseNode(self, node, context):
        res = RTResult()

        # Evaluate the switch expression
        switch_value = res.register(self.visit(node.switch_expr, context))
        if res.should_return(): return res

        # Check each case
        for case_value_node, expr, should_return_null in node.cases:
            case_value = res.register(self.visit(case_value_node, context))
            if res.should_return(): return res

            # Check if values match (using == comparison)
            if switch_value.get_comparison_eq(case_value)[0].is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return(): return res
                return res.success(Number.null if should_return_null else expr_value)

        # If no case matched, execute default if present
        if node.default_case:
            expr, should_return_null = node.default_case
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

        if not isinstance(iterable, (List, Tuple)):
            return res.failure(RTError(
                node.iterable_node.pos_start, node.iterable_node.pos_end,
                "Can only iterate through lists and tuples",
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

    def visit_LambdaNode(self, node, context):
        res = RTResult()

        # Lambda functions are anonymous (no name)
        func_name = "<lambda>"
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names).set_context(context).set_pos(node.pos_start, node.pos_end)

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

    def visit_ImportNode(self, node, context):
        """Handle import statements."""
        res = RTResult()
        from module_loader import module_loader
        from errors.module_not_found_error import ModuleNotFoundError
        from errors.circular_import_error import CircularImportError
        from module import Module
        from lexer import Lexer
        from parser import Parser
        from context import Context
        
        module_name = node.module_name_tok.value
        
        # Get the current file path for relative imports
        current_file = context.display_name if hasattr(context, 'display_name') else '<program>'
        if current_file == '<program>':
            current_file = None
        
        # Find the module file
        module_path, error_info = module_loader.find_module(module_name, current_file)
        
        if module_path is None:
            return res.failure(ModuleNotFoundError(
                node.pos_start, node.pos_end,
                error_info['message'],
                error_info['searched_paths']
            ))
        
        # Check if module is already cached
        if module_loader.is_cached(module_path):
            module_obj = module_loader.get_cached_module(module_path)
        else:
            # Check for circular imports
            if module_loader.is_loading(module_path):
                chain = module_loader.get_loading_chain() + [module_path]
                return res.failure(CircularImportError(
                    node.pos_start, node.pos_end,
                    f"Circular import detected involving '{module_name}'",
                    chain
                ))
            
            # Load module source
            source, error_msg = module_loader.load_module_source(module_path)
            if source is None:
                return res.failure(RTError(
                    node.pos_start, node.pos_end,
                    error_msg,
                    context
                ))
            
            # Mark module as loading
            module_loader.begin_loading(module_path)
            
            try:
                # Tokenize module source
                lexer = Lexer(module_path, source)
                tokens, error = lexer.make_tokens()
                if error:
                    module_loader.end_loading(module_path)
                    return res.failure(RTError(
                        node.pos_start, node.pos_end,
                        f"Error in module '{module_name}': {error.as_string()}",
                        context
                    ))
                
                # Parse module
                parser = Parser(tokens)
                ast = parser.parse()
                if ast.error:
                    module_loader.end_loading(module_path)
                    return res.failure(RTError(
                        node.pos_start, node.pos_end,
                        f"Error in module '{module_name}': {ast.error.as_string()}",
                        context
                    ))
                
                # Create module context with its own symbol table
                # Inherit global symbols but isolate module-specific definitions
                from entry import global_symbol_table
                module_context = Context(f'<module:{module_name}>')
                module_context.symbol_table = SymbolTable(global_symbol_table)
                module_context.display_name = module_path
                
                # Execute module
                module_result = self.visit(ast.node, module_context)
                module_loader.end_loading(module_path)
                
                if module_result.error:
                    return res.failure(RTError(
                        node.pos_start, node.pos_end,
                        f"Error executing module '{module_name}': {module_result.error.as_string()}",
                        context
                    ))
                
                # Check if module has explicit exports
                exports = None
                if hasattr(module_context, '_exports'):
                    exports = module_context._exports
                
                # Create module object
                module_obj = Module(module_name, module_path, module_context.symbol_table, exports, source)
                
                # Cache the module
                module_loader.cache_module(module_path, module_obj)
            
            except Exception as e:
                module_loader.end_loading(module_path)
                return res.failure(RTError(
                    node.pos_start, node.pos_end,
                    f"Unexpected error loading module '{module_name}': {str(e)}",
                    context
                ))
        
        # Import symbols into current context
        if node.items is None:
            # Import all exported symbols
            exported = module_obj.get_exported_symbols()
            for name, value in exported.items():
                context.symbol_table.set(name, value)
        else:
            # Import specific items
            exported = module_obj.get_exported_symbols()
            for item_name_tok, alias_tok in node.items:
                item_name = item_name_tok.value
                
                if item_name not in exported:
                    return res.failure(RTError(
                        item_name_tok.pos_start, item_name_tok.pos_end,
                        f"Module '{module_name}' does not export '{item_name}'",
                        context
                    ))
                
                # Use alias if provided, otherwise use original name
                import_name = alias_tok.value if alias_tok else item_name
                context.symbol_table.set(import_name, exported[item_name])
        
        return res.success(Number.null)

    def visit_ShareNode(self, node, context):
        """Handle share (export) statements."""
        res = RTResult()
        
        # Mark items for export in the module's context
        # This is tracked at the module level, not during normal execution
        # For now, we'll store export information in a special variable
        if not hasattr(context, '_exports'):
            context._exports = set()
        
        for item_tok in node.item_name_toks:
            item_name = item_tok.value
            
            # Verify the item exists in the symbol table
            value = context.symbol_table.get(item_name)
            if value is None:
                return res.failure(RTError(
                    item_tok.pos_start, item_tok.pos_end,
                    f"Cannot share undefined symbol '{item_name}'",
                    context
                ))
            
            context._exports.add(item_name)
        
        return res.success(Number.null)