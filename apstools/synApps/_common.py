"""
Ophyd support for fields common to all EPICS records


Public Structures

.. autosummary::

    ~EpicsRecordDeviceCommonAll
    ~EpicsRecordInputFields
    ~EpicsRecordOutputFields
    ~EpicsRecordFloatFields

:see: https://wiki-ext.aps.anl.gov/epics/index.php/RRM_3-14_dbCommon
:see: https://wiki-ext.aps.anl.gov/epics/index.php/RRM_3-14_Common
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

from ophyd.device import Device, Component
from ophyd import EpicsSignal, EpicsSignalRO


__all__ = [
    "EpicsRecordDeviceCommonAll",
    "EpicsRecordInputFields",
    "EpicsRecordOutputFields",
    "EpicsRecordFloatFields",
    ]


class EpicsRecordDeviceCommonAll(Device):
    """
    Many of the fields common to all EPICS records

    Some fields are not included because they are not interesting to
    an EPICS client or are already provided in other support.
    """
    description = Component(EpicsSignal, ".DESC", auto_monitor=True)
    processing_active = Component(EpicsSignalRO, ".PACT", auto_monitor=True)
    scanning_rate = Component(EpicsSignal, ".SCAN", auto_monitor=True)
    disable_value = Component(EpicsSignal, ".DISV", auto_monitor=True)
    scan_disable_input_link_value = Component(EpicsSignal, ".DISA", auto_monitor=True)
    scan_disable_value_input_link = Component(EpicsSignal, ".SDIS", auto_monitor=True)
    process_record = Component(EpicsSignal, ".PROC")
    forward_link = Component(EpicsSignal, ".FLNK")
    trace_processing = Component(EpicsSignal, ".TPRO")
    device_type = Component(EpicsSignalRO, ".DTYP")

    alarm_status = Component(EpicsSignalRO, ".STAT", auto_monitor=True)
    alarm_severity = Component(EpicsSignalRO, ".SEVR", auto_monitor=True)
    new_alarm_status = Component(EpicsSignalRO, ".NSTA", auto_monitor=True)
    new_alarm_severity = Component(EpicsSignalRO, ".NSEV", auto_monitor=True)
    disable_alarm_severity = Component(EpicsSignal, ".DISS", auto_monitor=True)


class EpicsRecordInputFields(Device):
    """
    some fields common to EPICS input records
    """
    input_link = Component(EpicsSignal, ".INP", auto_monitor=True)
    raw_value = Component(EpicsSignal, ".RVAL", auto_monitor=True)
    final_value = Component(EpicsSignal, ".VAL", auto_monitor=True)

    # will ignore simulation mode fields

    @property
    def value(self):
        return self.final_value.value


class EpicsRecordOutputFields(Device):
    """
    some fields common to EPICS output records
    """
    output_link = Component(EpicsSignal, ".OUT", auto_monitor=True)
    raw_value = Component(EpicsSignal, ".RVAL", auto_monitor=True)
    output_value = Component(EpicsSignal, ".OVAL", auto_monitor=True)
    readback_value = Component(EpicsSignalRO, ".RBV", auto_monitor=True)
    desired_output_location = Component(EpicsSignal, ".DOL", auto_monitor=True)
    output_mode_select = Component(EpicsSignal, ".OMSL", auto_monitor=True)
    desired_value = Component(EpicsSignal, ".VAL", auto_monitor=True)

    # will ignore simulation mode fields

    @property
    def value(self):
        return self.desired_value.value


class EpicsRecordFloatFields(Device):
    """
    some fields common to EPICS records supporting floating point values
    """
    units = Component(EpicsSignal, ".EGU", auto_monitor=True)
    precision = Component(EpicsSignal, ".PREC", auto_monitor=True)

    monitor_deadband = Component(EpicsSignal, ".MDEL", auto_monitor=True)

    # upper and lower display limits for the VAL, CVAL, HIHI, HIGH, LOW, and LOLO fields
    high_operating_range = Component(EpicsSignal, ".HOPR", auto_monitor=True)
    low_operating_range = Component(EpicsSignal, ".LOPR", auto_monitor=True)

    hihi_alarm_limit = Component(EpicsSignal, ".HIHI", auto_monitor=True)
    high_alarm_limit = Component(EpicsSignal, ".HIGH", auto_monitor=True)
    low_alarm_limit = Component(EpicsSignal, ".LOW", auto_monitor=True)
    lolo_alarm_limit = Component(EpicsSignal, ".LOLO", auto_monitor=True)
    hihi_alarm_severity = Component(EpicsSignal, ".HHSV", auto_monitor=True)
    high_alarm_severity = Component(EpicsSignal, ".HSV", auto_monitor=True)
    low_alarm_severity = Component(EpicsSignal, ".LSV", auto_monitor=True)
    lolo_alarm_severity = Component(EpicsSignal, ".LLSV", auto_monitor=True)
    alarm_hysteresis = Component(EpicsSignal, ".HYST", auto_monitor=True)
