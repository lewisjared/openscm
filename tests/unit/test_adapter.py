from openscm.adapter import Adapter
from openscm.core import ParameterSet


def test_adapter_base_class_init():
    parametersstub = "Parameters"
    outputstub = "Parameters"
    Adapter.__abstractmethods__ = set()
    adapter = Adapter(  # pylint: disable=abstract-class-instantiated
        parametersstub, outputstub
    )
    assert adapter._parameters == parametersstub
    assert adapter._output == outputstub


def test_adapter_base_class_initialize_model_input():
    Adapter.__abstractmethods__ = set()
    adapter = Adapter(  # pylint: disable=abstract-class-instantiated
        ParameterSet(), ParameterSet()
    )

    start_time = 0
    stop_time = 1
    adapter.initialize_model_input(start_time, stop_time)
    assert adapter._start_time == start_time
    assert adapter._stop_time == stop_time

    start_time = 1
    stop_time = 2
    adapter.initialize_model_input(start_time, stop_time)
    assert adapter._start_time == start_time
    assert adapter._stop_time == stop_time


def test_adapter_base_class_initialize_run_parameters():
    Adapter.__abstractmethods__ = set()
    adapter = Adapter(  # pylint: disable=abstract-class-instantiated
        ParameterSet(), ParameterSet()
    )

    adapter.initialize_run_parameters()
    assert adapter._initialized


def test_adapter_base_class_run():
    Adapter.__abstractmethods__ = set()
    adapter = Adapter(  # pylint: disable=abstract-class-instantiated
        ParameterSet(), ParameterSet()
    )
    start_time = 0
    adapter.initialize_run_parameters()
    adapter.initialize_model_input(start_time, 1)
    adapter.reset()
    assert adapter._current_time == start_time
    adapter.run()
    assert adapter.step() == start_time
