import networkx as nx


class Grid:
    """Defines a basic grid in eDisGo

    Attributes
    ----------
    _network : Network #TODO: ADD CORRECT REF
        Network which this scenario is associated with
    _voltage_nom : int
        Nominal voltage
    _peak_load : :obj:`float`
        Cumulative peak load of grid
    _peak_generation : :obj:`float`
        Cumulative peak generation of grid
    _grid_district : :obj:`dict`
        Contains information about grid district (supplied region) of grid,
        format: #TODO: DEFINE FORMAT
    _station : #TODO: ADD CORRECT REF
        The station the grid is fed by
    """

    def __init__(self, **kwargs):
        self._network = kwargs.get('network', None)
        self._voltage_nom = kwargs.get('voltage_nom', None)
        self._peak_load = kwargs.get('peak_load', None)
        self._peak_generation = kwargs.get('peak_generation', None)
        self._grid_district = kwargs.get('grid_district', None)
        self._station = kwargs.get('station', None)

        self._graph = Graph()

    def connect_generators(self, generators):
        """Connects generators to grid

        Parameters
        ----------
        generators: :pandas:`pandas.DataFrame<dataframe>`
            Generators to be connected

        """
        raise NotImplementedError

    @property
    def graph(self):
        """Provide access to the graph"""
        return self._graph

    @property
    def station(self):
        """Provide access to station"""
        return self._station


class MVGrid(Grid):
    """Defines a medium voltage grid in eDisGo

    Attributes
    ----------
    _mv_disconn_points : :obj:`list` of #TODO: FINISH
        Medium voltage disconnecting points = points where MV rings are split under
        normal operation conditions (= switch disconnectors in DINGO).
    _aggregates : :obj:`list` of :obj:`dict`
        This attribute is used for DINGO-imported data only. It contains data from
        DINGO's Aggregated Load Areas. Each list element represents one aggregated
        Load Area.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._mv_disconn_points = kwargs.get('mv_disconn_points', None)
        self._aggregates = kwargs.get('aggregates', None)


class LVGrid(Grid):
        """Defines a low voltage grid in eDisGo

        """

        def __init__(self, **kwargs):
            super().__init__(**kwargs)



class Graph(nx.Graph):
    """Graph object

    This graph is an object subclassed from `networkX.Graph` extended by extra
    functionality and specific methods.
    """

    def nodes_from_line(self, line):
        """
        Get nodes adjacent to line

        Here, line refers to the object behind the key 'line' of the attribute
        dict attached to each edge.

        Parameters
        ----------
        line: edisgo.grid.components.Line
            A eDisGo line object

        Returns
        -------
        tuple
            Nodes adjacent to this edge
        """

        return dict([(v, k) for k, v in
              nx.get_edge_attributes(self, 'line').items()])[line]

    def nodes_by_attribute(self, attr_val, attr='type'):
        """
        Select Graph's nodes by attribute value

        Get all nodes that share the same attribute. By default, the attr 'type'
        is used to specify the nodes type (generator, load, etc.).

        Examples
        --------
        >>> import edisgo
        >>> G = edisgo.grids.Graph()
        >>> G.add_node(1, type='generator')
        >>> G.add_node(2, type='load')
        >>> G.add_node(3, type='generator')
        >>> G.nodes_by_attribute('generator')
        [1, 3]

        Parameters
        ----------
        attr_val: str
            Value of the `attr` nodes should be selected by
        attr: str, default: 'type'
            Attribute key which is 'type' by default

        Returns
        -------
        list
            A list containing nodes elements that match the given attribute
            value
        """

        # get all nodes that have the attribute 'type' set
        nodes_attributes = nx.get_node_attributes(self, attr)

        # extract nodes where 'type' == attr_val
        nodes = [k for k, v in nodes_attributes.items() if v == attr_val]

        return nodes

    def graph_edges(self):
        """ Returns a generator for iterating over graph edges

        The edge of a graph is described by the two adjacent node and the branch
        object itself. Whereas the branch object is used to hold all relevant
        power system parameters.

        Note
        ----
        There are generator functions for nodes (`Graph.nodes()`) and edges
        (`Graph.edges()`) in NetworkX but unlike graph nodes, which can be
        represented by objects, branch objects can only be accessed by using an
        edge attribute ('branch' is used here)

        To make access to attributes of the branch objects simpler and more
        intuitive for the user, this generator yields a dictionary for each edge
        that contains information about adjacent nodes and the branch object.

        Note, the construction of the dictionary highly depends on the structure
        of the in-going tuple (which is defined by the needs of networkX). If
        this changes, the code will break.

        Copied from https://github.com/openego/dingo/blob/
        ee237e37d4c228081e1e246d7e6d0d431c6dda9e/dingo/core/network/__init__.py
        """

        # get edges with attributes
        edges = nx.get_edge_attributes(self, 'line').items()

        # sort them according to connected nodes
        edges_sorted = sorted(list(edges), key=lambda _: repr(_[0]))

        for edge in edges_sorted:
            yield {'adj_nodes': edge[0], 'line': edge[1]}

