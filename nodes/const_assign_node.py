class ConstAssignNode:
    def __init__(self, const_name_tok, value_node):
        self.const_name_tok = const_name_tok
        self.value_node = value_node
        self.pos_start = self.value_node.pos_start
        self.pos_end = self.const_name_tok.pos_end