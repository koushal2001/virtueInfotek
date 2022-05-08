from abc import ABCMeta, abstractmethod


class IGraph(metaclass=ABCMeta):
    @abstractmethod
    def nodes(self):
        pass


    @abstractmethod
    def edges(self):
        pass

    @abstractmethod
    def neighbors(self, node):
        pass


    @abstractmethod
    def has_node(self, node):
        pass


    @abstractmethod
    def add_node(self, node, attrs=None):
        pass


    @abstractmethod
    def add_edge(self, edge, wt=1, label='', attrs=[]):
        pass


    @abstractmethod
    def has_edge(self, edge):
        pass


    @abstractmethod
    def edge_weight(self, edge):
        pass


    @abstractmethod
    def del_node(self, node):
        pass


class Stats(IGraph):

    WEIGHT_ATTRIBUTE_NAME = "weight"
    DEFAULT_WEIGHT = 0

    LABEL_ATTRIBUTE_NAME = "label"
    DEFAULT_LABEL = ""

    def __init__(self):
        # Metadata about edges
        self.edge_properties = {}    # Mapping: Edge -> Dict mapping, lablel-> str, wt->num
        self.edge_attr = {}          # Key value pairs: (Edge -> Attributes)
        # Metadata about nodes
        self.node_attr = {}          # Pairing: Node -> Attributes
        self.node_neighbors = {}     # Pairing: Node -> Neighbors

    def has_edge(self, edge):
        u,v = edge
        return (u,v) in self.edge_properties and (v,u) in self.edge_properties

    def edge_weight(self, edge):
        return self.get_edge_properties( edge ).setdefault( self.WEIGHT_ATTRIBUTE_NAME, self.DEFAULT_WEIGHT )

    def neighbors(self, node):
        return self.node_neighbors[node]

    def has_node(self, node):
        return node in self.node_neighbors

    def add_edge(self, edge, wt=1, label='', attrs=[]):
        u, v = edge
        if (v not in self.node_neighbors[u] and u not in self.node_neighbors[v]):
            self.node_neighbors[u].append(v)
            if (u != v):
                self.node_neighbors[v].append(u)

            self.add_edge_attributes((u,v), attrs)
            self.set_edge_properties((u, v), label=label, weight=wt)
        else:
            raise ValueError("Edge (%s, %s) already in graph" % (u, v))

    def add_node(self, node, attrs=None):
        if attrs is None:
            attrs = []
        if (not node in self.node_neighbors):
            self.node_neighbors[node] = []
            self.node_attr[node] = attrs
        else:
            raise ValueError("Node %s already in graph" % node)

    def nodes(self):
        return list(self.node_neighbors.keys())

    def edges(self):
        return [ a for a in list(self.edge_properties.keys()) ]

    def del_node(self, node):
        for each in list(self.neighbors(node)):
            if (each != node):
                self.del_edge((each, node))
        del(self.node_neighbors[node])
        del(self.node_attr[node])

    # Helper methods
    def get_edge_properties(self, edge):
        return self.edge_properties.setdefault( edge, {} )

    def add_edge_attributes(self, edge, attrs):
        for attr in attrs:
            self.add_edge_attribute(edge, attr)

    def add_edge_attribute(self, edge, attr):
        self.edge_attr[edge] = self.edge_attributes(edge) + [attr]

        if (edge[0] != edge[1]):
            self.edge_attr[(edge[1],edge[0])] = self.edge_attributes((edge[1], edge[0])) + [attr]

    def edge_attributes(self, edge):
        try:
            return self.edge_attr[edge]
        except KeyError:
            return []

    def set_edge_properties(self, edge, **properties ):
        self.edge_properties.setdefault( edge, {} ).update( properties )
        if (edge[0] != edge[1]):
            self.edge_properties.setdefault((edge[1], edge[0]), {}).update( properties )

    def del_edge(self, edge):
        u, v = edge
        self.node_neighbors[u].remove(v)
        self.del_edge_labeling((u, v))
        if (u != v):
            self.node_neighbors[v].remove(u)
            self.del_edge_labeling((v, u))

    def del_edge_labeling( self, edge ):
        keys = [edge]
        keys.append(edge[::-1])

        for key in keys:
            for mapping in [self.edge_properties, self.edge_attr ]:
                try:
                    del ( mapping[key] )
                except KeyError:
                    pass
