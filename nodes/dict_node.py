class DictNode:
    def __init__(self, key_value_pairs, pos_start, pos_end):
        self.key_value_pairs = key_value_pairs  # List of tuples (key_node, value_node)
        self.pos_start = pos_start
        self.pos_end = pos_end
