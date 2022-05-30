# -*- coding: utf-8 -*-
"""Verifies the graph represents a connected and valid SNN, with all required
neuron and synapse properties specified."""

# Import the networkx module.
import networkx as nx


def verify_networkx_snn_spec(G: nx.DiGraph) -> None:
    """

    :param G: nx.DiGraph:

    """
    for node in G.nodes:
        print(f"node:{node}")
        print(f"node:{G.nodes[node]}")
        verify_neuron_properties_are_specified(G.nodes[node])

    # TODO: verify synapse properties
    for edge in G.edges:
        assert_synapse_properties_are_specified(G, edge)


def verify_neuron_properties_are_specified(node: nx.DiGraph.nodes) -> None:
    """

    :param node: nx.DiGraph.nodes:

    """
    if not isinstance(node["nx_LIF"].bias.get(), float):
        raise Exception("Bias is not a float.")
    if not isinstance(node["nx_LIF"].du.get(), float):
        raise Exception("du is not a float.")
    if not isinstance(node["nx_LIF"].dv.get(), float):
        raise Exception("dv is not a float.")
    if not isinstance(node["nx_LIF"].vth.get(), float):
        raise Exception("vth is not a float.")


def assert_synaptic_edgeweight_type_is_correct(edge: nx.DiGraph.edges) -> None:
    """

    :param edge: nx.DiGraph.edges:

    """
    if not isinstance(edge["w"], float):
        raise Exception(f"Weight of edge {edge} is not a" + " float.")


def assert_synapse_properties_are_specified(G, edge):
    """

    :param G:
    :param edge:

    """
    if not check_if_synapse_properties_are_specified(G, edge):
        raise Exception(
            f"Not all synapse properties of edge: {edge} are"
            + " specified. It only contains attributes:"
            + f"{get_synapse_property_names(G,edge)}"
        )


def check_if_synapse_properties_are_specified(G, edge):
    """

    :param G:
    :param edge:

    """
    synapse_property_names = get_synapse_property_names(G, edge)
    if "weight" in synapse_property_names:
        # if 'delay' in synapse_property_names:
        # TODO: implement delay using a chain of neurons in series since this
        # is not yet supported by lava-nc.

        return True
    return False


def get_synapse_property_names(G, edge):
    """

    :param G:
    :param edge:

    """
    return G.edges[edge].keys()
