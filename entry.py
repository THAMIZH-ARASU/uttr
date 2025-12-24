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
global_symbol_table.set("run", BuiltInFunction.run)
global_symbol_table.set("help", BuiltInFunction.help)
global_symbol_table.set("exit", BuiltInFunction.exit)
global_symbol_table.set("clear", BuiltInFunction.clear)

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