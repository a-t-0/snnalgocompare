"""Contains a single setting of the experiment configuration settings.

(The values of the settings may vary, yet the types should be the same.)
"""


from src.experiment_settings.Adaptation_Rad_settings import (
    Adaptation_settings,
    Radiation_settings,
)
from src.experiment_settings.Supported_experiment_settings import (
    Supported_experiment_settings,
)
from src.experiment_settings.verify_experiment_settings import (
    verify_adap_and_rad_settings,
    verify_experiment_config,
    verify_has_unique_id,
)


class Experiment_runner:
    """Stores the configuration of a single run."""

    # pylint: disable=R0903

    def __init__(
        self, config_settings: dict, export: bool, show: bool
    ) -> None:

        # Store the experiment configuration settings.
        self.config_settings = config_settings

        # Load the ranges of supported settings.
        self.supp_sets = Supported_experiment_settings()

        # Verify the experiment config_settings are complete and valid.
        verify_experiment_config(
            self.supp_sets, config_settings, has_unique_id=False
        )

        # If the experiment config_settings does not contain a hash-code,
        # create the unique hash code for this configuration.
        if not self.supp_sets.has_unique_config_id(self.config_settings):
            self.supp_sets.append_unique_config_id(self, self.config_settings)

        # Verify the unique hash code for this configuration is valid.
        verify_has_unique_id(self.config_settings)

        # Append the export and show arguments.
        self.config_settings["export"] = export
        self.config_settings["show"] = show

        # determine_what_to_run

        # TODO: Perform run accordingly.
        # __perform_run

    def determine_what_to_run(self):
        """Scans for existing output and then combines the run configuration
        settings to determine what still should be computed."""
        # Determine which of the 4 stages have been performed.

        # Check if the run is already performed without exporting.

        # Check if the run is already performed with exporting.

    # pylint: disable=W0238
    def __perform_run(self):
        """Private method that runs the experiment.

        The 2 underscores indicate it is private. This method executes
        the run in the way the processed configuration settings specify.
        """


def example_config_settings():
    """Creates example experiment configuration settings."""
    # Create prerequisites
    supp_sets = Supported_experiment_settings()
    adap_sets = Adaptation_settings()
    rad_sets = Radiation_settings()

    # Create the experiment configuration settings for a run with adaptation
    # and with radiation.
    with_adaptation_with_radiation = {
        "algorithms": {
            "MDSA": {
                "m_vals": list(range(0, 1, 1)),
            }
        },
        "adaptation": verify_adap_and_rad_settings(
            supp_sets, adap_sets.with_adaptation, "adaptation"
        ),
        "iterations": list(range(0, 3, 1)),
        "min_max_graphs": 1,
        "max_max_graphs": 15,
        "min_graph_size": 3,
        "max_graph_size": 20,
        "overwrite_sim_results": True,
        "overwrite_visualisation": True,
        "radiation": verify_adap_and_rad_settings(
            supp_sets, rad_sets.with_radiation, "radiation"
        ),
        "size_and_max_graphs": [(3, 15), (4, 15)],
        "simulators": ["nx"],
    }
    return with_adaptation_with_radiation
