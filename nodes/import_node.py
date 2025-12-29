class ImportNode:
    """
    AST node for import statements.
    
    Syntax variants:
    - bring in math;                    # Import entire module
    - bring add from math;              # Import specific item
    - bring add, subtract from math;    # Import multiple items
    - bring add as addition from math;  # Import with alias
    
    Attributes:
        module_name_tok: Token with the module name
        items: List of (item_name_tok, alias_tok) tuples, or None for full import
        pos_start: Start position in source
        pos_end: End position in source
    """
    def __init__(self, module_name_tok, items=None):
        self.module_name_tok = module_name_tok
        self.items = items  # None means import all, otherwise list of (name, alias) tuples
        
        self.pos_start = self.module_name_tok.pos_start
        self.pos_end = self.module_name_tok.pos_end
