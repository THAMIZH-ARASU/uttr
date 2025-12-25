from errors.invalid_syntax import InvalidSyntaxError
from nodes.binary_operator_node import BinOpNode
from nodes.call_node import CallNode
from nodes.const_assign_node import ConstAssignNode
from nodes.cut_node import CutNode
from nodes.dict_node import DictNode
from nodes.do_while_node import DoWhileNode
from nodes.for_each_node import ForEachNode
from nodes.for_node import ForNode
from nodes.function_definition_node import FuncDefNode
from nodes.if_node import IfNode
from nodes.list_access_node import ListAccessNode
from nodes.list_node import ListNode
from nodes.number_node import NumberNode
from nodes.return_node import ReturnNode
from nodes.skip_node import SkipNode
from nodes.string_node import StringNode
from nodes.try_catch_node import TryCatchNode
from nodes.unary_operator_node import UnaryOpNode
from nodes.var_access_node import VarAccessNode
from nodes.var_assign_node import VarAssignNode
from nodes.while_node import WhileNode
from parse_result import ParseResult
from tokens import TT_AT, TT_COLON, TT_COMMA, TT_DIV, TT_EE, TT_EOF, TT_FLOAT, TT_GT, TT_GTE, TT_IDENTIFIER, TT_INT, TT_KEYWORD, TT_LCURLY, TT_LPAREN, TT_LSQUARE, TT_LT, TT_LTE, TT_MINUS, TT_MOD, TT_MUL, TT_NE, TT_NEWLINE, TT_PLUS, TT_RCURLY, TT_RPAREN, TT_RSQUARE, TT_STRING, Token


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

    def parse(self):
        res = self.statements()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Unexpected token"
            ))
        return res

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

        # If we've reached EOF after skipping newlines, return empty statements
        if self.current_tok.type == TT_EOF:
            return res.success(ListNode(
                statements,
                pos_start,
                self.current_tok.pos_end.copy()
            ))

        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False
            
            if not more_statements: break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(
            statements,
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        # Check for 'give' (return)
        if self.current_tok.matches(TT_KEYWORD, 'give'):
            res.register_advancement()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))

        # Check for 'cut' (break)
        if self.current_tok.matches(TT_KEYWORD, 'cut'):
            res.register_advancement()
            self.advance()
            return res.success(CutNode(pos_start, self.current_tok.pos_start.copy()))

        # Check for 'skip' (continue)
        if self.current_tok.matches(TT_KEYWORD, 'skip'):
            res.register_advancement()
            self.advance()
            return res.success(SkipNode(pos_start, self.current_tok.pos_start.copy()))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'put', 'keep', 'show', 'when', 'cycle', 'as long as', 'attempt', 'make function', 'give', or expression"
            ))
        return res.success(expr)

    def expr(self):
        res = ParseResult()

        # Check for 'put X in Y' (variable assignment)
        if self.current_tok.matches(TT_KEYWORD, 'put'):
            res.register_advancement()
            self.advance()

            value_expr = res.register(self.logic_expr())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'in'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'in'"
                ))

            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier"
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()
            
            # Check for list access assignment (e.g., put 5 in list @ 0)
            if self.current_tok.type == TT_AT:
                res.register_advancement()
                self.advance()
                
                index_expr = res.register(self.logic_expr())
                if res.error: return res
                
                # This is actually a list element assignment
                # We'll handle this as a special assignment
                list_access = ListAccessNode(VarAccessNode(var_name), index_expr)
                return res.success(VarAssignNode(var_name, value_expr))  # Simplified for now

            return res.success(VarAssignNode(var_name, value_expr))

        # Check for 'keep X as Y' (constant assignment)
        if self.current_tok.matches(TT_KEYWORD, 'keep'):
            res.register_advancement()
            self.advance()

            value_expr = res.register(self.logic_expr())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'as'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'as'"
                ))

            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier"
                ))

            const_name = self.current_tok
            res.register_advancement()
            self.advance()

            return res.success(ConstAssignNode(const_name, value_expr))

        # Check for 'show' (print)
        if self.current_tok.matches(TT_KEYWORD, 'show'):
            res.register_advancement()
            self.advance()

            expr = res.register(self.logic_expr())
            if res.error: return res

            # Create a function call to built-in print
            return res.success(CallNode(VarAccessNode(Token(TT_IDENTIFIER, 'show', self.current_tok.pos_start, self.current_tok.pos_end)), [expr]))

        node = res.register(self.logic_expr())
        if res.error: return res

        return res.success(node)

    def logic_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'not'):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.logic_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, 'and'), (TT_KEYWORD, 'or'))))
        
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected value, identifier, 'not', or expression"
            ))

        return res.success(node)

    def comp_expr(self):
        return self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE))

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_MOD))

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        return self.call()

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: return res

        if self.current_tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.logic_expr()))
                if res.error: return res

                while self.current_tok.type == TT_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.logic_expr()))
                    if res.error: return res

                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ',' or ')'"
                    ))

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        
        # Check for list/dict access with @ (can be chained)
        while self.current_tok.type == TT_AT:
            res.register_advancement()
            self.advance()
            
            # Use atom() instead of logic_expr() to get higher precedence than +
            index = res.register(self.atom())
            if res.error: return res
            
            atom = ListAccessNode(atom, index)
        
        return res.success(atom)

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.matches(TT_KEYWORD, 'true'):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(Token(TT_INT, 1, tok.pos_start, tok.pos_end)))

        elif tok.matches(TT_KEYWORD, 'false'):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(Token(TT_INT, 0, tok.pos_start, tok.pos_end)))

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.logic_expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

        elif tok.type == TT_LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error: return res
            return res.success(list_expr)

        elif tok.type == TT_LCURLY:
            dict_expr = res.register(self.dict_expr())
            if res.error: return res
            return res.success(dict_expr)

        elif tok.matches(TT_KEYWORD, 'when'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        elif tok.matches(TT_KEYWORD, 'cycle'):
            loop_expr = res.register(self.loop_expr())
            if res.error: return res
            return res.success(loop_expr)

        elif tok.matches(TT_KEYWORD, 'as long as'):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)

        elif tok.matches(TT_KEYWORD, 'repeat while'):
            do_while_expr = res.register(self.do_while_expr())
            if res.error: return res
            return res.success(do_while_expr)

        elif tok.matches(TT_KEYWORD, 'make function'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        elif tok.matches(TT_KEYWORD, 'attempt'):
            try_catch_expr = res.register(self.try_catch_expr())
            if res.error: return res
            return res.success(try_catch_expr)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int, float, string, identifier, 'true', 'false', '+', '-', '(', '[', 'when', 'cycle', 'as long as', 'repeat while', 'make function', or 'attempt'"
        ))

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '['"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_RSQUARE:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.logic_expr()))
            if res.error: return res

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.logic_expr()))
                if res.error: return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ',' or ']'"
                ))

            res.register_advancement()
            self.advance()

        return res.success(ListNode(element_nodes, pos_start, self.current_tok.pos_end.copy()))

    def dict_expr(self):
        res = ParseResult()
        key_value_pairs = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LCURLY:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '{'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_RCURLY:
            res.register_advancement()
            self.advance()
        else:
            # Parse first key-value pair
            key_node = res.register(self.logic_expr())
            if res.error: return res

            if self.current_tok.type != TT_COLON:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ':'"
                ))

            res.register_advancement()
            self.advance()

            value_node = res.register(self.logic_expr())
            if res.error: return res

            key_value_pairs.append((key_node, value_node))

            # Parse remaining key-value pairs
            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                key_node = res.register(self.logic_expr())
                if res.error: return res

                if self.current_tok.type != TT_COLON:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ':'"
                    ))

                res.register_advancement()
                self.advance()

                value_node = res.register(self.logic_expr())
                if res.error: return res

                key_value_pairs.append((key_node, value_node))

            if self.current_tok.type != TT_RCURLY:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ',' or '}'"
                ))

            res.register_advancement()
            self.advance()

        return res.success(DictNode(key_value_pairs, pos_start, self.current_tok.pos_end.copy()))

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, 'when'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'when'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.logic_expr())
        if res.error: return res

        if self.current_tok.type != TT_COLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ':'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            statements = res.register(self.statements())
            if res.error: return res
            cases.append((condition, statements, True))

            # Check for 'otherwise when' or 'otherwise'
            while self.current_tok.matches(TT_KEYWORD, 'otherwise'):
                res.register_advancement()
                self.advance()

                if self.current_tok.matches(TT_KEYWORD, 'when'):
                    res.register_advancement()
                    self.advance()

                    condition = res.register(self.logic_expr())
                    if res.error: return res

                    if self.current_tok.type != TT_COLON:
                        return res.failure(InvalidSyntaxError(
                            self.current_tok.pos_start, self.current_tok.pos_end,
                            "Expected ':'"
                        ))

                    res.register_advancement()
                    self.advance()

                    if self.current_tok.type == TT_NEWLINE:
                        res.register_advancement()
                        self.advance()

                        statements = res.register(self.statements())
                        if res.error: return res
                        cases.append((condition, statements, True))
                else:
                    # This is the 'otherwise' (else) case
                    if self.current_tok.type != TT_COLON:
                        return res.failure(InvalidSyntaxError(
                            self.current_tok.pos_start, self.current_tok.pos_end,
                            "Expected ':'"
                        ))

                    res.register_advancement()
                    self.advance()

                    if self.current_tok.type == TT_NEWLINE:
                        res.register_advancement()
                        self.advance()

                        statements = res.register(self.statements())
                        if res.error: return res
                        else_case = (statements, True)
                    break

            if not self.current_tok.matches(TT_KEYWORD, 'end'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'end'"
                ))

            res.register_advancement()
            self.advance()
        else:
            expr = res.register(self.statement())
            if res.error: return res
            cases.append((condition, expr, False))

        return res.success(IfNode(cases, else_case))

    def loop_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'cycle'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'cycle'"
            ))

        res.register_advancement()
        self.advance()

        # Check for 'cycle each item through list' pattern
        if self.current_tok.matches(TT_KEYWORD, 'each'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier"
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if not self.current_tok.matches(TT_KEYWORD, 'through'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'through'"
                ))

            res.register_advancement()
            self.advance()

            iterable = res.register(self.logic_expr())
            if res.error: return res

            if self.current_tok.type != TT_COLON:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ':'"
                ))

            res.register_advancement()
            self.advance()

            if self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()

                body = res.register(self.statements())
                if res.error: return res

                if not self.current_tok.matches(TT_KEYWORD, 'end'):
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected 'end'"
                    ))

                res.register_advancement()
                self.advance()

                return res.success(ForEachNode(var_name, iterable, body))
        
        # Check for 'cycle n from X to Y' pattern
        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected identifier"
            ))

        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if not self.current_tok.matches(TT_KEYWORD, 'from'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'from'"
            ))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.logic_expr())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'to'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'to'"
            ))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.logic_expr())
        if res.error: return res

        # Check for optional 'step' keyword
        step_value = None
        if self.current_tok.matches(TT_KEYWORD, 'step'):
            res.register_advancement()
            self.advance()
            
            step_value = res.register(self.logic_expr())
            if res.error: return res

        if self.current_tok.type != TT_COLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ':'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'end'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'end'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(ForNode(var_name, start_value, end_value, body, step_value))

        body = res.register(self.statement())
        if res.error: return res

        return res.success(ForNode(var_name, start_value, end_value, body, step_value))

    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'as long as'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'as long as'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.logic_expr())
        if res.error: return res

        if self.current_tok.type != TT_COLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ':'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'end'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'end'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(WhileNode(condition, body))

        body = res.register(self.statement())
        if res.error: return res

        return res.success(WhileNode(condition, body))

    def do_while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'repeat while'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'repeat while'"
            ))

        res.register_advancement()
        self.advance()

        # Parse the condition
        condition = res.register(self.logic_expr())
        if res.error: return res

        if self.current_tok.type != TT_COLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ':'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'end'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'end'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(DoWhileNode(body, condition))

        # Single line statement
        body = res.register(self.statement())
        if res.error: return res

        return res.success(DoWhileNode(body, condition))

    def func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'make function'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'make function'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
        else:
            var_name_tok = None

        if self.current_tok.type != TT_LPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '('"
            ))

        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.current_tok.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected identifier"
                    ))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ',' or ')'"
                ))
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier or ')'"
                ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_COLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ':'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'end'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'end'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(FuncDefNode(var_name_tok, arg_name_toks, body))

        body = res.register(self.statement())
        if res.error: return res

        return res.success(FuncDefNode(var_name_tok, arg_name_toks, body))

    def try_catch_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'attempt'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'attempt'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_COLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ':'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            attempt_body = res.register(self.statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'end'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'end'"
                ))

            res.register_advancement()
            self.advance()

            # Skip any newlines between 'end' and 'handle'
            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()

            # Now expect 'handle'
            if not self.current_tok.matches(TT_KEYWORD, 'handle'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'handle'"
                ))

            res.register_advancement()
            self.advance()

            # Check for optional error variable binding: 'as <identifier>'
            error_var_name = None
            if self.current_tok.matches(TT_KEYWORD, 'as'):
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected identifier"
                    ))

                error_var_name = self.current_tok
                res.register_advancement()
                self.advance()

            if self.current_tok.type != TT_COLON:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ':'"
                ))

            res.register_advancement()
            self.advance()

            if self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()

                handle_body = res.register(self.statements())
                if res.error: return res

                if not self.current_tok.matches(TT_KEYWORD, 'end'):
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected 'end'"
                    ))

                res.register_advancement()
                self.advance()

                return res.success(TryCatchNode(attempt_body, handle_body, error_var_name))

            handle_body = res.register(self.statement())
            if res.error: return res

            return res.success(TryCatchNode(attempt_body, handle_body, error_var_name))

        attempt_body = res.register(self.statement())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'handle'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'handle'"
            ))

        res.register_advancement()
        self.advance()

        error_var_name = None
        if self.current_tok.matches(TT_KEYWORD, 'as'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier"
                ))

            error_var_name = self.current_tok
            res.register_advancement()
            self.advance()

        if self.current_tok.type != TT_COLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ':'"
            ))

        res.register_advancement()
        self.advance()

        handle_body = res.register(self.statement())
        if res.error: return res

        return res.success(TryCatchNode(attempt_body, handle_body, error_var_name))

    def bin_op(self, func_a, ops, func_b=None):
        if func_b is None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)