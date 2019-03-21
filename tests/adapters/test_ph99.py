import datetime

import numpy as np
import pytest
from base import _AdapterTester

from openscm.adapters.ph99 import PH99
from openscm.parameters import ParameterType
from openscm.utils import convert_datetime_to_openscm_time


class TestPH99Adapter(_AdapterTester):
    tadapter = PH99

    def test_initialize(self, test_adapter):
        with pytest.raises(AttributeError):
            test_adapter.model
        super().test_initialize(test_adapter)
        assert test_adapter.model

    def test_initialize_run_parameters(self, test_adapter):
        super().test_initialize_run_parameters(test_adapter)

        tc1 = 3.8
        test_adapter._parameters.get_writable_scalar_view("c1", ("World",), "ppb").set(
            tc1 * 1000
        )
        test_adapter.initialize_run_parameters()
        assert (
            test_adapter._parameters.get_scalar_view(("c1",), ("World",), "ppm").get()
            == tc1
        )

    def test_run(self, test_adapter, test_drivers):
        super().test_run(test_adapter, test_drivers)

        emms_2017 = test_adapter._output.get_timeseries_view(
            ("Emissions", "CO2"),
            "World",
            "GtC / yr",
            np.array(
                [
                    convert_datetime_to_openscm_time(datetime.datetime(2017, 1, 1)),
                    convert_datetime_to_openscm_time(datetime.datetime(2018, 1, 1)),
                ]
            ),
            ParameterType.AVERAGE_TIMESERIES,
        ).get()
        assert emms_2017[0] == -0.378101689838863  # could be wrong, need to check...

        temp_2017_2018 = test_adapter._output.get_timeseries_view(
            ("Surface Temperature"),
            "World",
            "K",
            np.array(
                [
                    convert_datetime_to_openscm_time(datetime.datetime(2017, 1, 1)),
                    convert_datetime_to_openscm_time(datetime.datetime(2018, 1, 1)),
                ]
            ),
            ParameterType.POINT_TIMESERIES,
        ).get()
        np.testing.assert_allclose(
            temp_2017_2018, np.array([-0.0008942013640017765, -0.00202055345682164])
        )
