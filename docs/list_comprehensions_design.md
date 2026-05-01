# List Comprehensions Feature - Design Document

## Overview
Implement list comprehensions in UTTR with natural English-like syntax consistent with the language's design philosophy.

## Project Understanding
UTTR is a procedure-oriented programming language built from scratch in Python with:
- **Lexer**: Tokenizes source code into tokens
- **Parser**: Converts tokens into Abstract Syntax Tree (AST)
- **Interpreter**: Executes AST nodes with symbol tables for variable scope
- **Nodes**: Different node types in `nodes/` directory for language constructs
- **Values**: Different value types in `values/` directory (List, Tuple, Set, Dict, Number, String, etc.)

## Proposed Syntax

### Basic List Comprehension
```uttr
put [x * 2 cycle x in [1, 2, 3, 4, 5]] in doubled;
```

### With Filter Condition
```uttr
put [x * 2 cycle x in [1, 2, 3, 4, 5] where x > 2] in result;
```

### Nested Comprehensions
```uttr
put [x + y cycle x in [1, 2] cycle y in [10, 20]] in nested;
```

### Multiple Conditions
```uttr
put [x cycle x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] where x > 2 where x < 8] in filtered;
```

## Implementation Plan

### 1. Keywords
Update `tokens.py`:
- `cycle` - for comprehensions (already exists for loops)
- `where` - for filtering conditions
- `in` - already exists

### 2. AST Node
Create `nodes/list_comprehension_node.py`:
```python
class ListComprehensionNode:
    def __init__(self, expression_node, comprehension_clauses, pos_start, pos_end)
    # where comprehension_clauses is a list of (var_token, iterable_node, condition_nodes)
```

### 3. Parser Updates
Modify `parser.py`:
- Update list parsing logic to detect comprehension syntax
- Check if `[` is followed by an expression and `for` keyword
- Recursively parse comprehension clauses
- Parse optional `where` conditions

### 4. Interpreter Updates
Add to `interpreter.py`:
```python
def visit_ListComprehensionNode(self, node, context):
    # Create new context for comprehension variables (scoped)
    # Execute nested loops
    # Apply filter conditions
    # Evaluate expression for each valid element
    # Return new List
```

### 5. Scoping Considerations
- Variables in comprehension should not pollute outer scope
- Create a new child context for comprehension
- Filter conditions have access to comprehension variables

### 6. Edge Cases to Handle
- Empty input lists
- Type mismatches in expression
- Undefined variables in iterable
- Invalid filter conditions
- Multiple nested levels
- Multiple conditions combined with logical operators

## Testing Strategy

### Debug Files (debug/)
- `debug_list_comp_simple.uttr` - Basic functionality
- `debug_list_comp_filter.uttr` - Filter with where
- `debug_list_comp_nested.uttr` - Nested loops
- `debug_list_comp_complex.uttr` - Complex scenarios

### Unit Tests (tests/)
- `test_list_comprehensions.uttr` - Comprehensive test suite

### Integration
- Ensure backward compatibility
- Test with existing language features (lambdas, functions, etc.)

## Documentation Updates
1. Update `README.md` Features section
2. Add to Project Roadmap section
3. Create `examples/list_comprehensions.uttr`
4. Update grammar documentation if exists

## Success Criteria
✓ Basic list comprehension syntax works
✓ Filter/where clause works
✓ Nested comprehensions work
✓ Variable scoping is correct
✓ Error handling is robust
✓ No breaking changes to existing features
✓ Comprehensive documentation and examples
