# Module Import Context Preservation - Bug Fix

## Issue

When a function was imported from a module that itself had imports, the function would lose access to those module-level imports when called from the importing context.

### Example of the Bug

```uttr
$ module_a.uttr
bring helper from module_b;

make function use_helper():
    put helper() in result;  $ This would fail when module_a is imported
    give result;
end;
```

When `use_helper` was imported and called from another file, it would fail with "'helper' is not defined", even though the import succeeded when `module_a.uttr` was executed directly.

## Root Cause

In [interpreter.py](interpreter.py) lines 95-107 (visit_VarAccessNode), when accessing a variable (including imported functions), the code would:

1. Retrieve the value from the symbol table
2. For non-mutable types (excluding List/Dict), **copy the value and set its context to the current context**

```python
# OLD CODE (buggy)
if isinstance(value, (List, Dict)):
    value = value.set_pos(node.pos_start, node.pos_end).set_context(context)
else:
    value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
```

When a function from a module was imported:
1. The function had `context` pointing to its defining module (e.g., `module_a`)
2. The module's symbol table contained the imported symbols (e.g., `helper`)
3. When accessed via VarAccessNode, the function was copied and its context was **overwritten** with the importing module's context
4. When the function executed, it created a new context based on `self.context` (now the wrong context)
5. The new context's symbol table parent was the importing module's symbol table, which didn't have `helper`

## Solution

Functions (both user-defined and built-in) should preserve their defining context to maintain access to their module's symbols.

**Key Changes in [interpreter.py](interpreter.py):**

```python
# NEW CODE (fixed)
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
```

**Rationale:**

1. **User-defined Functions (Function class)**: Preserve their original context so they can access symbols from their defining module
2. **Built-in Functions (BuiltInFunction class)**: Update context to current context for proper error reporting
3. **Mutable types (List, Dict)**: Don't copy to allow in-place modifications, update context
4. **Immutable types (Number, String)**: Copy and update context as before

## Testing

The fix was validated with:

- **test_nested_import.uttr**: Tests importing a module that itself imports from another module
- **test_nested_import2.uttr**: Tests calling a function that uses module-level imports
- **test_import_scope.uttr**: Direct test of function scope with imports
- **test_imports_advanced.uttr**: Comprehensive subdirectory import tests
- **test_paths.uttr**: Multi-level nesting and relative path imports

All 43 tests in the test suite pass with 100% success rate.

## Impact

This fix enables:
- Functions to be properly exported and reused across modules
- Nested imports where modules import from other modules
- Complex module hierarchies with proper symbol resolution
- Standard library modules that build upon each other

## Files Modified

- [interpreter.py](interpreter.py) - Lines 95-107: Updated VarAccessNode visitor to preserve function contexts
