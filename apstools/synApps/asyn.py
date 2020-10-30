"""
Ophyd support for the EPICS asyn record


Public Structures

.. autosummary::

    ~AsynRecord

:see: https://github.com/epics-modules/asyn
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


__all__ = ["AsynRecord", ]


class AsynRecord(EpicsRecordDeviceCommonAll):
    """
    EPICS asyn record support in ophyd

    :see: https://epics.anl.gov/modules/soft/asyn/R4-36/asynRecord.html
    :see: https://github.com/epics-modules/asyn
    :see: https://epics.anl.gov/modules/soft/asyn/
    """
    ascii_output = Component(EpicsSignal, ".AOUT", auto_monitor=True)
    binary_output = Component(EpicsSignal, ".BOUT", auto_monitor=True)
    end_of_message_reason = Component(EpicsSignalRO, ".EOMR", auto_monitor=True)
    input_format = Component(EpicsSignalRO, ".IFMT", auto_monitor=True)
    input_maxlength = Component(EpicsSignal, ".IMAX", auto_monitor=True)
    interface = Component(EpicsSignal, ".IFACE", auto_monitor=True)
    number_bytes_actually_read = Component(EpicsSignalRO, ".NRRD", auto_monitor=True)
    number_bytes_actually_written = Component(EpicsSignalRO, ".NAWT", auto_monitor=True)
    number_bytes_to_read = Component(EpicsSignal, ".NORD", auto_monitor=True)
    number_bytes_to_write = Component(EpicsSignal, ".NOWT", auto_monitor=True)
    octet_is_valid = Component(EpicsSignalRO, ".OCTETIV", auto_monitor=True)
    output_format = Component(EpicsSignalRO, ".OFMT", auto_monitor=True)
    output_maxlength = Component(EpicsSignal, ".OMAX", auto_monitor=True)
    terminator_input = Component(EpicsSignal, ".IEOS", auto_monitor=True)
    terminator_output = Component(EpicsSignal, ".OEOS", auto_monitor=True)
    timeout = Component(EpicsSignal, ".TMOT", auto_monitor=True)
    transaction_mode = Component(EpicsSignal, ".TMOD", auto_monitor=True)
    translated_input = Component(EpicsSignal, ".TINP", auto_monitor=True)

    binary_output_maxlength = output_maxlength     # TODO: deprecated name
