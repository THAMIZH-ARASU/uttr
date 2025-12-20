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

- **Natural English-Like Syntax**: Write code that reads like plain English with keywords like `put`, `in`, `when`, `otherwise`, `make function`, and `give`
- **Complete Interpreter**: Full lexer-parser-interpreter pipeline built from scratch with comprehensive error handling and position tracking
- **Procedure-Oriented Design**: Focus on procedures and sequential execution with modular, reusable functions
- **Rich Data Types**: Support for integers, floats, strings, booleans, and lists with intuitive list access using `@` operator
- **Control Structures**: Conditional statements (`when...otherwise`), loops (`cycle`, `repeat while`), and for-each iteration
- **Function Support**: Define and call custom functions with return values using `make function` and `give` keywords
- **Built-in Functions**: Pre-defined utilities including `show`, `input`, `input_int`, `len`, `append`, `pop`, and `extend`
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
				<td>Shows condition-based looping with repeat while construct</td>
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
```

###  Testing
Run the following command to test the lexer's output:

```sh
❯ python lexer_testing.py <file_name>
```


---
##  Project Roadmap

- [X] **`Task 1`**: <strike>Implement lexer with tokenization for all language constructs</strike>
- [X] **`Task 2`**: <strike>Build parser to generate AST from tokens</strike>
- [X] **`Task 3`**: <strike>Create interpreter with runtime execution</strike>
- [X] **`Task 4`**: <strike>Add support for functions, loops, and conditionals</strike>
- [X] **`Task 5`**: <strike>Implement comprehensive error handling with position tracking</strike>
- [ ] **`Task 6`**: Add support for dictionaries/maps data structure
- [ ] **`To be added`**

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
