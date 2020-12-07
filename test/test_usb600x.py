"""
This files is for testing the National Instruments USB-600x series of data
acquisition devices.  To execute this test, the device must be attached to
the PC and the following connections must be made:

 - port0.line0 to port1.line0
 - port0.line1 to port1.line1
 - ao0 to (ai0+ and ai1)
 - ao1 to (ai0- and ai5)

Only one of the USB NI-600x device should be connected to the PC at the time
of the test.  If the `device_model_number` is different that what is connected
to the PC, the test may fail.

The testing that will occur will look something like this:

 - port0.line0 to True, read port1.line0, ensure is True
 - port0.line0 to False, read port1.line0, ensure is False
 - port0.line1 to True, read port1.line1, ensure is True
 - port0.line1 to False, read port1.line1, ensure is False
 - ao0 to 2.5V, confirm with ai1 (single-ended ground-referenced measurement)
 - ao1 to 2.5V, confirm with ai5 (single-ended ground-referenced measurement)
 - confirm ai0 differential measurement of 0.0V
 - change ao0 to 3.5V, confirm ai0 different measurement of 1.0V
 - repeat analog sequence on ao1
"""
import pytest
from daqmx import NIDAQmxInstrument

device_model_number = 'USB-6001'


@pytest.fixture
def daq():
    instrument = NIDAQmxInstrument(model_number=device_model_number)

    # configure port0.line0 and line1 to inputs
    instrument.port0.line0
    instrument.port0.line1

    # configure ao lines to 0V
    instrument.ao0 = 0
    instrument.ao1 = 0

    yield instrument


def test_hardware_acquisition(daq):
    assert True


def test_dio0_true(daq):
    """
    Change state of port0.line0, port0.line1, then
    reads those lines using port1.

    :param daq: the NIDAQmxInstrument instance
    :return:
    """
    daq.port0.line0 = True
    daq.port0.line1 = False

    assert daq.port1.line0 == True
    assert daq.port1.line1 == False


def test_dio0_false(daq):
    """
    Change state of port0.line0, port0.line1, then
    reads those lines using port1.

    :param daq: the NIDAQmxInstrument instance
    :return:
    """
    daq.port0.line0 = False
    daq.port0.line1 = True

    assert daq.port1.line0 == False
    assert daq.port1.line1 == True


def test_dio1_true(daq):
    """
    Change state of port1.line0, port1.line1, then
    reads those lines using port0.

    :param daq: the NIDAQmxInstrument instance
    :return:
    """
    daq.port1.line0 = True
    daq.port1.line1 = False

    assert daq.port0.line0 == True
    assert daq.port0.line1 == False


def test_dio1_false(daq):
    """
    Change state of port1.line0, port1.line1, then
    reads those lines using port0.

    :param daq: the NIDAQmxInstrument instance
    :return:
    """
    daq.port1.line0 = False
    daq.port1.line1 = True

    assert daq.port0.line0 == False
    assert daq.port0.line1 == True


def test_ai0_diff(daq):
    # set to near 0.0V differential
    daq.ao0 = 2.5
    daq.ao1 = 2.5

    # check 100 samples, ensure that they are all close to the expected value
    for value in daq.ai0.capture(sample_count=100):
        if value > 0.01 or value < -0.01:
            assert False

    # set to 1.0V differential
    daq.ao0 = 3.0
    daq.ao1 = 2.0
    for value in daq.ai0.capture(sample_count=100):
        if value > 1.01 or value < 0.99:
            assert False

    # set to -1.0V differential
    daq.ao0 = 2.0
    daq.ao1 = 3.0
    for value in daq.ai0.capture(sample_count=100):
        if value > -0.99 or value < -1.01:
            assert False
