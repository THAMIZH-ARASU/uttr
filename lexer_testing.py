from lexer import Lexer
import sys

if len(sys.argv) > 1:
    file_name = sys.argv[1]
    with open(file_name, 'r') as file:
        content = file.read()

    lexer = Lexer('test', content)
    tokens, error = lexer.make_tokens()
    print("Contents of", file_name)
    print(content)
    print("-" * 80)
    print("Lexing Result:")
    
    if error:
        print(f'Error: {error}')
    else:
        print("Tokens:")
        for tok in tokens:
            print(tok)
else:
    print("Please provide a file to lex.")
