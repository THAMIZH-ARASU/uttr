class DoWhileNode:
    def __init__(self, body_node, condition_node):
        self.body_node = body_node
        self.condition_node = condition_node
        self.pos_start = self.body_node.pos_start
        self.pos_end = self.condition_node.pos_end
