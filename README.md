<div align="left" style="position: relative;">
<h1>UTTR</h1>
<img src="assets/logo.png" align="right" width="30%" style="margin: -20px 0 0 20px;">
<p align="left">
	<em>Understandable Translation Tool for Routines - A procedure-oriented programming language with plain English-like syntax</em>
</p>
<p align="left">
	<img src="https://img.shields.io/github/license/THAMIZH-ARASU/uttr?style=default&logo=opensourceinitiative&logoColor=white&color=66d07d" alt="license">
	<img src="https://img.shields.io/github/last-commit/THAMIZH-ARASU/uttr?style=default&logo=git&logoColor=white&color=66d07d" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/THAMIZH-ARASU/uttr?style=default&color=66d07d" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/THAMIZH-ARASU/uttr?style=default&color=66d07d" alt="repo-language-count">
</p>
<p align="left"><!-- default option, no dependency badges. -->
</p>
<p align="left">
	<!-- default option, no dependency badges. -->
</p>
</div>
<br clear="right">

##  Quick Links

- [ Overview](#-overview)
- [ Features](#-features)
- [ Project Structure](#-project-structure)
  - [ Project Index](#-project-index)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#-prerequisites)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Testing](#-testing)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

<br>

---

##  Overview

UTTR (Understandable Translation Tool for Routines) is a custom-built, procedure-oriented programming language featuring an intuitive, English-like syntax designed for clarity and ease of learning. Built from scratch in Python, UTTR includes a complete interpreter with lexical analysis, parsing, and runtime execution capabilities. The language emphasizes simplicity and readability, making programming concepts more accessible through natural language constructs like `put 10 in x` for variable assignment and `show` for output.

---

##  Features

- **Natural English-Like Syntax**: Write code that reads like plain English with keywords like `put`, `in`, `when`, `otherwise`, `check`, `whether`, `default`, `make function`, `give`, `cut`, `skip`, `attempt`, and `handle`
- **Complete Interpreter**: Full lexer-parser-interpreter pipeline built from scratch with comprehensive error handling and position tracking
- **Procedure-Oriented Design**: Focus on procedures and sequential execution with modular, reusable functions
- **Module System**: Import/export functionality for code organization with natural syntax (`bring in`, `share`), standard library modules, and automatic caching
- **Rich Data Types**: Support for integers, floats, strings, booleans, lists, tuples (immutable lists), dictionaries, and regular expressions with intuitive access using `@` operator for dictionaries and `/` for indexing
- **Regular Expressions**: Full regex support with pattern matching using `r"pattern"` syntax for text processing and validation
- **Operators**: Arithmetic (`+`, `-`, `*`, `/`, `%`), comparison (`==`, `!=`, `<`, `>`, `<=`, `>=`), and logical (`and`, `or`, `not`)
- **Control Structures**: Conditional statements (`when...otherwise`), switch-case statements (`check...whether...default`), loops (`cycle`, `as long as`, `repeat while`), and for-each iteration with loop control (`cut` for break, `skip` for continue)
- **Error Handling**: Try-catch blocks using `attempt...handle` syntax with error introspection (`error_message`, `error_type`)
- **Function Support**: 
  - Named functions with `make function` and `give` keywords
  - Anonymous lambda functions with inline syntax (`lambda x => x * 2`)
  - Higher-order functions (functions as arguments/return values)
- **Built-in Functions**: Pre-defined utilities including:
  - I/O: `show`, `input`, `input_int`
  - Collections: `len`, `append`, `pop`, `extend`
  - Tuples: `tuple` (convert to tuple), `list` (convert to list)
  - Dictionaries: `keys`, `values`, `has_key`, `remove`
  - Strings: `split`, `join`, `upper`, `lower`, `replace`, `substring`
  - Regular Expressions: `regex_match`, `regex_search`, `regex_replace`, `regex_findall`, `regex_split`
  - Error handling: `error_message`, `error_type`
  - Execution: `run` (execute external .uttr files)
- **Standard Library**: Built-in modules for common tasks:
  - `math`: Mathematical functions (sqrt, pow, abs, max, min, etc.) and constants (PI, E)
  - `lists`: List utilities (range, sum, reverse, contains, etc.)
  - `strings`: String operations (starts_with, ends_with, repeat, capitalize, etc.)
- **Variable & Constant Management**: Mutable variables with `put...in` and immutable constants with `keep...as`
- **Comment Support**: Single-line (`$`) and multi-line (`$[...]$`) comments for code documentation
- **Interactive REPL**: Test code snippets interactively or run complete `.uttr` files
- **Comprehensive Error Reporting**: Detailed error messages with line and column information using visual arrows

---


###  Project Index
<details open>
	<summary><b><code>UTTR/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/interpreter.py'>interpreter.py</a></b></td>
				<td>Executes the abstract syntax tree (AST) by visiting nodes and performing operations based on the language's runtime semantics</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/strings_with_arrows.py'>strings_with_arrows.py</a></b></td>
				<td>Generates visual error indicators with arrows pointing to specific error locations in source code for better debugging</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/lexer_testing.py'>lexer_testing.py</a></b></td>
				<td>Testing utility for validating the lexer's tokenization process with various input patterns</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/parser.py'>parser.py</a></b></td>
				<td>Transforms token stream into an abstract syntax tree (AST) according to UTTR's grammar rules</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/symbol_table.py'>symbol_table.py</a></b></td>
				<td>Manages variable and constant storage with scope hierarchy for runtime symbol lookup and assignment</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/context.py'>context.py</a></b></td>
				<td>Maintains execution context information including function call stack and symbol tables</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/position.py'>position.py</a></b></td>
				<td>Tracks line, column, and character positions in source code for accurate error reporting</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/constants.py'>constants.py</a></b></td>
				<td>Defines character sets (digits, letters) used throughout the lexer for token recognition</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/lexer.py'>lexer.py</a></b></td>
				<td>Converts raw source code into tokens for parsing, handling keywords, operators, literals, and comments</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/run_time_result.py'>run_time_result.py</a></b></td>
				<td>Wraps interpreter execution results with success/error status and return value handling</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/parse_result.py'>parse_result.py</a></b></td>
				<td>Encapsulates parser output with AST nodes and error information for downstream processing</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/entry.py'>entry.py</a></b></td>
				<td>Main entry point coordinating lexer, parser, and interpreter with global symbol table initialization</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/shell.py'>shell.py</a></b></td>
				<td>Interactive REPL and file runner for executing UTTR programs from command line or interactively</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/tokens.py'>tokens.py</a></b></td>
				<td>Defines all token types and keywords recognized by the UTTR language lexer</td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- nodes Submodule -->
		<summary><b>nodes</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/const_assign_node.py'>const_assign_node.py</a></b></td>
				<td>AST node representing constant declarations with immutability semantics</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/dict_node.py'>dict_node.py</a></b></td>
				<td>AST node representing dictionary literals with key-value pairs</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/for_node.py'>for_node.py</a></b></td>
				<td>AST node for range-based for loops with start, end, and step expressions</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/list_access_node.py'>list_access_node.py</a></b></td>
				<td>AST node for list element access using index notation</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/unary_operator_node.py'>unary_operator_node.py</a></b></td>
				<td>AST node for unary operations like negation and logical NOT</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/string_node.py'>string_node.py</a></b></td>
				<td>AST node representing string literal values</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/binary_operator_node.py'>binary_operator_node.py</a></b></td>
				<td>AST node for binary operations including arithmetic, comparison, and logical operators</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/if_node.py'>if_node.py</a></b></td>
				<td>AST node for conditional statements with if, elif, and else branches</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/for_each_node.py'>for_each_node.py</a></b></td>
				<td>AST node for iterating over collections with for-each semantics</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/function_definition_node.py'>function_definition_node.py</a></b></td>
				<td>AST node defining function declarations with parameters and body</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/call_node.py'>call_node.py</a></b></td>
				<td>AST node for function invocation with argument evaluation</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/while_node.py'>while_node.py</a></b></td>
				<td>AST node for while loop constructs with condition checking</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/do_while_node.py'>do_while_node.py</a></b></td>
				<td>AST node for do-while loop constructs (executes body before checking condition)</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/number_node.py'>number_node.py</a></b></td>
				<td>AST node representing numeric literal values (integers and floats)</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/var_assign_node.py'>var_assign_node.py</a></b></td>
				<td>AST node for variable assignment and reassignment operations</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/return_node.py'>return_node.py</a></b></td>
				<td>AST node handling function return statements with value expressions</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/cut_node.py'>cut_node.py</a></b></td>
				<td>AST node for break statements (loop early exit)</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/skip_node.py'>skip_node.py</a></b></td>
				<td>AST node for continue statements (skip to next loop iteration)</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/attempt_handle_node.py'>attempt_handle_node.py</a></b></td>
				<td>AST node for attempt...handle error handling blocks</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/list_node.py'>list_node.py</a></b></td>
				<td>AST node representing list literals with element expressions</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/nodes/var_access_node.py'>var_access_node.py</a></b></td>
				<td>AST node for variable and constant value retrieval from symbol table</td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- functions Submodule -->
		<summary><b>functions</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/functions/builtin_function.py'>builtin_function.py</a></b></td>
				<td>Implements standard library functions (show, input, len, append, pop, extend, run) with argument validation</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/functions/function.py'>function.py</a></b></td>
				<td>Manages user-defined functions with parameter binding and execution context setup</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/functions/base_function.py'>base_function.py</a></b></td>
				<td>Abstract base class defining common function interface and execution patterns</td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- values Submodule -->
		<summary><b>values</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/values/number_value.py'>number_value.py</a></b></td>
				<td>Runtime representation of numeric values with arithmetic and comparison operations</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/values/dict_value.py'>dict_value.py</a></b></td>
				<td>Runtime representation of dictionary/map collections with key-based access and manipulation operations</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/values/error_value.py'>error_value.py</a></b></td>
				<td>Runtime representation of caught errors with message, type, and details for error handling</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/values/value.py'>value.py</a></b></td>
				<td>Base class for all runtime values with position tracking and context management</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/values/string_value.py'>string_value.py</a></b></td>
				<td>Runtime representation of string values with concatenation and comparison support</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/values/list_value.py'>list_value.py</a></b></td>
				<td>Runtime representation of list collections with indexing, concatenation, and mutation operations</td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- errors Submodule -->
		<summary><b>errors</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/errors/invalid_syntax.py'>invalid_syntax.py</a></b></td>
				<td>Error class for syntax violations during parsing with expected token information</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/errors/illegal_character.py'>illegal_character.py</a></b></td>
				<td>Error class for unrecognized characters encountered during lexical analysis</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/errors/error.py'>error.py</a></b></td>
				<td>Base error class with position tracking and formatted error message generation</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/errors/run_time_error.py'>run_time_error.py</a></b></td>
				<td>Error class for runtime exceptions with execution context and traceback information</td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- examples Submodule -->
		<summary><b>examples</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/conditionals.uttr'>conditionals.uttr</a></b></td>
				<td>Demonstrates conditional branching with when/otherwise statements</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/dictionaries.uttr'>dictionaries.uttr</a></b></td>
				<td>Shows dictionary creation, key-based access, and built-in dictionary functions</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/lists.uttr'>lists.uttr</a></b></td>
				<td>Shows list creation, indexing, and manipulation operations</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/for_loop.uttr'>for_loop.uttr</a></b></td>
				<td>Illustrates range-based iteration with cycle keyword</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/for_each_loop.uttr'>for_each_loop.uttr</a></b></td>
				<td>Demonstrates iteration over collections using for-each semantics</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/constants.uttr'>constants.uttr</a></b></td>
				<td>Examples of immutable constant declarations with keep/as syntax</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/while_loop.uttr'>while_loop.uttr</a></b></td>
				<td>Shows condition-based looping with as long as construct</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/do_while_loop.uttr'>do_while_loop.uttr</a></b></td>
				<td>Demonstrates do-while loops (repeat while) that execute at least once</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/functions.uttr'>functions.uttr</a></b></td>
				<td>Function definition, invocation, and return value examples</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/variables.uttr'>variables.uttr</a></b></td>
				<td>Basic variable declaration and assignment with put/in syntax</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/nested_condition_and_loop.uttr'>nested_condition_and_loop.uttr</a></b></td>
				<td>Complex control flow with nested conditionals and loops</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/function_with_list.uttr'>function_with_list.uttr</a></b></td>
				<td>Functions working with list parameters and operations</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/comments.uttr'>comments.uttr</a></b></td>
				<td>Demonstrates single-line and multi-line comment syntax</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/break_continue.uttr'>break_continue.uttr</a></b></td>
				<td>Examples of loop control with cut (break) and skip (continue) statements</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/modulo.uttr'>modulo.uttr</a></b></td>
				<td>Demonstrates modulo operator (%) usage for divisibility checks and patterns</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/attempt_handle.uttr'>attempt_handle.uttr</a></b></td>
				<td>Demonstrates attempt...handle error handling with error introspection and recovery patterns</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/examples/tuples.uttr'>tuples.uttr</a></b></td>
				<td>Demonstrates tuple (immutable list) creation, indexing, concatenation, and conversion with `<>` syntax</td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- tests Submodule -->
		<summary><b>tests</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/tests/run_tests.py'>run_tests.py</a></b></td>
				<td>Automated test runner that executes all test files and reports pass/fail statistics</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/THAMIZH-ARASU/uttr/blob/master/tests/README.md'>README.md</a></b></td>
				<td>Comprehensive documentation for the test suite with usage instructions</td>
			</tr>
			<tr>
				<td><b>Test Files</b></td>
				<td>21 test files covering all language features: variables, arithmetic, comparisons, logical operations, strings, conditionals, loops (for/while/do-while/for-each), lists, tuples, dictionaries, list/dict mutations, functions, built-ins, comments, errors, break/continue, modulo operator, and integration tests</td>
			</tr>
			</table>
		</blockquote>
	</details>
</details>

---
##  Getting Started

###  Prerequisites

Before getting started with uttr, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python 3.7+


###  Installation

Install uttr using one of the following methods:

**Build from source:**

1. Clone the uttr repository:
```sh
❯ git clone https://github.com/THAMIZH-ARASU/uttr
```

2. Navigate to the project directory:
```sh
❯ cd uttr
```

3. Install the project dependencies:

No external dependencies required - UTTR uses only Python standard library



###  Usage
Run uttr using the following command:

**Interactive REPL Mode:**
```sh
❯ python shell.py
```

**Execute a .uttr file:**
```sh
❯ python shell.py examples/variables.uttr
```

**Example Code:**
```uttr
$ Variable declaration
put 42 in answer;
show answer;

$ Function definition
make function greet(name):
    show "Hello, " + name + "!";
end;

greet("World");

$ For loop with step
cycle i from 0 to 10 step 2:
    show i;
end;

$ Loop control with cut (break) and skip (continue)
cycle i from 0 to 20:
    when i > 10:
        cut;  $ Exit loop early
    end;
    when i == 5:
        skip;  $ Skip to next iteration
    end;
    show i;
end;

$ Modulo operator for patterns
cycle i from 1 to 16:
    when i % 15 == 0:
        show "FizzBuzz";
    end;
    when i % 3 == 0:
        show "Fizz";
    end;
    when i % 5 == 0:
        show "Buzz";
    end;
end;

$ Dictionary creation and access
put {"name": "Alice", "age": 25, "city": "NYC"} in person;
show "Name: " + person @ "name";
show "Age: " + person @ "age";

$ Dictionary operations
put keys(person) in all_keys;
show "Has 'email' key: " + has_key(person, "email");

$ String methods
put "hello world from uttr" in text;
put upper(text) in uppercase;
show uppercase;

put split(text, " ") in words;
show "Word count: " + len(words);

put join(words, "-") in joined;
show joined;

put replace(text, "uttr", "UTTR") in replaced;
show replaced;

put substring(text, 0, 5) in first_word;
show first_word;

$ Tuples - immutable lists with <> syntax
put <1, 2, 3, 4, 5> in immutable_tuple;
show "Tuple: " + immutable_tuple;
show "Length: " + len(immutable_tuple);
show "First element: " + immutable_tuple / 0;

$ Tuple concatenation
put <1, 2, 3> in t1;
put <4, 5, 6> in t2;
put t1 * t2 in combined;
show "Combined tuple: " + combined;

$ Convert between list and tuple
put [1, 2, 3] in mutable_list;
put tuple(mutable_list) in as_tuple;
put list(as_tuple) in back_to_list;
show "As tuple: " + as_tuple;

$ Tuple immutability - this will cause an error
attempt:
    put immutable_tuple + 6 in modified;
end
handle as error:
    show "Error: " + error_message(error);
end;

$ Try-catch error handling
make function safe_divide(a, b):
    attempt:
        give a / b;
    end
    handle as error:
        show "Error: " + error_message(error);
        give 0;
    end
end;

put safe_divide(10, 2) in result;
show "Result: " + result;

put safe_divide(10, 0) in result;
show "Result: " + result;  $ Handles error gracefully

$ Lambda functions - anonymous functions with inline syntax
put lambda x => x * 2 in double;
show "Double of 5: " + double(5);

$ Lambda with multiple parameters
put lambda a, b => a + b in add;
show "3 + 7 = " + add(3, 7);

$ Lambda as function argument (higher-order functions)
make function apply(func, value):
    give func(value);
end;

show "Apply square: " + apply(lambda x => x * x, 4);

$ Lambda with list processing
make function map_list(func, list):
    put [] in result;
    cycle i from 0 to len(list):
        append(result, func(list / i));
    end;
    give result;
end;

put [1, 2, 3, 4, 5] in numbers;
put map_list(lambda x => x * x, numbers) in squares;
show "Squares: " + squares;
```

###  Module System

UTTR includes a powerful module system for organizing code into reusable libraries.

**Import Syntax:**
```uttr
$ Import entire module
bring in math;

$ Import specific items
bring sqrt, pow from math;

$ Import with alias
bring sqrt as square_root from math;

$ Import multiple items with aliases
bring add as sum, multiply as product from calculator;
```

**Export Syntax:**
```uttr
$ In your module file (mymodule.uttr)
make function helper():
    give "I'm exported!";
end;

$ Explicitly export specific items
share helper;

$ Without share statement, all top-level definitions are exported automatically
```

**Standard Library Modules:**

- **math**: Mathematical operations
  - Constants: `PI`, `E`
  - Functions: `abs`, `pow`, `max`, `min`, `round`, `floor`, `ceil`, `sqrt`
  
- **lists**: List utilities
  - Functions: `range`, `sum`, `max_list`, `min_list`, `reverse`, `contains`
  
- **strings**: String operations
  - Functions: `starts_with`, `ends_with`, `trim`, `count_occurrences`, `repeat`, `capitalize`

**Module Search Paths:**
1. Current directory of the importing file (for relative imports)
2. Current working directory
3. Standard library directory (`stdlib/`)

**Example - Creating a Custom Module:**
```uttr
$ File: calculator.uttr
make function add(a, b):
    give a + b;
end;

make function multiply(a, b):
    give a * b;
end;

share add, multiply;
```

```uttr
$ File: main.uttr
bring add, multiply from calculator;

show add(10, 20);       $ Output: 30
show multiply(5, 7);    $ Output: 35
```

See [examples/modules/](examples/modules/) for more examples.

**Technical Notes:**

- **Function Context Preservation**: When a function is imported from a module, it preserves its original defining context. This allows functions to access other symbols (variables, functions) defined in their module, even when called from a different module.
- **Module Caching**: Modules are executed once and cached. Subsequent imports reuse the cached module.
- **Circular Import Detection**: The module loader detects and prevents circular dependencies.
- **Path Resolution**: Module paths support subdirectories using forward slashes (e.g., `subdir/module`). Absolute file system paths are not supported to maintain portability.
- **Export Behavior**: Without an explicit `share` statement, all non-underscore top-level definitions are exported. Use underscore prefix (e.g., `_helper_func`) for private functions.

###  Regular Expressions

UTTR includes comprehensive regular expression support for pattern matching and text processing using Python's `re` module under the hood.

**Regex Literal Syntax:**

Use the `r"pattern"` syntax (similar to Python raw strings) to create regex patterns:

```uttr
put r"\d{3}-\d{4}" in phone_pattern;
put r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" in email_pattern;
```

**Built-in Regex Functions:**

1. **regex_match(pattern, text)** - Check if pattern matches from the start of string
   ```uttr
   put r"hello" in pattern;
   put regex_match(pattern, "hello world") in result;  $ Returns match object
   ```

2. **regex_search(pattern, text)** - Search for pattern anywhere in string
   ```uttr
   put r"\d+" in pattern;
   put regex_search(pattern, "I have 42 apples") in result;
   when result:
       show "Found: " + result @ "matched_text";
       show "At position: " + result @ "start_pos";
   end;
   ```
   Returns a dictionary with: `matched_text`, `start_pos`, `end_pos`, `groups` (list of captured groups)

3. **regex_replace(pattern, replacement, text)** - Replace all pattern matches
   ```uttr
   put r"\d+" in pattern;
   put regex_replace(pattern, "X", "I have 42 apples") in result;
   $ Result: "I have X apples"
   ```

4. **regex_findall(pattern, text)** - Find all matches and return as list
   ```uttr
   put r"\d+" in pattern;
   put regex_findall(pattern, "1 and 2 and 3") in numbers;
   $ Result: ["1", "2", "3"]
   ```

5. **regex_split(pattern, text)** - Split string by pattern
   ```uttr
   put r"\s+" in pattern;
   put regex_split(pattern, "one  two   three") in words;
   $ Result: ["one", "two", "three"]
   ```

**Common Use Cases:**

```uttr
$ Email validation
make function is_valid_email(email):
    put r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" in pattern;
    put regex_match(pattern, email) in match;
    when match:
        give 1;
    end;
    otherwise:
        give 0;
    end;
end;

$ Extract phone numbers
put "Contact: 555-1234 or 555-5678" in text;
put r"\d{3}-\d{4}" in phone_pattern;
put regex_findall(phone_pattern, text) in phones;
show phones;  $ ["555-1234", "555-5678"]

$ Clean up whitespace
put "Too    many     spaces" in messy;
put r"\s+" in spaces_pattern;
put regex_replace(spaces_pattern, " ", messy) in clean;
show clean;  $ "Too many spaces"

$ URL parsing with groups
put "https://example.com:8080/path" in url;
put r"(https?)://([^:]+):(\d+)(/.*)" in pattern;
put regex_search(pattern, url) in match;
when match:
    put match @ "groups" in parts;
    show "Protocol: " + parts / 0;  $ "https"
    show "Domain: " + parts / 1;    $ "example.com"
    show "Port: " + parts / 2;      $ "8080"
    show "Path: " + parts / 3;      $ "/path"
end;
```

**Error Handling:**

Invalid regex patterns are caught at runtime:

```uttr
attempt:
    put r"[invalid(" in bad_pattern;
    put regex_match(bad_pattern, "test") in result;
end
handle as error:
    show "Regex error: " + error_message(error);
end;
```

See [examples/regex_basics.uttr](examples/regex_basics.uttr) for more examples.

###  Testing

UTTR includes a comprehensive test suite covering all language features. Run tests using:

**Run all tests:**
```sh
> python tests/run_tests.py
```

**Run all tests with their output:**
```pwsh
> Get-ChildItem tests\test_*.uttr | ForEach-Object { Write-Host "`n=== Testing $($_.Name) ==="; python shell.py $_.FullName }
```

**Run individual test files:**
```sh
> python shell.py tests/test_variables.uttr
> python shell.py tests/test_tuples.uttr
> python shell.py tests/test_dictionaries.uttr
> python shell.py tests/test_functions.uttr
> python shell.py tests/test_break_continue.uttr
> python shell.py tests/test_modulo.uttr
> python shell.py tests/test_imports.uttr
```

**Test lexer output:**
```sh
> python lexer_testing.py <file_name>
```

The test suite includes 22 test categories with 230+ individual tests covering:
- Variables and constants
- Arithmetic and comparison operations
- Modulo operator (`%`) for divisibility checks
- Logical operations
- String operations with escape sequences
- Conditional statements
- All loop types (for, while, do-while, for-each)
- Loop control (break with `cut`, continue with `skip`)
- Try-catch error handling (`attempt...handle` with error introspection)
- Lists, tuples (immutable lists), and dictionaries
- List mutations (append, pop, extend) and dictionary mutations (remove)
- Tuple immutability and conversions
- Functions and built-ins
- Lambda/anonymous functions with inline syntax
- Module system (imports, exports, standard library, error handling)
- Regular expressions (pattern matching, search, replace, findall, split)
- Comments and error handling
- Complex integration scenarios


---
##  Project Roadmap

### Completed
- [X] **`Task 1`**: <strike>Implement lexer with tokenization for all language constructs</strike>
- [X] **`Task 2`**: <strike>Build parser to generate AST from tokens</strike>
- [X] **`Task 3`**: <strike>Create interpreter with runtime execution</strike>
- [X] **`Task 4`**: <strike>Add support for functions, loops, and conditionals</strike>
- [X] **`Task 5`**: <strike>Implement comprehensive error handling with position tracking</strike>
- [X] **`Task 6`**: <strike>Add do-while loop support with repeat while keyword</strike>
- [X] **`Task 7`**: <strike>Add support for dictionaries/maps data structure</strike>
- [X] **`Task 8`**: <strike>Add break and continue statements for loop control (`cut` and `skip` keywords)</strike>
- [X] **`Task 9`**: <strike>Add modulo operator (`%`) for arithmetic operations</strike>
- [X] **`Task 10`**: <strike>Fix list/dictionary mutation functions (append, pop, extend, remove)</strike>
- [X] **`Task 11`**: <strike>Implement try-catch error handling (`attempt...handle` syntax)</strike>
- [X] **`Task 12`**: <strike>Add built-in methods for strings (split, join, upper, lower, replace, substring)</strike>
- [X] **`Task 13`**: <strike>Support for tuple data type (immutable lists with `<>` syntax)</strike>
- [X] **`Task 14`**: <strike>Add import/module system for code organization</strike>
- [X] **`Task 15`**: <strike>Implement lambda/anonymous functions with inline syntax (`lambda x => x * 2`)</strike>
- [X] **`Task 16`**: <strike>Add switch-case statements (`check...whether...default` syntax)</strike>
- [X] **`Task 17`**: <strike>Support for regular expressions with pattern matching (`r"pattern"` syntax, `regex_match`, `regex_search`, `regex_replace`, `regex_findall`, `regex_split`)</strike>

### Language Features
- [ ] **`Task 18`**: Add set data type with set operations (union, intersection, difference)

### Advanced Operations
- [ ] **`Task 19`**: Implement list comprehensions with natural syntax
- [ ] **`Task 20`**: Add dictionary comprehensions
- [ ] **`Task 21`**: Support for multiple return values from functions
- [ ] **`Task 22`**: Implement variadic functions (variable argument count) with natural syntax
- [ ] **`Task 23`**: Support for ternary conditional expressions

### File & I/O Operations
- [ ] **`Task 22`**: Add file I/O operations (read_file, write_file, append_file)
- [ ] **`Task 23`**: Implement JSON parsing and generation functions
### File & I/O Operations
- [ ] **`Task 24`**: Add file I/O operations (read_file, write_file, append_file)
- [ ] **`Task 25`**: Implement JSON parsing and generation functions
- [ ] **`Task 26`**: Add CSV file reading and writing capabilities
- [ ] **`Task 27`**: Support for command-line arguments in .uttr files

### Standard Library Expansion
- [ ] **`Task 28`**: Add math functions (sqrt, pow, abs, round, floor, ceil, sin, cos, tan)
- [ ] **`Task 29`**: Implement random number generation functions
- [ ] **`Task 30`**: Add date and time manipulation functions
- [ ] **`Task 31`**: Create string formatting utilities (template-based approach)
- [ ] **`Task 32`**: Add list sorting and filtering built-in functions
- [ ] **`Task 33`**: Implement type checking and conversion functions

### Optimization & Performance
- [ ] **`Task 34`**: Optimize interpreter with bytecode compilation
- [ ] **`Task 35`**: Implement caching for frequently used expressions
- [ ] **`Task 36`**: Add tail call optimization for recursive functions
- [ ] **`Task 37`**: Create AST optimization passes before interpretation

### Interoperability
- [ ] **`Task 38`**: Add Python interop to call Python libraries from UTTR
- [ ] **`Task 39`**: Create UTTR-to-Python transpiler for performance
- [ ] **`Task 40`**: Support for calling external executables/shell commands
- [ ] **`Task 41`**: Add HTTP client functions for web requests

### Documentation & Examples
- [ ] **`Task 42`**: Create interactive tutorial website for UTTR
- [ ] **`Task 43`**: Add more complex example projects
- [ ] **`Task 44`**: Create video tutorials for language features

### Quality Assurance & Testing
- [ ] **`Task 45`**: Expand test coverage to 100% of codebase
- [ ] **`Task 46`**: Add benchmark suite to track performance over time
- [ ] **`Task 47`**: Implement fuzzing tests for parser robustness

### Developer Tools
- [ ] **`Task 48`**: Build debugging tools with breakpoint support
- [ ] **`Task 49`**: Add code formatter/prettifier for UTTR files
- [ ] **`Task 50`**: Create syntax highlighting extension for VS Code
- [ ] **`Task 51`**: Implement static type checking (optional type annotations)
- [ ] **`Task 52`**: Create linter for code quality and style enforcement
- [ ] **`Task 53`**: Add performance profiler to identify bottlenecks

---

##  Contributing

- **💬 [Join the Discussions](https://github.com/THAMIZH-ARASU/uttr/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/THAMIZH-ARASU/uttr/issues)**: Submit bugs found or log feature requests for the `uttr` project.
- **💡 [Submit Pull Requests](https://github.com/THAMIZH-ARASU/uttr/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/THAMIZH-ARASU/uttr
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/THAMIZH-ARASU/uttr/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=THAMIZH-ARASU/uttr">
   </a>
</p>
</details>

---

##  License

This project is protected under the [MIT](https://choosealicense.com/licenses/mit/) License. For more details, refer to the [LICENSE](https://github.com/THAMIZH-ARASU/uttr/blob/master/LICENSE) file.

---

##  Acknowledgments

- Inspired by the desire to create a more readable and intuitive programming language for beginners
- Built with Python's powerful language processing capabilities
- Thanks to the open-source community for tools and inspiration

---
