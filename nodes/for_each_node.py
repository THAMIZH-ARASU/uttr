class ForEachNode:
    def __init__(self, var_name_tok, iterable_node, body_node):
        self.var_name_tok = var_name_tok
        self.iterable_node = iterable_node
        self.body_node = body_node
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end