"""Exports the following structure to an output file for simsnn:

/stage_2/
    snn_algo_graph: spikes, du, dv.
    adapted_snn_algo_graph: spikes, du, dv.
    rad_snn_algo_graph: spikes, du, dv.
    rad_adapted_snn_algo_graph: spikes, du, dv.
"""
import json
from pathlib import Path
from pprint import pprint
from typing import Dict, List, Union

import networkx as nx
import numpy as np
from simsnn.core.simulators import Simulator
from typeguard import typechecked

from snncompare.export_results.output_stage1_configs_and_input_graph import (
    Radiation_output_data,
    get_radiation_names_filepath_and_exists,
    get_rand_nrs_and_hash,
)
from snncompare.import_results.helper import simsnn_files_exists_and_get_path
from snncompare.import_results.read_json import load_json_file_into_dict
from snncompare.run_config.Run_config import Run_config


@typechecked
def output_stage_2_snns(
    *,
    run_config: Run_config,
    graphs_dict: Dict[str, Union[nx.Graph, nx.DiGraph, Simulator]],
) -> None:
    """Exports results dict to a json file."""
    stage_index: int = 2

    for with_adaptation in [False, True]:
        for with_radiation in [False, True]:
            # pylint:disable=R0801
            if with_radiation:
                radiation_output_data: Radiation_output_data = (
                    get_radiation_names_filepath_and_exists(
                        graphs_dict=graphs_dict,
                        run_config=run_config,
                        stage_index=2,
                        with_adaptation=with_adaptation,
                    )
                )
                rad_affected_neurons_hash: Union[
                    None, str
                ] = radiation_output_data.rad_affected_neurons_hash
            else:
                rad_affected_neurons_hash = None

        _, rand_nrs_hash = get_rand_nrs_and_hash(
            input_graph=graphs_dict["input_graph"]
        )

        # pylint:disable=R0801
        simsnn_exists, simsnn_filepath = simsnn_files_exists_and_get_path(
            output_category="snns",
            input_graph=graphs_dict["input_graph"],
            run_config=run_config,
            with_adaptation=with_adaptation,
            stage_index=2,
            rad_affected_neurons_hash=rad_affected_neurons_hash,
            rand_nrs_hash=rand_nrs_hash,
        )
        if simsnn_exists:
            raise FileExistsError(
                f"Error, {simsnn_exists} already exists while outputting: "
                + f"stage{stage_index}"
            )
        output_snn_graph(
            output_filepath=simsnn_filepath,
            snn_graph=get_desired_snn_graph(
                graphs_dict=graphs_dict,
                with_adaptation=with_adaptation,
                with_radiation=with_radiation,
            ),
        )


@typechecked
def get_desired_snn_graph(
    *,
    graphs_dict: Dict[str, Union[nx.Graph, nx.DiGraph, Simulator]],
    with_adaptation: bool,
    with_radiation: bool,
) -> Union[nx.DiGraph, Simulator]:
    """Outputs the simsnn neuron behaviour over time."""
    if with_adaptation:
        if with_radiation:
            snn_graph = graphs_dict["rad_adapted_snn_graph"]
        else:
            snn_graph = graphs_dict["adapted_snn_graph"]
    else:
        if with_radiation:
            snn_graph = graphs_dict["rad_snn_algo_graph"]
        else:
            snn_graph = graphs_dict["snn_algo_graph"]

    return snn_graph


@typechecked
def output_snn_graph(
    *,
    output_filepath: str,
    snn_graph: Union[nx.DiGraph, Simulator],
) -> None:
    """Outputs the simsnn neuron behaviour over time."""
    # TODO: change this into an object with: name and a list of parameters
    # instead.

    if isinstance(snn_graph, Simulator):
        v: List[float] = snn_graph.multimeter.V.tolist()
        i: List[float] = snn_graph.multimeter.I.tolist()
        spikes: List[bool] = snn_graph.raster.spikes.tolist()
        neuron_dict: Dict = {"V": v, "I": i, "spikes": spikes}
        with open(output_filepath, "w", encoding="utf-8") as fp:
            json.dump(
                neuron_dict,
                fp,
                indent=4,
                sort_keys=True,
            )
            fp.close()
        # Verify the file exists.
        if not Path(output_filepath).is_file():
            raise FileExistsError(
                f"Error, filepath:{output_filepath} was not created."
            )

        loaded_snn: Dict = load_json_file_into_dict(
            json_filepath=output_filepath
        )

        for key, value in loaded_snn.items():
            loaded_snn[key] = np.array(value)
            if key == "spikes":
                snn_data_obj = snn_graph.raster
            else:
                snn_data_obj = snn_graph.multimeter

            if not np.array_equal(loaded_snn[key], getattr(snn_data_obj, key)):
                pprint(loaded_snn[key])
                pprint(getattr(snn_graph.multimeter, key))
                raise ValueError(
                    f"Error, for:{key} loaded different value from json than "
                    + f"was found in snn. At:{output_filepath}"
                )