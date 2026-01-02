class LambdaNode:
    def __init__(self, arg_name_toks, body_node, pos_start, pos_end):
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node
        self.pos_start = pos_start
        self.pos_end = pos_end
    
    def __repr__(self):
        return f'LambdaNode({self.arg_name_toks}, {self.body_node})'
