from .Text_Statestics import Stats


def generate_hierarchy(combined_word):
    hierarchy = Stats()
    for words in combined_word:
        if not hierarchy.has_node(words):
            hierarchy.add_node(words)
    return hierarchy


def remove_unwanted_words(hierarchy):
    for node in hierarchy.nodes():
        if sum(hierarchy.edge_weight((node, other)) for other in hierarchy.neighbors(node)) == 0:
            hierarchy.del_node(node)
