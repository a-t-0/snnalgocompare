# -*- coding: utf-8 -*-
"""Runs a converted networkx graph without the Lava platform.

First verifies the graph represents a connected and valid SNN, with all
required neuron and synapse properties specified. Then loops through the
network to simulate it, one neuron at a time.
"""

# Import external libraries.
import networkx as nx

# Import local project functions and classes.
from src.verify_graph_is_snn import verify_networkx_snn_spec

from .LIF_neuron import LIF_neuron


def simulate_snn_on_networkx(G: nx.DiGraph, duration: int) -> None:
    """

    :param G: nx.DiGraph:
    :param duration: int:

    """
    # Verify the graph represents a connected and valid SNN, with all required
    # neuron and synapse properties specified.
    verify_networkx_snn_spec(G)

    # Create LIF neurons in networkx graph.
    generate_lif_neurons(G)

    # Create synapses between neurons in networkx graph edges.
    generate_lif_synapses(G)

    # Initialise the nodes at time t=0 (with a_in=0).
    initialise_a_in_is_zero_at_t_is_1(G)

    # The simulation is ran for t timesteps on a Loihi emulation.
    for _ in range(duration):
        run_simulation_with_networkx_for_1_timestep(G)


def generate_lif_neurons(G: nx.DiGraph) -> None:
    """

    :param G: nx.DiGraph:

    """
    for node in G.nodes:
        G.nodes[node]["nx_LIF"] = LIF_neuron(
            name=node,
            bias=G.nodes[node]["nx_LIF"].bias.get(),
            du=G.nodes[node]["nx_LIF"].du.get(),
            dv=G.nodes[node]["nx_LIF"].dv.get(),
            vth=G.nodes[node]["nx_LIF"].vth.get(),
        )


def generate_lif_synapses(G: nx.DiGraph) -> None:
    """

    :param G: nx.DiGraph:

    """
    return G


def run_snn_on_networkx(G: nx.DiGraph, t: int) -> None:
    """Runs the simulation for t timesteps using networkx, not lava."""
    for _ in range(t):
        run_simulation_with_networkx_for_1_timestep(G)


def run_simulation_with_networkx_for_1_timestep(G: nx.DiGraph) -> None:
    """Runs the networkx simulation of the network for 1 timestep. The results
    of the simulation are stored in the G.nodes network.

    :param G: nx.DiGraph:
    """

    # Compute for each node whether it spikes based on a_in, starting at t=1.
    for node in G.nodes:
        nx_lif = G.nodes[node]["nx_LIF"]
        spikes = nx_lif.simulate_neuron_one_timestep(nx_lif.a_in)
        if spikes:
            # Propagate the output spike to the connected receiving neurons.
            for neighbour in nx.all_neighbors(G, node):

                # Check if the outgoing edge is exists and is directed.
                if G.has_edge(node, neighbour):

                    # Compute synaptic weight.
                    weight = G.edges[(node, neighbour)]["weight"]

                    # Add input signal to connected receiving neuron.
                    G.nodes[neighbour]["nx_LIF"].a_in_next += 1 * weight

    # After all inputs have been computed, store a_in_next values for next
    # round into a_in of the current round to prepare for the nextsimulation
    # step.
    for node in G.nodes:
        nx_lif = G.nodes[node]["nx_LIF"]
        nx_lif.a_in = nx_lif.a_in_next


def initialise_a_in_is_zero_at_t_is_1(G: nx.DiGraph) -> None:
    """

    :param G: nx.DiGraph:

    """
    for node in G.nodes:
        G.nodes[node]["nx_LIF"].a_in = 0
        # G.nodes[node]["a_in"] = 0
