class ShareNode:
    """
    AST node for share (export) statements.
    
    Syntax:
    - share add;           # Export single item
    - share add, subtract; # Export multiple items
    
    Attributes:
        item_name_toks: List of tokens with item names to export
        pos_start: Start position in source
        pos_end: End position in source
    """
    def __init__(self, item_name_toks, pos_start, pos_end):
        self.item_name_toks = item_name_toks
        self.pos_start = pos_start
        self.pos_end = pos_end
