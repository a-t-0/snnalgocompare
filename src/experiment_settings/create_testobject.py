"""Creates test object."""


from lava.proc.monitor.process import Monitor

from src.helper import fill_dictionary

# from src.networkx_to_snn import convert_networkx_graph_to_snn_with_one_neuron


def get_degree_receiver_previous_property_dicts(
    test_object, degree_receiver_neurons
):
    """

    :param test_object: Object containing test settings.
    :param degree_receiver_neurons: The neuron objects from the degree_receiver
    position. Type unknown.

    """
    degree_receiver_previous_us = {}
    degree_receiver_previous_vs = {}
    degree_receiver_previous_has_spiked = {}
    (
        degree_receiver_previous_us,
        degree_receiver_previous_vs,
        degree_receiver_previous_has_spiked,
        _,
    ) = fill_dictionary(
        test_object.neuron_dict,
        degree_receiver_neurons,
        degree_receiver_previous_us,
        degree_receiver_previous_vs,
        previous_has_spiked=degree_receiver_previous_has_spiked,
    )

    return (
        degree_receiver_previous_has_spiked,
        degree_receiver_previous_us,
        degree_receiver_previous_vs,
    )


def get_selector_previous_property_dicts(test_object, selector_neurons):
    """

    :param test_object: Object containing test settings.
    :param selector_neurons:
    :param selector_neurons: Neuron objects at the selector position.
    Type unknown.

    """
    selector_previous_a_in = {}
    selector_previous_us = {}
    selector_previous_vs = {}
    (
        selector_previous_a_in,
        selector_previous_us,
        selector_previous_vs,
        _,
    ) = fill_dictionary(
        test_object.neuron_dict,
        selector_neurons,
        selector_previous_us,
        selector_previous_vs,
        selector_previous_a_in,
    )
    return selector_previous_a_in, selector_previous_us, selector_previous_vs


def get_counter_previous_property_dicts(test_object, counter_neurons):
    """

    :param test_object: Object containing test settings.
    :param counter_neurons:
    :param counter_neurons: Neuron objects at the counter position.
    Type unknown.

    """
    counter_previous_a_in = {}
    counter_previous_us = {}
    counter_previous_vs = {}
    (
        counter_previous_a_in,
        counter_previous_us,
        counter_previous_vs,
        _,
    ) = fill_dictionary(
        test_object.neuron_dict,
        counter_neurons,
        counter_previous_us,
        counter_previous_vs,
        counter_previous_a_in,
    )
    return counter_previous_a_in, counter_previous_us, counter_previous_vs


def add_monitor_to_dict(neuron, monitor_dict, sim_time):
    """Creates a dictionary monitors that monitor the outgoing spikes of LIF
    neurons.

    :param neuron: Lava neuron object.
    :param monitor_dict: Dictionary of neurons whose spikes are monitored.
    :param sim_time: Nr. of timesteps for which the experiment is ran.
    :param monitor_dict: Dictionary of neurons whose spikes are monitored.
    """
    if isinstance(neuron, str):
        monitor = Monitor()
        monitor.probe(neuron.out_ports.s_out, sim_time)
        monitor_dict[neuron] = monitor
    return monitor_dict


class Selector_neuron:
    """Creates expected properties of the selector neuron."""

    # pylint: disable=R0903
    def __init__(self):
        self.first_name = "selector_0"
        self.bias = 5
        self.du = 0
        self.dv = 1
        self.vth = 4


class Spike_once_neuron:
    """Creates expected properties of the spike_once neuron."""

    # pylint: disable=R0903
    def __init__(self):
        self.first_name = "spike_once_0"
        self.bias = 2
        self.du = 0
        self.dv = 0
        self.vth = 1


class Rand_neuron:
    """Creates expected properties of the rand neuron."""

    # pylint: disable=R0903
    def __init__(self):
        self.first_name = "rand_0"
        self.bias = 2
        self.du = 0
        self.dv = 0
        self.vth = 1


class Counter_neuron:
    """Creates expected properties of the counter neuron."""

    # pylint: disable=R0903
    def __init__(self):
        self.first_name = "counter_0"
        self.bias = 0
        self.du = 0
        self.dv = 1
        self.vth = 0


class Degree_receiver:
    """Creates expected properties of the spike_once neuron."""

    # pylint: disable=R0903
    def __init__(self):
        self.first_name = "spike_once_0"
        self.bias = 0
        self.du = 0
        self.dv = 1
        self.vth = 1
