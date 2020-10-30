"""
Ophyd support for the EPICS epid record


Public Structures

.. autosummary::

    ~EpidRecord

:see: https://epics.anl.gov/bcda/synApps/std/epidRecord.html
"""

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     jemian@anl.gov
# :copyright: (c) 2017-2020, UChicago Argonne, LLC
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

from ophyd.device import Component
from ophyd import EpicsSignal, EpicsSignalRO
from ._common import EpicsRecordDeviceCommonAll
from ._common import EpicsRecordFloatFields


__all__ = ["EpidRecord", ]


class EpidRecord(EpicsRecordFloatFields, EpicsRecordDeviceCommonAll):
    """
    EPICS epid record support in ophyd

    :see: https://epics.anl.gov/bcda/synApps/std/epidRecord.html
    """
    controlled_value_link = Component(EpicsSignal, ".INP", auto_monitor=True)
    controlled_value = Component(EpicsSignalRO, ".CVAL", auto_monitor=True)

    readback_trigger_link = Component(EpicsSignal, ".TRIG", auto_monitor=True)
    readback_trigger_link_value = Component(EpicsSignal, ".TVAL", auto_monitor=True)

    setpoint_location = Component(EpicsSignal, ".STPL", auto_monitor=True)
    setpoint_mode_select = Component(EpicsSignal, ".SMSL", auto_monitor=True)

    output_location = Component(EpicsSignal, ".OUTL", auto_monitor=True)
    feedback_on = Component(EpicsSignal, ".FBON", auto_monitor=True)

    proportional_gain = Component(EpicsSignal, ".KP", auto_monitor=True)
    integral_gain = Component(EpicsSignal, ".KI", auto_monitor=True)
    derivative_gain = Component(EpicsSignal, ".KD", auto_monitor=True)

    following_error = Component(EpicsSignalRO, ".ERR", auto_monitor=True)
    output_value = Component(EpicsSignalRO, ".OVAL", auto_monitor=True)
    final_value = Component(EpicsSignalRO, ".VAL", auto_monitor=True)

    calculated_P = Component(EpicsSignalRO, ".P", auto_monitor=True)
    calculated_I = Component(EpicsSignal, ".I", auto_monitor=True)
    calculated_D = Component(EpicsSignalRO, ".D", auto_monitor=True)

    time_difference = Component(EpicsSignal, ".DT", auto_monitor=True)
    minimum_delta_time = Component(EpicsSignal, ".MDT", auto_monitor=True)

    # limits imposed by the record support:
    #     .LOPR <= .OVAL <= .HOPR
    #     .LOPR <= .I <= .HOPR
    high_limit = Component(EpicsSignal, ".DRVH", auto_monitor=True)
    low_limit = Component(EpicsSignal, ".DRVL", auto_monitor=True)

    @property
    def value(self):
        return self.output_value.value
