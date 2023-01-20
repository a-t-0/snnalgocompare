""""Stores the run config Dict type."""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Dict

from snnadaptation.redundancy.verify_redundancy_settings import (
    verify_redundancy_settings_for_exp_config,
)
from snnalgorithms.get_alg_configs import get_algo_configs
from snnalgorithms.sparse.MDSA.alg_params import MDSA
from snnalgorithms.verify_algos import verify_algos_in_exp_config
from typeguard import typechecked


# pylint: disable=R0902
# pylint: disable=R0903
class Exp_config:
    """Stores the exp_configriment settings object."""

    # pylint: disable=R0913
    # pylint: disable=R0914
    @typechecked
    def __init__(
        self,
        adaptations: None | dict[str, int] | dict,
        algorithms: dict[str, list[dict[str, int]]],
        max_graph_size: int,
        max_max_graphs: int,
        min_graph_size: int,
        min_max_graphs: int,
        neuron_models: list,
        recreate_s1: bool,
        recreate_s2: bool,
        overwrite_images_only: bool,
        recreate_s4: bool,
        radiations: dict,
        seeds: list[int],
        simulators: list,
        size_and_max_graphs: list,
        synaptic_models: list,
        export_images: bool | None = False,
        export_types: list[str] | None = None,
        unique_id: str | None = None,
    ):
        """Stores run configuration settings for the exp_configriment."""

        # Required properties
        self.adaptations: None | dict[str, int] = adaptations
        self.algorithms: dict[str, list[dict[str, int]]] = algorithms
        self.max_graph_size: int = max_graph_size
        self.max_max_graphs: int = max_max_graphs
        self.min_graph_size: int = min_graph_size
        self.min_max_graphs: int = min_max_graphs
        self.neuron_models: list = neuron_models
        self.recreate_s1: bool = recreate_s1
        self.recreate_s2: bool = recreate_s2
        self.overwrite_images_only: bool = overwrite_images_only
        self.recreate_s4: bool = recreate_s4
        self.radiations: dict = radiations
        self.seeds: list[int] = seeds
        self.simulators: list = simulators
        self.size_and_max_graphs: list = size_and_max_graphs
        self.synaptic_models: list = synaptic_models

        # Optional properties
        self.export_images: bool = bool(export_images)
        if self.export_images:
            if export_types is not None:
                self.export_types: list[str] = export_types

        if unique_id is not None:
            self.unique_id: str = unique_id

        # Verify run config object.
        supp_exp_config = Supported_experiment_settings()
        verify_exp_config(
            supp_exp_config=supp_exp_config,
            exp_config=self,
            has_unique_id=False,
            allow_optional=False,
        )


@typechecked
def remove_optional_args_exp_config(
    supported_experiment_settings: Supported_experiment_settings,
    copied_exp_config: Exp_config,
) -> Exp_config:
    """removes the optional arguments from a run config."""
    non_unique_attributes = [
        "recreate_s1",
        "recreate_s2",
        "overwrite_images_only",
        "recreate_s4",
        "export_images",
        "export_types",
        "unique_id",
    ]
    for attribute_name in non_unique_attributes:
        # TODO: set to default value instead
        setattr(copied_exp_config, attribute_name, None)
    verify_exp_config(
        supp_exp_config=supported_experiment_settings,
        exp_config=copied_exp_config,
        has_unique_id=False,
        allow_optional=False,
    )
    return copied_exp_config


# pylint: disable=R0902
class Supported_experiment_settings:
    """Contains the settings that are supported for the exp_config.

    (The values of the settings may vary, yet the values of an
    experiment setting should be within the ranges specified in this
    file, and the setting types should be identical.)
    """

    @typechecked
    def __init__(
        self,
    ) -> None:

        self.seed = 5

        # Create dictionary with algorithm name as key, and algorithm settings
        # object as value.
        mdsa_min = MDSA([]).min_m_vals
        mdsa_max = MDSA([]).max_m_vals
        self.algorithms = get_algo_configs(
            MDSA(list(range(mdsa_min, mdsa_max, 1))).__dict__
        )

        # Specify the maximum number of: (maximum number of graphs per run
        # size).
        self.min_max_graphs = 1
        self.max_max_graphs = 15
        # verify_min_max(self.min_max_graphs, self.max_max_graphs)

        # Specify the maximum graph size.
        self.min_graph_size = 3
        self.max_graph_size = 20
        # verify_min_max(self.min_graph_size, self.max_graph_size)

        # The size of the graph and the maximum number of used graphs of that
        # size.
        self.size_and_max_graphs = [
            (self.min_graph_size, self.max_max_graphs),
            (5, 4),  # Means: get 4 graphs of size 5 for experiment.
            (self.max_graph_size, self.max_max_graphs),
        ]

        # Overwrite the simulation results or not.
        self.recreate_s4 = True
        # Overwrite the visualisation of the SNN behaviour or not.
        self.overwrite_images_only = True

        self.seeds = list(range(0, 1000))

        # The backend/type of simulator that is used.
        self.simulators = ["nx", "lava"]

        # Generate the supported adaptation settings.
        self.specify_supported_adaptation_settings()

        # Generate the supported radiations settings.
        self.specify_supported_radiations_settings()

        # Specify the supported image export file extensions.
        self.export_types = ["pdf", "png"]

    @typechecked
    def specify_supported_radiations_settings(self) -> None:
        """Specifies types of supported radiations settings. Some settings
        consist of a list of tuples, with the probability of a change
        occurring, followed by the average magnitude of the change.

        Others only contain a list of floats which represent the
        probability of radiations induced change occurring.
        """
        # List of tuples with x=probabiltity of change, y=average value change
        # in synaptic weights.
        self.delta_synaptic_w = [
            (0.01, 0.5),
            (0.05, 0.4),
            (0.1, 0.3),
            (0.2, 0.2),
            (0.25, 0.1),
        ]

        # List of tuples with x=probabiltity of change, y=average value change
        # in neuronal threshold.
        self.delta_vth = [
            (0.01, 0.5),
            (0.05, 0.4),
            (0.1, 0.3),
            (0.2, 0.2),
            (0.25, 0.1),
        ]

        # Create a supported radiations setting example.
        self.radiations = {
            # No radiations
            "None": [],
            # radiations effects are transient, they last for 1 or 10
            # simulation steps. If transient is 0., the changes are permanent.
            "transient": [0.0, 1.0, 10.0],
            # List of probabilities of a neuron dying due to radiations.
            "neuron_death": [
                0.01,
                0.05,
                0.1,
                0.2,
                0.25,
            ],
            # List of probabilities of a synapse dying due to radiations.
            "synaptic_death": [
                0.01,
                0.05,
                0.1,
                0.2,
                0.25,
            ],
            # List of: (probability of synaptic weight change, and the average
            # factor with which it changes due to radiations).
            "delta_synaptic_w": self.delta_synaptic_w,
            # List of: (probability of neuron threshold change, and the average
            # factor with which it changes due to radiations).
            "delta_vth": self.delta_vth,
        }

    @typechecked
    def specify_supported_adaptation_settings(self) -> None:
        """Specifies all the supported types of adaptation settings."""

        # Specify the (to be) supported adaptation types.
        self.adaptations = {
            "None": [],
            "redundancy": [
                1.0,
            ],  # Create 1 redundant neuron per neuron.
            "population": [
                10.0
            ],  # Create a population of 10 neurons to represent a
            # single neuron.
            "rate_coding": [
                5.0
            ],  # Multiply firing frequency with 5 to limit spike decay
            # impact.
        }

    @typechecked
    def has_unique_config_id(self, some_config: Exp_config) -> bool:
        """

        :param exp_config:

        """
        if "unique_id" in some_config.__dict__.keys():
            return True
        return False


@typechecked
def append_unique_exp_config_id(
    exp_config: Exp_config,
) -> Exp_config:
    """Checks if an experiment configuration dictionary already has a unique
    identifier, and if not it computes and appends it.

    If it does, throws an error.

    :param exp_config: Exp_config:
    """
    if "unique_id" in exp_config.__dict__.keys():
        raise Exception(
            f"Error, the exp_config:{exp_config}\n"
            + "already contains a unique identifier."
        )

    # Compute a unique code belonging to this particular experiment
    # configuration.
    # TODO: remove optional arguments from config.
    supported_experiment_settings = Supported_experiment_settings()
    exp_config_without_unique_id: Exp_config = remove_optional_args_exp_config(
        supported_experiment_settings=supported_experiment_settings,
        copied_exp_config=copy.deepcopy(exp_config),
    )

    unique_id = str(
        hashlib.sha256(
            json.dumps(exp_config_without_unique_id.__dict__).encode("utf-8")
        ).hexdigest()
    )
    exp_config.unique_id = unique_id
    return exp_config


# pylint: disable=W0613
@typechecked
def verify_exp_config(
    supp_exp_config: Supported_experiment_settings,
    exp_config: Exp_config,
    has_unique_id: bool,
    allow_optional: bool,
) -> None:
    """Verifies the selected experiment configuration settings are valid.

    :param exp_config: param has_unique_id:
    :param has_unique_id: param supp_exp_config:
    :param supp_exp_config:
    """

    verify_exp_config_is_sensible(
        exp_config,
        supp_exp_config,
    )

    # Verify settings are sensible.

    # Verify the algorithms
    verify_algos_in_exp_config(exp_config)

    # Verify settings of type: list and tuple.
    verify_list_setting(supp_exp_config, exp_config.seeds, int, "seeds")

    verify_list_setting(
        supp_exp_config, exp_config.simulators, str, "simulators"
    )
    verify_size_and_max_graphs_settings(
        supp_exp_config, exp_config.size_and_max_graphs
    )

    # Verify settings of type integer.
    verify_integer_settings(
        exp_config.min_max_graphs,
        supp_exp_config.min_max_graphs,
        supp_exp_config.max_max_graphs,
    )
    verify_integer_settings(
        exp_config.max_max_graphs,
        supp_exp_config.min_max_graphs,
        supp_exp_config.max_max_graphs,
    )
    verify_integer_settings(
        exp_config.min_graph_size,
        supp_exp_config.min_graph_size,
        supp_exp_config.max_graph_size,
    )
    verify_integer_settings(
        exp_config.max_graph_size,
        supp_exp_config.min_graph_size,
        supp_exp_config.max_graph_size,
    )

    # Verify a lower bound/min is not larger than a upper bound/max value.
    verify_min_max(
        exp_config.min_graph_size,
        exp_config.max_graph_size,
    )
    verify_min_max(
        exp_config.min_max_graphs,
        exp_config.max_max_graphs,
    )

    # Verify settings of type bool.


def verify_exp_config_is_sensible(
    exp_config: Exp_config,
    supp_exp_config: Supported_experiment_settings,
) -> None:
    """Verifies the experiment configuration does not contain unsensible
    options."""
    # Check that if overwrite_images_only is True, that the experiment
    # configuration actually exports images.
    if exp_config.overwrite_images_only:
        if not exp_config.export_images:
            raise AttributeError(
                "Error, the user asked to overwrite the images without"
                "Telling that the images should be exported."
            )

    if exp_config.export_images:
        if len(exp_config.export_types) < 1:
            raise TypeError(
                "Error, export types not defined whilst wanting to export"
                + " images."
            )
        for export_type in exp_config.export_types:
            if export_type not in supp_exp_config.export_types:
                raise AttributeError(
                    "Error, the user asked to overwrite the images whilst"
                    + "specifying invalid image export extensions: "
                    + f"{export_type}. Expected: "
                    + f"{supp_exp_config.export_types}"
                )


@typechecked
def verify_list_element_types_and_list_len(  # type:ignore[misc]
    list_setting: Any, element_type: type
) -> None:
    """Verifies the types and minimum length of configuration settings that are
    stored with a value of type list.

    :param list_setting: param element_type:
    :param element_type:
    """
    verify_object_type(list_setting, list, element_type=element_type)
    if len(list_setting) < 1:
        raise Exception(
            "Error, list was expected contain at least 1 integer."
            + f" Instead, it has length:{len(list_setting)}"
        )


def verify_list_setting(  # type:ignore[misc]
    supp_exp_config: Supported_experiment_settings,
    setting: Any,
    element_type: type,
    setting_name: str,
) -> None:
    """Verifies the configuration settings that have values of type list, that
    the list has at least 1 element in it, and that its values are within the
    supported range.

    :param setting: param supp_exp_config:
    :param element_type: param setting_name:
    :param supp_exp_config:
    :param setting_name:
    """

    # Check if the configuration setting is a list with length at least 1.
    verify_list_element_types_and_list_len(setting, element_type)

    # Verify the configuration setting list elements are all within the
    # supported range.
    expected_range = get_expected_range(setting_name, supp_exp_config)
    for element in setting:
        if element not in expected_range:
            raise Exception(
                f"Error, {setting_name} was expected to be in range:"
                + f"{expected_range}. Instead, it"
                + f" contains:{element}."
            )


def get_expected_range(
    setting_name: str, supp_exp_config: Supported_experiment_settings
) -> list[int] | list[str]:
    """Returns the ranges as specified in the Supported_experiment_settings
    object for the asked setting.

    :param setting_name: param supp_exp_config:
    :param supp_exp_config:
    """
    if setting_name == "m_val":
        return list(range(MDSA([1]).min_m_vals, MDSA([1]).max_m_vals, 1))
    if setting_name == "simulators":
        return supp_exp_config.simulators
    if setting_name == "seeds":
        return supp_exp_config.seeds

    # TODO: test this is raised.
    raise Exception(f"Error, unsupported parameter requested:{setting_name}")


def verify_size_and_max_graphs_settings(
    supp_exp_config: Supported_experiment_settings,
    size_and_max_graphs_setting: list[tuple[int, int]] | None,
) -> None:
    """Verifies the configuration setting size_and_max_graphs_setting values
    are a list of tuples with at least 1 tuple, and that its values are within
    the supported range.

    :param supp_exp_config:
    :param size_and_max_graphs_setting:
    :param supp_exp_config:
    """
    verify_list_element_types_and_list_len(size_and_max_graphs_setting, tuple)

    # Verify the tuples contain valid values for size and max_graphs.
    if size_and_max_graphs_setting is not None:
        for size_and_max_graphs in size_and_max_graphs_setting:
            size = size_and_max_graphs[0]
            max_graphs = size_and_max_graphs[1]

            verify_integer_settings(
                size,
                supp_exp_config.min_graph_size,
                supp_exp_config.max_graph_size,
            )

            verify_integer_settings(
                max_graphs,
                supp_exp_config.min_max_graphs,
                supp_exp_config.max_max_graphs,
            )


@typechecked
def verify_integer_settings(
    integer_setting: int,
    min_val: int | None = None,
    max_val: int | None = None,
) -> None:
    """Verifies an integer setting is of type integer and that it is within the
    supported minimum and maximum value range..

    :param integer_setting:
    :param min_val:
    :param max_val:
    """
    if (min_val is not None) and (max_val is not None):

        if integer_setting < min_val:
            raise Exception(
                f"Error, setting expected to be at least {min_val}. "
                + f"Instead, it is:{integer_setting}"
            )
        if integer_setting > max_val:
            raise Exception(
                "Error, setting expected to be at most"
                + f" {max_val}. Instead, it is:"
                + f"{integer_setting}"
            )


@typechecked
def verify_min_max(min_val: int, max_val: int) -> None:
    """Verifies a lower bound/minimum value is indeed smaller than an
    upperbound/maximum value.

    Also verifies the values are either of type integer or float.
    """
    if min_val > max_val:
        raise Exception(
            f"Lower bound:{min_val} is larger than upper bound:"
            + f"{max_val}."
        )


# TODO: determine why this can not be typechecked.
def verify_object_type(
    obj: float | list | tuple,
    expected_type: type,
    element_type: type | None = None,
) -> None:
    """Verifies an incoming object has the expected type, and if the object is
    a tuple or list, it also verifies the types of the elements in the tuple or
    list.

    :param obj: param expected_type:
    :param element_type: Default value = None
    :param expected_type:
    """

    # Verify the object type is as expected.
    if not isinstance(obj, expected_type):
        raise Exception(
            f"Error, expected type:{expected_type}, yet it was:{type(obj)}"
            + f" for:{obj}"
        )

    # If object is of type list or tuple, verify the element types.
    if isinstance(obj, (list, tuple)):

        # Verify user passed the expected element types.
        if element_type is None:
            raise Exception("Expected a type to check list element types.")

        # Verify the element types.
        if not all(isinstance(n, element_type) for n in obj):

            # if list(map(type, obj)) != element_type:
            raise Exception(
                f"Error, obj={obj}, its type is:{list(map(type, obj))},"
                + f" expected type:{element_type}"
            )


def verify_adap_and_rad_settings(
    supp_exp_config: Supported_experiment_settings,
    some_dict: dict | str | None,
    check_type: str,
) -> dict:
    """Verifies the settings of adaptations or radiations property are valid.
    Returns a dictionary with the adaptations setting if the settngs are valid.

    :param some_dict: param check_type:
    :param check_type: param supp_exp_config:
    :param supp_exp_config:
    """

    # Load the example settings from the Supported_experiment_settings object.
    if check_type == "adaptations":
        reference_object: dict[  # type:ignore[misc]
            str, Any
        ] = supp_exp_config.adaptations
    elif check_type == "radiations":
        reference_object = supp_exp_config.radiations
    else:
        raise Exception(f"Check type:{check_type} not supported.")

    # Verify object is a dictionary.
    if isinstance(some_dict, Dict):
        if some_dict == {}:
            raise Exception(f"Error, property Dict: {check_type} was empty.")
        for key in some_dict:

            # Verify the keys are within the supported dictionary keys.
            if key not in reference_object:
                raise Exception(
                    f"Error, property.key:{key} is not in the supported "
                    + f"property keys:{reference_object.keys()}."
                )
            # Check if values belonging to key are within supported range.
            if check_type == "adaptations":
                verify_redundancy_settings_for_exp_config(some_dict[key])
            elif check_type == "radiations":
                verify_radiations_values(supp_exp_config, some_dict, key)
        return some_dict
    raise Exception(
        "Error, property is expected to be a Dict, yet"
        + f" it was of type: {type(some_dict)}."
    )


def verify_algorithm_settings(
    supp_exp_config: Supported_experiment_settings,
    some_dict: dict,
    check_type: str,
) -> None:
    """TODO: Verifies the settings of the algorithm are valid."""


def verify_radiations_values(
    supp_exp_config: Supported_experiment_settings, radiations: dict, key: str
) -> None:
    """The configuration settings contain key named: radiations. The value of
    belonging to this key is a dictionary, which also has several keys.

    This method checks whether these radiations dictionary keys, are within
    the supported range of adaptations setting keys. These adaptations
    dictionary keys should each have values of the type list. These list
    elements should have the type float, tuple(float, float) or be empty lists.
    The empty list represents: no radiations is used, signified by the key
    name: "None".

    This method verifies the keys in the adaptations dictionary are within the
    supported range. It also checks if the values of the adaptations dictionary
    keys are a list, and whether all elements in those lists are of type float
    or tuple. If the types are tuple, it also checks whether the values within
    those tuples are of type float.

    :param radiations: Dict:
    :param key: str:
    :param supp_exp_config:
    """
    if not isinstance(
        radiations[key], type(supp_exp_config.radiations[key])
    ) or (not isinstance(radiations[key], list)):

        raise Exception(
            "Error, the radiations value is of type:"
            + f"{type(radiations[key])}, yet it was expected to be"
            + " float or dict."
        )

    # Verify radiations setting types.
    if isinstance(radiations[key], list):
        for setting in radiations[key]:

            # Verify radiations setting can be of type float.
            if isinstance(setting, float):
                # TODO: superfluous check.
                verify_object_type(setting, float, None)
            # Verify radiations setting can be of type tuple.
            elif isinstance(setting, tuple):
                # Verify the radiations setting tuple is of type float,
                # float.
                # TODO: change type((1.0, 2.0)) to the type it is.
                verify_object_type(setting, tuple, type((1.0, 2.0)))

            else:
                # Throw error if the radiations setting is something other
                # than a float or tuple of floats.
                raise Exception(
                    f"Unexpected setting type:{type(setting)} for:"
                    + f" {setting}."
                )
