from errors.run_time_error import RTError
from functions.base_function import BaseFunction
from run_time_result import RTResult
from values.dict_value import Dict
from values.error_value import ErrorValue
from values.list_value import List
from values.number_value import Number
from values.string_value import String


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.should_return(): return res

        return_value = res.register(method(exec_ctx))
        if res.should_return(): return res
        return res.success(return_value)

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    # Built-in function implementations
    def execute_show(self, exec_ctx):
        value = exec_ctx.symbol_table.get('value')
        print(str(value))
        return RTResult().success(Number.null)
    execute_show.arg_names = ['value']

    def execute_input(self, exec_ctx):
        text = input()
        return RTResult().success(String(text))
    execute_input.arg_names = []

    def execute_input_int(self, exec_ctx):
        while True:
            text = input()
            try:
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer. Try again!")
        return RTResult().success(Number(number))
    execute_input_int.arg_names = []

    def execute_len(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")

        if isinstance(list_, List):
            return RTResult().success(Number(len(list_.elements)))
        elif isinstance(list_, String):
            return RTResult().success(Number(len(list_.value)))
        else:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be list or string",
                exec_ctx
            ))
    execute_len.arg_names = ["list"]

    def execute_append(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        list_.elements.append(value)
        return RTResult().success(Number.null)
    execute_append.arg_names = ["list", "value"]

    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be number",
                exec_ctx
            ))

        try:
            element = list_.elements.pop(int(index.value))
        except:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                'Element at this index could not be removed from list because index is out of bounds',
                exec_ctx
            ))
        return RTResult().success(element)
    execute_pop.arg_names = ["list", "index"]

    def execute_extend(self, exec_ctx):
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")

        if not isinstance(listA, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(listB, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be list",
                exec_ctx
            ))

        listA.elements.extend(listB.elements)
        return RTResult().success(Number.null)
    execute_extend.arg_names = ["listA", "listB"]

    def execute_run(self, exec_ctx):
        fn = exec_ctx.symbol_table.get("fn")

        if not isinstance(fn, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be string",
                exec_ctx
            ))

        fn = fn.value

        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to load script \"{fn}\"\n" + str(e),
                exec_ctx
            ))

        # Import here to avoid circular dependency
        from entry import run
        _, error = run(fn, script)

        if error:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to finish executing script \"{fn}\"\n" + error.as_string(),
                exec_ctx
            ))

        return RTResult().success(Number.null)
    execute_run.arg_names = ["fn"]

    def execute_keys(self, exec_ctx):
        dict_ = exec_ctx.symbol_table.get("dict")

        if not isinstance(dict_, Dict):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be dictionary",
                exec_ctx
            ))

        keys_list = []
        for key in dict_.elements.keys():
            if isinstance(key, str):
                keys_list.append(String(key))
            else:
                keys_list.append(Number(key))
        
        return RTResult().success(List(keys_list))
    execute_keys.arg_names = ["dict"]

    def execute_values(self, exec_ctx):
        dict_ = exec_ctx.symbol_table.get("dict")

        if not isinstance(dict_, Dict):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be dictionary",
                exec_ctx
            ))

        values_list = list(dict_.elements.values())
        return RTResult().success(List(values_list))
    execute_values.arg_names = ["dict"]

    def execute_has_key(self, exec_ctx):
        dict_ = exec_ctx.symbol_table.get("dict")
        key = exec_ctx.symbol_table.get("key")

        if not isinstance(dict_, Dict):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be dictionary",
                exec_ctx
            ))

        # Convert key to hashable
        if isinstance(key, String):
            hashable_key = key.value
        elif isinstance(key, Number):
            hashable_key = key.value
        else:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Key must be string or number",
                exec_ctx
            ))

        result = 1 if hashable_key in dict_.elements else 0
        return RTResult().success(Number(result))
    execute_has_key.arg_names = ["dict", "key"]

    def execute_remove(self, exec_ctx):
        dict_ = exec_ctx.symbol_table.get("dict")
        key = exec_ctx.symbol_table.get("key")

        if not isinstance(dict_, Dict):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be dictionary",
                exec_ctx
            ))

        # Convert key to hashable
        if isinstance(key, String):
            hashable_key = key.value
        elif isinstance(key, Number):
            hashable_key = key.value
        else:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Key must be string or number",
                exec_ctx
            ))

        if hashable_key in dict_.elements:
            # Modify dictionary in-place (like append and pop for lists)
            removed_value = dict_.elements.pop(hashable_key)
            return RTResult().success(removed_value)
        else:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f'Key "{hashable_key}" not found in dictionary',
                exec_ctx
            ))
    execute_remove.arg_names = ["dict", "key"]

    def execute_help(self, exec_ctx):
        help_text = """
UTTR Quick Reference:
--------------------
Variables:      put 10 in x;
Constants:      keep 3.14 as pi;
Print:          show x;
Comments:       $ single line
                $[ multi-line ]$

Conditionals:   when x > 10:
                    show "big";
                otherwise:
                    show "small";
                end;

Loops:          cycle n from 1 to 10:
                    show n;
                end;
                
                cycle each item through list:
                    show item;
                end;
                
                as long as x < 100:
                    put x + 1 in x;
                end;

Lists:          put [1, 2, 3] in nums;
                show nums @ 0;

Dictionaries:   put {"name": "Alice", "age": 25} in person;
                show person @ "name";
                put "Bob" in person @ "name";

Functions:      make function greet(name):
                    show "Hello " + name;
                end;
                
                make function add(a, b):
                    give a + b;
                end;

Built-ins:      show, input, input_int, len, append, 
                pop, extend, keys, values, has_key, 
                remove, run, help, exit, clear

For full documentation, see README.md
"""
        print(help_text)
        return RTResult().success(Number.null)
    execute_help.arg_names = []

    def execute_exit(self, exec_ctx):
        import sys
        print("Goodbye!")
        sys.exit(0)
    execute_exit.arg_names = []

    def execute_clear(self, exec_ctx):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        return RTResult().success(Number.null)
    execute_clear.arg_names = []

    def execute_error_message(self, exec_ctx):
        error = exec_ctx.symbol_table.get("error")

        if not isinstance(error, ErrorValue):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be an error",
                exec_ctx
            ))

        return RTResult().success(String(error.error_message))
    execute_error_message.arg_names = ["error"]

    def execute_error_type(self, exec_ctx):
        error = exec_ctx.symbol_table.get("error")

        if not isinstance(error, ErrorValue):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be an error",
                exec_ctx
            ))

        return RTResult().success(String(error.error_type))
    execute_error_type.arg_names = ["error"]

    def execute_split(self, exec_ctx):
        string = exec_ctx.symbol_table.get("string")
        delimiter = exec_ctx.symbol_table.get("delimiter")

        if not isinstance(string, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be string",
                exec_ctx
            ))

        # Default delimiter is space if not provided or null
        if delimiter is None or isinstance(delimiter, type(Number.null)) or (hasattr(delimiter, 'value') and delimiter.value == Number.null.value):
            delimiter_str = " "
        elif isinstance(delimiter, String):
            delimiter_str = delimiter.value
        else:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Delimiter must be string or null",
                exec_ctx
            ))

        # Split the string and convert to String values
        parts = string.value.split(delimiter_str)
        result_list = [String(part) for part in parts]
        
        return RTResult().success(List(result_list))
    execute_split.arg_names = ["string", "delimiter"]

    def execute_join(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        separator = exec_ctx.symbol_table.get("separator")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(separator, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be string",
                exec_ctx
            ))

        # Validate all list elements are strings and convert to Python strings
        string_parts = []
        for element in list_.elements:
            if isinstance(element, String):
                string_parts.append(element.value)
            elif isinstance(element, Number):
                string_parts.append(str(element.value))
            else:
                return RTResult().failure(RTError(
                    self.pos_start, self.pos_end,
                    "All list elements must be strings or numbers",
                    exec_ctx
                ))

        # Join the strings
        result = separator.value.join(string_parts)
        return RTResult().success(String(result))
    execute_join.arg_names = ["list", "separator"]

    def execute_upper(self, exec_ctx):
        string = exec_ctx.symbol_table.get("string")

        if not isinstance(string, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be string",
                exec_ctx
            ))

        return RTResult().success(String(string.value.upper()))
    execute_upper.arg_names = ["string"]

    def execute_lower(self, exec_ctx):
        string = exec_ctx.symbol_table.get("string")

        if not isinstance(string, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be string",
                exec_ctx
            ))

        return RTResult().success(String(string.value.lower()))
    execute_lower.arg_names = ["string"]

    def execute_replace(self, exec_ctx):
        string = exec_ctx.symbol_table.get("string")
        old = exec_ctx.symbol_table.get("old")
        new = exec_ctx.symbol_table.get("new")

        if not isinstance(string, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be string",
                exec_ctx
            ))

        if not isinstance(old, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be string",
                exec_ctx
            ))

        if not isinstance(new, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Third argument must be string",
                exec_ctx
            ))

        result = string.value.replace(old.value, new.value)
        return RTResult().success(String(result))
    execute_replace.arg_names = ["string", "old", "new"]

    def execute_substring(self, exec_ctx):
        string = exec_ctx.symbol_table.get("string")
        start = exec_ctx.symbol_table.get("start")
        end = exec_ctx.symbol_table.get("end")

        if not isinstance(string, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be string",
                exec_ctx
            ))

        if not isinstance(start, Number) or start == Number.null:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be a number (null not allowed for start index)",
                exec_ctx
            ))

        start_idx = int(start.value)

        # If end is not provided or is null, slice to end of string
        if end is None or end == Number.null or (isinstance(end, Number) and end.value == Number.null.value):
            result = string.value[start_idx:]
        elif isinstance(end, Number):
            end_idx = int(end.value)
            result = string.value[start_idx:end_idx]
        else:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Third argument must be number or null",
                exec_ctx
            ))

        return RTResult().success(String(result))
    execute_substring.arg_names = ["string", "start", "end"]

# Create built-in function instances
BuiltInFunction.show = BuiltInFunction("show")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.input_int = BuiltInFunction("input_int")
BuiltInFunction.len = BuiltInFunction("len")
BuiltInFunction.append = BuiltInFunction("append")
BuiltInFunction.pop = BuiltInFunction("pop")
BuiltInFunction.extend = BuiltInFunction("extend")
BuiltInFunction.keys = BuiltInFunction("keys")
BuiltInFunction.values = BuiltInFunction("values")
BuiltInFunction.has_key = BuiltInFunction("has_key")
BuiltInFunction.remove = BuiltInFunction("remove")
BuiltInFunction.run = BuiltInFunction("run")
BuiltInFunction.help = BuiltInFunction("help")
BuiltInFunction.exit = BuiltInFunction("exit")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.error_message = BuiltInFunction("error_message")
BuiltInFunction.error_type = BuiltInFunction("error_type")
BuiltInFunction.split = BuiltInFunction("split")
BuiltInFunction.join = BuiltInFunction("join")
BuiltInFunction.upper = BuiltInFunction("upper")
BuiltInFunction.lower = BuiltInFunction("lower")
BuiltInFunction.replace = BuiltInFunction("replace")
BuiltInFunction.substring = BuiltInFunction("substring")