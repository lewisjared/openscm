from abc import abstractmethod


import pytest


from openscm.adapter import Adapter
from openscm.core import ParameterSet


@pytest.fixture(scope="function")
def test_adapter(request):
    """Get an initialised instance of an the requesting classes ``tadapter`` property.
    """
    try:
        yield request.cls.tadapter(ParameterSet(), ParameterSet())
    except TypeError:
        pytest.skip("{} cannot be instantiated".format(str(request.cls.tadapter)))


@pytest.fixture(scope="function")
def test_config_paraset():
    parameters = ParameterSet()
    parameters.get_writable_scalar_view("ecs", ("World",), "K").set(3)
    parameters.get_writable_scalar_view("rf2xco2", ("World",), "W / m^2").set(4.0)

    yield parameters


@pytest.fixture(scope="function")
def test_drivers_core():
    # doesn't exist yet but we'd want something like this for testing
    core = rcp_26_core

    yield core


def test_adapter_base_class_init():
    parametersstub = "Parameters"
    outputstub = "Parameters"
    Adapter.__abstractmethods__ = set()
    adapter = Adapter(parametersstub, outputstub)  # pylint: disable=abstract-class-instantiated
    assert adapter._parameters == parametersstub
    assert adapter._output == outputstub


def test_adapter_base_class_initialise_run_parameters():
    Adapter.__abstractmethods__ = set()
    adapter = Adapter(ParameterSet(), ParameterSet())  # noqa

    start_time = 0
    stop_time = 1
    adapter.initialize_run_parameters(start_time, stop_time)
    assert adapter._start_time == start_time
    assert adapter._stop_time == stop_time


def test_adapter_base_class_run():
    Adapter.__abstractmethods__ = set()
    adapter = Adapter(ParameterSet(), ParameterSet())  # noqa
    start_time = 0
    adapter.initialize_run_parameters(start_time, 1)
    adapter.initialize_model_input()
    adapter.reset()
    assert adapter._current_time == start_time
    adapter.run()
    assert adapter.step() == start_time


class _AdapterTester(object):
    """Base class for adapter testing.

    At minimum, a new adapter should define a subclass of this class called,
    ``AdapterXTester`` which has ``tadapter`` equal to the adapter to be tested.
    This ensures that the new adapter is subject to all of OpenSCM's minimum
    requirements whilst giving authors the ability to tweak the tests as necessary
    for their specific adapter.
    """
    @property
    @abstractmethod
    def tadapter(self):
        """Adapter to test
        """
        pass

    def test_initialize(self):
        tadapter = self.tadapter
        assert not tadapter.initialized
        tadapter._initialize_model()
        assert tadapter.initialized

    def test_shutdown(self, test_adapter):
        """Test the adapter can be shutdown

        Extra tests can be adapted depending on what the adapter should actually
        do on shutdown.
        """
        test_adapter.shutdown()

    def test_initialise_model_input(self, test_adapter, test_config_paraset):
        """Test that initalising model input does as intended
        """
        # @swillner I am not sure how we want this to work. I still don't understand
        # how the model can distinguish between 'model_input' and 'run_parameters' if
        # it is always reading from one ParameterSet i.e. how does it know which
        # parameters in the ParameterSet to set when `initialise_model_input` is
        # called vs. `intialise_run_paramters`?
        test_adapter.initialize_model_input(test_config_paraset)
        # some test here that model input was set as intended (will have to be model
        # specific I think).

    def test_initialise_model_input_non_model_parameter(self, test_adapter, test_config_paraset):
        tname = "junk"
        test_config_paraset.get_writable_scalar_view(tname, ("World",), "K").set(4)
        # What should happen here when we try to write a parameter which the model
        # does not recognise? Warning? Error?
        test_adapter.initialize_model_input(test_config_paraset)

    def test_initialise_run_parameters(self, test_adapter, test_config_paraset):
        """Test that initalising run parameters does as intended
        """
        # blocked by questions about initialize_model_input above
        test_adapter.initialize_run_parameters(test_config_paraset)

    def test_initialise_run_parameters_non_model_parameter(self, test_adapter, test_config_paraset):
        # blocked by questions about initialize_model_input above
        tname = "junk"
        test_config_paraset.get_writable_scalar_view(tname, ("World",), "K").set(4)
        # What should happen here when we try to write a parameter which the model
        # does not recognise? Warning? Error?
        test_adapter.initialize_run_parameters(test_config_paraset)

    def test_run(self, test_adapter, test_config_paraset, test_drivers_core):
        test_adapter.initialize_model_input(test_drivers_core)
        test_adapter.initialize_run_parameters(test_config_paraset)

        res = test_adapter.run()

        assert res.parameters.get_scalar_view(
            name=("ecs",), region=("World",), unit="K"
        ).get() == 3

        assert res.parameters.get_scalar_view(
            name=("rf2xco2",), region=("World",), unit="W / m^2"
        ).get() == 4.0
