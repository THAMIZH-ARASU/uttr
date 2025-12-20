class ListAccessNode:
    def __init__(self, list_node, index_node):
        self.list_node = list_node
        self.index_node = index_node
        self.pos_start = self.list_node.pos_start
        self.pos_end = self.index_node.pos_end