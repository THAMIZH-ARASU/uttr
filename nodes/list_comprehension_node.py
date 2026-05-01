class ListComprehensionNode:
    """
    Represents a list comprehension in the AST.
    
    Structure:
    [expression for var in iterable where condition1 for var2 in iterable2 where condition2]
    
    Attributes:
        expression_node: The expression to evaluate for each element
        comprehension_clauses: List of (var_token, iterable_node, conditions) tuples
                              conditions is a list of condition nodes for 'where' clauses
    """
    
    def __init__(self, expression_node, comprehension_clauses, pos_start, pos_end):
        self.expression_node = expression_node
        self.comprehension_clauses = comprehension_clauses  # List of (var_tok, iterable_node, conditions)
        
        self.pos_start = pos_start
        self.pos_end = pos_end
