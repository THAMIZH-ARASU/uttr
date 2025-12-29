# UTTR Test Suite

Comprehensive test suite for the UTTR programming language.

## Overview

This test suite covers all major features of the UTTR language, including:

- **Variables and Constants** - Variable assignment, reassignment, and constant declarations
- **Arithmetic Operations** - Addition, subtraction, multiplication, division, order of operations
- **Comparison Operations** - Equality, inequality, less than, greater than, etc.
- **Logical Operations** - AND, OR, NOT, complex boolean expressions
- **String Operations** - Concatenation, special characters, string manipulation
- **Conditional Statements** - if/when/otherwise, nested conditionals, elif chains
- **For Loops** - Range-based iteration with cycle keyword
- **While Loops** - Condition-based looping with "as long as"
- **Do-While Loops** - Post-condition loops with "repeat while"
- **For-Each Loops** - Collection iteration with "cycle each through"
- **Lists** - Creation, access, manipulation, built-in functions
- **Tuples** - Immutable lists, tuple syntax, conversions
- **Dictionaries** - Key-value pairs, access, keys(), values(), has_key(), remove()
- **Functions** - Definition, parameters, return values, recursion
- **Built-in Functions** - show, len, append, pop, extend, keys, values, etc.
- **Module System** - Imports, exports, standard library, nested imports, path resolution
- **Loop Control** - Break (cut) and continue (skip) statements
- **Error Handling** - Try-catch with attempt/handle, error introspection
- **Modulo Operator** - Divisibility checks, remainders, combined with cut/skip
- **Comments** - Single-line ($) and multi-line ($[...]$) comments
- **Integration Tests** - Complex real-world scenarios

## Test Files

### Basic Features
1. `test_variables.uttr` - Variables and Constants (10 tests)
2. `test_arithmetic.uttr` - Arithmetic Operations (12 tests)
3. `test_comparisons.uttr` - Comparison Operations (8 tests)
4. `test_logical.uttr` - Logical Operations (9 tests)
5. `test_strings.uttr` - String Operations (10 tests)

### Control Flow
6. `test_conditionals.uttr` - Conditional Statements (10 tests)
7. `test_for_loops.uttr` - For Loops (10 tests)
8. `test_while_loops.uttr` - While Loops (8 tests)
9. `test_do_while_loops.uttr` - Do-While Loops (8 tests)
10. `test_foreach_loops.uttr` - For-Each Loops (10 tests)

### Data Structures
11. `test_lists.uttr` - List Operations (14 tests)
12. `test_nested_lists.uttr` - Nested List Operations (8 tests)
13. `test_list_mutations.uttr` - List Mutations (append, pop, extend) (6 tests)
14. `test_tuples.uttr` - Tuple Operations (10 tests)
15. `test_nested_tuples.uttr` - Nested Tuple Operations (6 tests)
16. `test_dictionaries.uttr` - Dictionary Operations (15 tests)
17. `test_dict_mutations.uttr` - Dictionary Mutations (6 tests)

### Functions
18. `test_functions.uttr` - Function Definitions (12 tests)
19. `test_function_call.uttr` - Function Calls (5 tests)
20. `test_builtins.uttr` - Built-in Functions (14 tests)

### Module System
21. `test_imports.uttr` - Import System (10 tests)
22. `test_imports_advanced.uttr` - Advanced Imports (8 tests)
23. `test_import_scope.uttr` - Import Scope and Context (1 test)
24. `test_nested_import.uttr` - Nested Module Imports (1 test)
25. `test_nested_import2.uttr` - Indirect Module Imports (1 test)
26. `test_paths.uttr` - Module Path Resolution (3 tests)
27. `test_module_a.uttr` - Module A (test module)
28. `test_module_b.uttr` - Module B (test module)

### Loop Control and Operators
29. `test_break_continue.uttr` - Break (cut) and Continue (skip) (10 tests)
30. `test_modulo.uttr` - Modulo Operator (10 tests)

### Error Handling
31. `test_attempt_handle.uttr` - Try-Catch Error Handling (8 tests)
32. `test_errors.uttr` - Error Detection (10 tests)

### Language Features
33. `test_comments.uttr` - Comment Syntax (10 tests)
34. `test_string_methods.uttr` - String Methods (10 tests)
35. `test_mutations.uttr` - Mutation Operations (6 tests)
36. `test_mixed_nesting.uttr` - Mixed Nesting (5 tests)
37. `test_integration.uttr` - Complex Integration Tests (10 tests)

## Running Tests

### Run Individual Test Files

```bash
# Windows PowerShell
python shell.py tests/test_variables.uttr
python shell.py tests/test_lists.uttr
python shell.py tests/test_dictionaries.uttr

# Linux/Mac
python3 shell.py tests/test_variables.uttr
python3 shell.py tests/test_lists.uttr
python3 shell.py tests/test_dictionaries.uttr
```

### Run All Tests

**Windows PowerShell:**
```powershell
Get-ChildItem tests\*.uttr | ForEach-Object { python shell.py $_.FullName }
```

**Windows Command Prompt:**
```cmd
for %f in (tests\*.uttr) do python shell.py %f
```

**Linux/Mac:**
```bash
for f in tests/*.uttr; do python3 shell.py "$f"; done
```

### Run Specific Test Categories

```bash
# Basic features
python shell.py tests/test_variables.uttr
python shell.py tests/test_arithmetic.uttr
python shell.py tests/test_strings.uttr

# Control flow
python shell.py tests/test_conditionals.uttr
python shell.py tests/test_for_loops.uttr
python shell.py tests/test_while_loops.uttr

# Data structures
python shell.py tests/test_lists.uttr
python shell.py tests/test_dictionaries.uttr

# Functions
python shell.py tests/test_functions.uttr
python shell.py tests/test_builtins.uttr

# Integration
python shell.py tests/test_integration.uttr

# Module system
python shell.py tests/test_imports.uttr
python shell.py tests/test_imports_advanced.uttr
python shell.py tests/test_paths.uttr
```

## Test Statistics

- **Total Test Files**: 43
- **Total Individual Tests**: 230+
- **Code Coverage**: All documented UTTR features including module system
- **Integration Tests**: 10+ complex scenarios
- **Module System Tests**: 8 test files covering imports, exports, standard library, and nested imports

## Test Results

All tests are designed to:
- Execute without errors when features work correctly
- Display clear output showing test progress
- Demonstrate feature usage with practical examples
- Provide comprehensive coverage of edge cases

## Adding New Tests

To add new tests:

1. Create a new `.uttr` file in the `tests/` directory
2. Follow the naming convention: `test_<feature>.uttr`
3. Include a header comment describing the test suite
4. Number each test clearly (Test 1, Test 2, etc.)
5. Add descriptive show statements for test output
6. Include a completion message at the end

Example template:
```uttr
$ ============================================
$ UTTR Test Suite - <Feature Name>
$ ============================================

$ Test 1: <Description>
<test code>
show "Test 1 - <Description>: " + result;

$ ... more tests ...

show "=== All <feature> tests passed! ===";
```

## Known Issues

The `test_errors.uttr` file contains commented-out tests that would deliberately cause errors. These are skipped to allow the test suite to complete. Uncomment specific tests to verify error handling behavior.

## Contributing

When adding new language features, please:
1. Create corresponding test files
2. Update this README with test information
3. Ensure tests cover normal cases and edge cases
4. Document expected behavior in comments

## License

This test suite is part of the UTTR project and follows the same MIT license.
