import re

import pytest

from openscm.errors import NotAnScmParameterError
from openscm.parameters import ParameterType
from openscm.timeseries_converter import InterpolationType, create_time_points


class _AdapterTester:
    """
    Base class for adapter testing.

    At minimum, a new adapter should define a subclass of this class called,
    ``AdapterXTester`` which has ``tadapter`` set to the adapter to be tested. This
    ensures that the new adapter is subject to all of OpenSCM's minimum requirements
    whilst giving authors the ability to tweak the tests as necessary for their specific
    adapter.
    """

    tadapter = None
    """
    Adapter to test
    """

    def test_initialize(self, test_adapter):
        test_adapter._initialize_model()

    def test_shutdown(self, test_adapter):
        """
        Test the adapter can be shutdown.

        Extra tests can be adapted depending on what the adapter should actually
        do on shutdown.
        """
        del test_adapter

    def test_initialize_model_input(self, test_adapter, test_drivers):
        """
        Test that initalizing model input does as intended.
        """
        assert not test_adapter._initialized
        # TODO test for missing but mandatory parameter
        sst = test_drivers["start_stop_time"]
        test_adapter.initialize_model_input(sst.start_time, sst.stop_time)
        assert test_adapter._initialized

    def test_initialize_model_input_non_model_parameter(
        self, test_adapter, test_drivers
    ):
        tname = ("junk",)
        test_adapter._parameters.get_writable_scalar_view(tname, ("World",), "K").set(4)
        sst = test_drivers["start_stop_time"]
        test_adapter.initialize_model_input(sst.start_time, sst.stop_time)
        # TODO test that "junk" has not been used

    def test_initialize_run_parameters(self, test_adapter):
        """
        Test that initalizing run parameters does as intended.
        """
        assert not test_adapter._initialized
        # TODO see test_initialize_model_input
        test_adapter.initialize_run_parameters()
        assert test_adapter._initialized
        assert (
            test_adapter._parameters.get_scalar_view("ecs", ("World",), "K").get() == 3
        )
        assert (
            test_adapter._parameters.get_scalar_view(
                ("rf2xco2",), ("World",), "W / m^2"
            ).get()
            == 4
        )

    def test_initialize_run_parameters_non_model_parameter(self, test_adapter):
        tname = ("junk",)
        test_adapter._parameters.get_writable_scalar_view(tname, ("World",), "K").set(4)
        error_msg = re.escape(
            "{} is not a {} parameter".format(tname[0], self.tadapter.__name__)
        )
        with pytest.raises(NotAnScmParameterError, match=error_msg):
            test_adapter.initialize_run_parameters()

    def test_run(self, test_adapter, test_drivers):
        # TODO: work out how to more easily append a view to a parameterset
        # so we don't have to duplicate conftest
        timestep_count = 500
        sst = test_drivers["start_stop_time"]

        time_points_for_averages = create_time_points(
            sst.start_time, 31556926, timestep_count, ParameterType.AVERAGE_TIMESERIES
        )

        test_model_inputs = test_drivers["inputs"]
        iview = test_model_inputs.get_timeseries_view(
            ("Emissions", "CO2"),
            ("World",),
            "GtCO2/yr",
            time_points_for_averages,
            ParameterType.AVERAGE_TIMESERIES,
            InterpolationType.LINEAR,
        )

        test_adapter._parameters.get_writable_timeseries_view(
            ("Emissions", "CO2"),
            ("World",),
            "GtCO2/yr",
            time_points_for_averages,
            ParameterType.AVERAGE_TIMESERIES,
            InterpolationType.LINEAR,
        ).set(iview.get())

        test_adapter.initialize_model_input(sst.start_time, sst.stop_time)

        test_adapter.initialize_run_parameters()
        test_adapter.reset()
        test_adapter.run()

    def test_step(self, test_adapter, test_drivers):
        # TODO: work out how to more easily append a view to a parameterset
        # so we don't have to duplicate conftest
        timestep_count = 500
        sst = test_drivers["start_stop_time"]

        time_points_for_averages = create_time_points(
            sst.start_time, 31556926, timestep_count, ParameterType.AVERAGE_TIMESERIES
        )

        test_model_inputs = test_drivers["inputs"]
        iview = test_model_inputs.get_timeseries_view(
            ("Emissions", "CO2"),
            ("World",),
            "GtCO2/yr",
            time_points_for_averages,
            ParameterType.AVERAGE_TIMESERIES,
            InterpolationType.LINEAR,
        )

        test_adapter._parameters.get_writable_timeseries_view(
            ("Emissions", "CO2"),
            ("World",),
            "GtCO2/yr",
            time_points_for_averages,
            ParameterType.AVERAGE_TIMESERIES,
            InterpolationType.LINEAR,
        ).set(iview.get())

        test_adapter.initialize_model_input(sst.start_time, sst.stop_time)
        test_adapter.initialize_run_parameters()
        test_adapter.reset()
        assert test_adapter._current_time == sst.start_time
        try:
            new_time = test_adapter.step()
            assert new_time > sst.start_time
        except NotImplementedError:
            pass
