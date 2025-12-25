"""
UTTR (Understandable Translation Tool for Routines) Interpreter
A procedure-oriented programming language with plain English-like syntax
"""

from context import Context
from functions.builtin_function import BuiltInFunction
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser


from symbol_table import SymbolTable
from values.number_value import Number

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("true", Number.true)
global_symbol_table.set("show", BuiltInFunction.show)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("input_int", BuiltInFunction.input_int)
global_symbol_table.set("len", BuiltInFunction.len)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)
global_symbol_table.set("keys", BuiltInFunction.keys)
global_symbol_table.set("values", BuiltInFunction.values)
global_symbol_table.set("has_key", BuiltInFunction.has_key)
global_symbol_table.set("remove", BuiltInFunction.remove)
global_symbol_table.set("run", BuiltInFunction.run)
global_symbol_table.set("help", BuiltInFunction.help)
global_symbol_table.set("exit", BuiltInFunction.exit)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("error_message", BuiltInFunction.error_message)
global_symbol_table.set("error_type", BuiltInFunction.error_type)
global_symbol_table.set("split", BuiltInFunction.split)
global_symbol_table.set("join", BuiltInFunction.join)
global_symbol_table.set("upper", BuiltInFunction.upper)
global_symbol_table.set("lower", BuiltInFunction.lower)
global_symbol_table.set("replace", BuiltInFunction.replace)
global_symbol_table.set("substring", BuiltInFunction.substring)
global_symbol_table.set("tuple", BuiltInFunction.tuple)
global_symbol_table.set("list", BuiltInFunction.list)

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error