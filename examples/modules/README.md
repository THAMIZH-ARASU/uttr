# UTTR Module Examples

This directory contains example modules demonstrating the UTTR module system.

## Example Files

### calculator.uttr
A reusable calculator library demonstrating basic module creation.

**Exports:**
- `add(a, b)` - Addition
- `subtract(a, b)` - Subtraction
- `multiply(a, b)` - Multiplication
- `divide(a, b)` - Division

**Usage:**
```uttr
bring add, multiply from calculator;
show add(10, 20);       $ Output: 30
show multiply(5, 7);    $ Output: 35
```

### use_calculator.uttr
Demonstrates how to import and use functions from the calculator module.

**Features:**
- Selective imports
- Aliased imports
- Using imported functions

### validation.uttr
Input validation utilities module.

**Exports:**
- `is_positive(n)` - Check if number is positive
- `is_even(n)` - Check if number is even
- `is_valid_age(age)` - Validate age range
- `is_valid_score(score)` - Validate score range

**Usage:**
```uttr
bring is_positive, is_even from validation;
show is_positive(42);   $ Output: 1 (true)
show is_even(7);        $ Output: 0 (false)
```

### stdlib_demo.uttr
Comprehensive demonstration of the standard library modules.

**Demonstrates:**
- Using the `math` standard library (PI, sqrt, pow, etc.)
- Using the `lists` standard library (range, sum, reverse, etc.)
- Using the `strings` standard library (starts_with, trim, etc.)
- Combining multiple standard library functions
- Practical examples for each module

## Running Examples

**Windows PowerShell:**
```powershell
python shell.py examples/modules/use_calculator.uttr
python shell.py examples/modules/stdlib_demo.uttr
```

**Linux/Mac:**
```bash
python3 shell.py examples/modules/use_calculator.uttr
python3 shell.py examples/modules/stdlib_demo.uttr
```

## Standard Library

UTTR includes a standard library located in the `stdlib/` directory:

### math.uttr
Mathematical operations and constants.

**Constants:**
- `PI` - π (3.14159265359)
- `E` - Euler's number (2.71828182846)

**Functions:**
- `abs(n)` - Absolute value
- `pow(base, exponent)` - Power function
- `sqrt(n)` - Square root
- `max(a, b)` - Maximum of two numbers
- `min(a, b)` - Minimum of two numbers
- `round(n)` - Round to nearest integer
- `floor(n)` - Round down
- `ceil(n)` - Round up

### lists.uttr
List utility functions.

**Functions:**
- `range(start_val, stop_val, step_val)` - Generate number range
- `sum(lst)` - Sum all elements
- `max_list(lst)` - Find maximum element
- `min_list(lst)` - Find minimum element
- `reverse(lst)` - Reverse a list
- `contains(lst, item)` - Check if list contains item

### strings.uttr
String manipulation functions.

**Functions:**
- `starts_with(text, prefix)` - Check if string starts with prefix
- `ends_with(text, suffix)` - Check if string ends with suffix
- `trim(text)` - Remove leading/trailing spaces
- `count_occurrences(text, search_str)` - Count substring occurrences
- `repeat(text, times)` - Repeat string n times
- `capitalize(text)` - Capitalize first character

## Module System Features

### Import Syntax
```uttr
$ Import entire module
bring in math;

$ Import specific items
bring sqrt, pow from math;

$ Import with alias
bring sqrt as square_root from math;
```

### Export Syntax
```uttr
$ Explicit exports
make function helper():
    give "Hello";
end;

share helper;

$ Or export all non-underscore definitions automatically
```

### Module Search Paths
1. Current directory of importing file (for relative imports)
2. Current working directory
3. Standard library directory (`stdlib/`)

### Path Resolution
- Use forward slashes for subdirectories: `subdir/module`
- Module names don't need `.uttr` extension
- Absolute file system paths are not supported (for portability)

## Creating Your Own Modules

1. Create a `.uttr` file with functions/variables
2. Optionally use `share` to explicitly export symbols
3. Import in other files using `bring` statements

Example:
```uttr
$ mymodule.uttr
make function greet(name):
    give "Hello, " + name + "!";
end;

share greet;
```

```uttr
$ main.uttr
bring greet from mymodule;
show greet("World");  $ Output: Hello, World!
```

## Best Practices

1. **Use descriptive module names** - Make purpose clear
2. **Export selectively** - Only expose public API with `share`
3. **Use underscore for private functions** - `_internal_helper` won't be auto-exported
4. **Document your exports** - Use comments to describe functions
5. **Keep modules focused** - One clear purpose per module
6. **Use standard library** - Leverage built-in modules when possible

## See Also

- [Main README](../../README.md) - Full language documentation
- [Test Suite](../../tests/README.md) - Comprehensive test examples
- [Module System Documentation](../../README.md#module-system) - Detailed module system docs
