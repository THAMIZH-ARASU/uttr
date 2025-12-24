"""
UTTR Interactive Shell and File Runner
Run UTTR code interactively or execute .uttr files
"""

import entry
import sys
import os
from values.list_value import List
from values.number_value import Number

def run_file(filename):
    """Run a UTTR file"""
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found")
        return
    
    try:
        with open(filename, 'r') as f:
            code = f.read()
        
        result, error = entry.run(filename, code)
        
        if error:
            print(error.as_string())
        elif result:
            # Only print result if it's not a list of statements
            if isinstance(result, List) and len(result.elements) > 0:
                # Check if it's a multi-statement program (don't print)
                pass
            elif result and not isinstance(result, Number) or result.value != 0:
                print(repr(result))
    except Exception as e:
        print(f"Error reading file: {e}")

def run_interactive():
    """Run the interactive REPL"""
    print("=" * 60)
    print("UTTR v1.0 - Understandable Translation Tool for Routines")
    print("=" * 60)
    print("Type your code and press Enter.")
    print("Type 'exit();' or press Ctrl+C to quit.")
    print("Type 'help();' for quick reference.")
    print("For multi-line blocks, end with 'end;' and press Enter.")
    print()
    
    # Keywords that start multi-line blocks
    block_starters = ['make function', 'when', 'cycle', 'as long as', 'repeat']
    
    while True:
        try:
            text = input('uttr > ')
            
            if text.strip() == "":
                continue
            
            # Check if this starts a multi-line block
            is_block = any(text.strip().startswith(starter) for starter in block_starters)
            
            if is_block and not text.strip().endswith('end;'):
                # Multi-line input mode with nested block tracking
                lines = [text]
                block_depth = 1  # Start with depth 1 for the initial block
                
                while True:
                    try:
                        line = input('...  > ')
                        lines.append(line)
                        
                        # Count block starters and ends in this line
                        line_stripped = line.strip()
                        
                        # Check for new block starters (including 'otherwise' and 'when')
                        for starter in block_starters:
                            if line_stripped.startswith(starter):
                                block_depth += 1
                                break
                        
                        # 'otherwise' and 'when' inside blocks don't increase depth
                        # but we need to handle them properly
                        if line_stripped.startswith('otherwise:') or line_stripped.startswith('when '):
                            # These are part of the current conditional, check if already counted
                            # Actually, 'when' at start already counted above, 'otherwise' doesn't start new depth
                            pass
                        
                        # Check for 'end;' - this closes one block level
                        if line_stripped == 'end;' or line_stripped.endswith('end;'):
                            block_depth -= 1
                            if block_depth == 0:
                                break
                                
                    except (KeyboardInterrupt, EOFError):
                        print("\nBlock input cancelled")
                        lines = []
                        break
                
                if not lines:
                    continue
                    
                text = '\n'.join(lines)
            
            result, error = entry.run('<stdin>', text)

            if error:
                print(error.as_string())
            elif result:
                if isinstance(result, List):
                    if len(result.elements) == 1:
                        element = result.elements[0]
                        # Check if element is a List with only null values
                        if isinstance(element, List):
                            # Check if all elements in the inner list are null
                            if all(isinstance(e, Number) and e.value == 0 for e in element.elements):
                                pass  # Don't print lists containing only nulls
                            else:
                                print(repr(element))
                        # Don't print if element is Number.null (0)
                        elif not (isinstance(element, Number) and element.value == 0):
                            print(repr(element))
                    elif len(result.elements) > 1:
                        # Multiple statements, only print if last one has value
                        last = result.elements[-1]
                        if last and not (isinstance(last, Number) and last.value == 0):
                            print(repr(last))
                    # If list is empty or all elements are null, don't print anything
                else:
                    # Don't print if result is Number.null (0)
                    if not (isinstance(result, Number) and result.value == 0):
                        print(repr(result))
                    
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # File execution mode
        filename = sys.argv[1]
        
        if not filename.endswith('.uttr'):
            print(f"Warning: '{filename}' doesn't have .uttr extension")
        
        run_file(filename)
    else:
        # Interactive mode
        run_interactive()

if __name__ == '__main__':
    main()