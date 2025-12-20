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
    print("Type 'exit' or press Ctrl+C to quit.")
    print("Type 'help' for quick reference.")
    print()
    
    while True:
        try:
            text = input('uttr > ')
            
            if text.strip() == "":
                continue
            
            if text.strip().lower() == 'exit':
                print("Goodbye!")
                break
            
            if text.strip().lower() == 'help':
                print_help()
                continue
            
            result, error = entry.run('<stdin>', text)

            if error:
                print(error.as_string())
            elif result:
                if isinstance(result, entry.List):
                    if len(result.elements) == 1:
                        print(repr(result.elements[0]))
                    elif len(result.elements) > 1:
                        # Multiple statements, only print if last one has value
                        last = result.elements[-1]
                        if last and not (isinstance(last, entry.Number) and last.value == 0):
                            print(repr(last))
                else:
                    print(repr(result))
                    
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

def print_help():
    """Print quick reference"""
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

Functions:      make function greet(name):
                    show "Hello " + name;
                end;
                
                make function add(a, b):
                    give a + b;
                end;

Built-ins:      show, input, input_int, len, append, 
                pop, extend, run

For full documentation, see README.md
"""
    print(help_text)

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