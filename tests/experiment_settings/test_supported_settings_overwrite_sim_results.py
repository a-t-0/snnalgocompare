"""Verifies the Supported_settings object catches invalid overwrite_sim_results
specifications."""
# pylint: disable=R0801
import copy
import unittest

from src.experiment_settings.Supported_settings import Supported_settings
from src.experiment_settings.verify_supported_settings import (
    verify_configuration_settings,
)
from tests.experiment_settings.test_supported_settings_iteration import (
    adap_sets,
    rad_sets,
    supp_sets,
    with_adaptation_with_radiation,
)


class Test_overwrite_sim_results_settings(unittest.TestCase):
    """Tests whether the verify_configuration_settings_types function catches
    invalid overwrite_sim_results settings.."""

    # Initialize test object
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.supp_sets = Supported_settings()
        self.valid_overwrite_sim_results = self.supp_sets.overwrite_sim_results

        self.invalid_overwrite_sim_results_value = {
            "overwrite_sim_results": "invalid value of type string iso list of"
            + " floats",
        }

        self.supp_sets = supp_sets
        self.adap_sets = adap_sets
        self.rad_sets = rad_sets
        self.with_adaptation_with_radiation = with_adaptation_with_radiation

    def test_overwrite_sim_results_is_none(self):
        """Verifies an error is thrown if configuration settings do not contain
        m."""

        with self.assertRaises(Exception) as context:
            # Configuration Settings of type None throw error.
            verify_configuration_settings(
                self.supp_sets, None, has_unique_id=False
            )

        self.assertEqual(
            "Error, the experiment_config is of type:"
            + f"{type(None)}, yet it was expected to be of"
            + " type dict.",
            str(context.exception),
        )

    def test_catch_invalid_overwrite_sim_results_type(self):
        """."""

        with self.assertRaises(Exception) as context:
            # overwrite_sim_results dictionary of type None throws error.
            verify_configuration_settings(
                self.supp_sets, "string_instead_of_dict", has_unique_id=False
            )
        self.assertEqual(
            "Error, the experiment_config is of type:"
            + f'{type("")}, yet it was expected to be of'
            + " type dict.",
            str(context.exception),
        )

    def test_catch_empty_overwrite_sim_results_value(self):
        """."""
        # Create deepcopy of configuration settings.
        config_settings = copy.deepcopy(self.with_adaptation_with_radiation)
        # Set negative value of overwrite_sim_results in copy.
        config_settings["overwrite_sim_results"] = None

        with self.assertRaises(Exception) as context:
            verify_configuration_settings(
                self.supp_sets, config_settings, has_unique_id=False
            )

        self.assertEqual(
            "Error, expected type:<class 'bool'>, yet it was:"
            + "<class 'NoneType'>",
            str(context.exception),
        )

    def test_returns_valid_m(self):
        """Verifies a valid overwrite_sim_results is returned."""
        returned_dict = verify_configuration_settings(
            self.supp_sets,
            self.with_adaptation_with_radiation,
            has_unique_id=False,
        )
        self.assertIsInstance(returned_dict, dict)

    def test_empty_overwrite_sim_results(self):
        """Verifies an exception is thrown if an empty overwrite_sim_results
        dict is thrown."""

        # Create deepcopy of configuration settings.
        config_settings = copy.deepcopy(self.with_adaptation_with_radiation)
        # Remove key and value of m.

        config_settings.pop("overwrite_sim_results")

        with self.assertRaises(Exception) as context:
            verify_configuration_settings(
                self.supp_sets, config_settings, has_unique_id=False
            )

        self.assertEqual(
            "'overwrite_sim_results'",
            str(context.exception),
        )
