"""
Ophyd support for the EPICS synApps sscan record

see:  https://epics.anl.gov/bcda/synApps/sscan/SscanRecord.html

EXAMPLE

    import apstools.synApps
    scans = apstools.synApps.SscanDevice("xxx:", name="scans")
    scans.select_channels()     # only the channels configured in EPICS


Public Structures

.. autosummary::

    ~SscanRecord
    ~SscanDevice

Private Structures

.. autosummary::

    ~sscanPositioner
    ~sscanDetector
    ~sscanTrigger

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


from collections import OrderedDict
from ophyd.device import (
    Device,
    Component as Cpt,
    DynamicDeviceComponent as DDC,
    FormattedComponent as FC)
from ophyd import EpicsSignal, EpicsSignalRO
from ophyd.status import DeviceStatus
from ophyd.ophydobj import Kind

from .. import utils as APS_utils


__all__ = """
    SscanRecord
    SscanDevice
    """.split()


class sscanPositioner(Device):
    """
    positioner of an EPICS sscan record

    .. autosummary::

        ~defined_in_EPICS
        ~reset

    """

    readback_pv = FC(EpicsSignal, '{self.prefix}.R{self._ch_num}PV', kind=Kind.config, auto_monitor=True)
    readback_value = FC(EpicsSignalRO, '{self.prefix}.R{self._ch_num}CV', auto_monitor=True)
    array = FC(EpicsSignalRO, '{self.prefix}.P{self._ch_num}CA', kind=Kind.omitted, auto_monitor=True)
    setpoint_pv = FC(EpicsSignal, '{self.prefix}.P{self._ch_num}PV', kind=Kind.config, auto_monitor=True)
    setpoint_value = FC(EpicsSignalRO, '{self.prefix}.P{self._ch_num}DV', auto_monitor=True)
    start = FC(EpicsSignal, '{self.prefix}.P{self._ch_num}SP', kind=Kind.config, auto_monitor=True)
    center = FC(EpicsSignal, '{self.prefix}.P{self._ch_num}CP', kind=Kind.config, auto_monitor=True)
    end = FC(EpicsSignal, '{self.prefix}.P{self._ch_num}EP', kind=Kind.config, auto_monitor=True)
    step_size = FC(EpicsSignal, '{self.prefix}.P{self._ch_num}SI', kind=Kind.config, auto_monitor=True)
    width = FC(EpicsSignal, '{self.prefix}.P{self._ch_num}WD', kind=Kind.config, auto_monitor=True)
    abs_rel = FC(EpicsSignal, '{self.prefix}.P{self._ch_num}AR', kind=Kind.config, auto_monitor=True)
    mode = FC(EpicsSignal, '{self.prefix}.P{self._ch_num}SM', kind=Kind.config, auto_monitor=True)
    units = FC(EpicsSignalRO, '{self.prefix}.P{self._ch_num}EU', kind=Kind.config, auto_monitor=True)

    def __init__(self, prefix, num, **kwargs):
        self._ch_num = num
        super().__init__(prefix, **kwargs)

    def reset(self):
        """set all fields to default values"""
        self.readback_pv.put("")
        self.setpoint_pv.put("")
        self.start.put(0)
        self.center.put(0)
        self.end.put(0)
        self.step_size.put(0)
        self.width.put(0)
        self.abs_rel.put("ABSOLUTE")
        self.mode.put("LINEAR")

    @property
    def defined_in_EPICS(self):
        """True if defined in EPICS"""
        return len(self.setpoint_pv.value.strip()) > 0


class sscanDetector(Device):
    """
    detector of an EPICS sscan record

    .. autosummary::

        ~defined_in_EPICS
        ~reset

    """

    input_pv = FC(EpicsSignal, '{self.prefix}.D{self._ch_num}PV', kind=Kind.config, auto_monitor=True)
    current_value = FC(EpicsSignal, '{self.prefix}.D{self._ch_num}CV', auto_monitor=True)
    array = FC(EpicsSignal, '{self.prefix}.D{self._ch_num}CA', kind=Kind.omitted, auto_monitor=True)

    def __init__(self, prefix, num, **kwargs):
        self._ch_num = num
        super().__init__(prefix, **kwargs)

    def reset(self):
        """set all fields to default values"""
        self.input_pv.put("")

    @property
    def defined_in_EPICS(self):
        """True if defined in EPICS"""
        return len(self.input_pv.value.strip()) > 0


class sscanTrigger(Device):
    """
    detector trigger of an EPICS sscan record

    .. autosummary::

        ~reset
    """

    trigger_pv = FC(EpicsSignal, '{self.prefix}.T{self._ch_num}PV', kind=Kind.config, auto_monitor=True)
    trigger_value = FC(EpicsSignal, '{self.prefix}.T{self._ch_num}CD', auto_monitor=True)

    def __init__(self, prefix, num, **kwargs):
        self._ch_num = num
        super().__init__(prefix, **kwargs)

    def reset(self):
        """set all fields to default values"""
        self.trigger_pv.put("")
        self.trigger_value.put(1)

    @property
    def defined_in_EPICS(self):
        """True if defined in EPICS"""
        return len(self.trigger_pv.value.strip()) > 0


def _sscan_positioners(channel_list):
    defn = OrderedDict()
    for chan in channel_list:
        attr = 'p{}'.format(chan)
        defn[attr] = (sscanPositioner, '', {'num': chan})
    return defn


def _sscan_detectors(channel_list):
    defn = OrderedDict()
    for chan in channel_list:
        attr = 'd{}'.format(chan)
        defn[attr] = (sscanDetector, '', {'num': chan})
    return defn


def _sscan_triggers(channel_list):
    defn = OrderedDict()
    for chan in channel_list:
        attr = 't{}'.format(chan)
        defn[attr] = (sscanTrigger, '', {'num': chan})
    return defn


class SscanRecord(Device):
    """
    EPICS synApps sscan record: used as $(P):scan(N)

    .. autosummary::

        ~defined_in_EPICS
        ~reset
        ~select_channels

    """

    desc = Cpt(EpicsSignal, '.DESC', kind=Kind.config, auto_monitor=True)
    scan_phase = Cpt(EpicsSignalRO, '.FAZE', auto_monitor=True)
    data_state = Cpt(EpicsSignalRO, '.DSTATE', auto_monitor=True)
    data_ready = Cpt(EpicsSignalRO, '.DATA', auto_monitor=True)
    scan_busy = Cpt(EpicsSignalRO, '.BUSY', auto_monitor=True)
    alert_flag = Cpt(EpicsSignalRO, '.ALRT', auto_monitor=True)
    alert_message = Cpt(EpicsSignalRO, '.SMSG', auto_monitor=True)
    number_points = Cpt(EpicsSignal, '.NPTS', kind=Kind.config, auto_monitor=True)
    maximum_number_points = Cpt(EpicsSignal, '.MPTS', kind=Kind.config, auto_monitor=True)
    current_point = Cpt(EpicsSignalRO, '.CPT', auto_monitor=True)
    pasm = Cpt(EpicsSignal, '.PASM', auto_monitor=True)
    execute_scan = Cpt(EpicsSignal, '.EXSC', auto_monitor=True)
    bspv = Cpt(EpicsSignal, '.BSPV', kind=Kind.config, auto_monitor=True)
    bscd = Cpt(EpicsSignal, '.BSCD', auto_monitor=True)
    bswait = Cpt(EpicsSignal, '.BSWAIT', auto_monitor=True)
    cmnd = Cpt(EpicsSignal, '.CMND', auto_monitor=True)
    detector_delay = Cpt(EpicsSignal, '.DDLY', auto_monitor=True)
    positioner_delay = Cpt(EpicsSignal, '.PDLY', auto_monitor=True)
    reference_detector = Cpt(EpicsSignal, '.REFD', kind=Kind.config, auto_monitor=True)
    wait = Cpt(EpicsSignal, '.WAIT', auto_monitor=True)
    wcnt = Cpt(EpicsSignalRO, '.WCNT', auto_monitor=True)
    awct = Cpt(EpicsSignal, '.AWCT', auto_monitor=True)
    acqt = Cpt(EpicsSignal, '.ACQT', auto_monitor=True)
    acqm = Cpt(EpicsSignal, '.ACQM', auto_monitor=True)
    atime = Cpt(EpicsSignal, '.ATIME', auto_monitor=True)
    copyto = Cpt(EpicsSignal, '.COPYTO', auto_monitor=True)
    a1pv = Cpt(EpicsSignal, '.A1PV', kind=Kind.config, auto_monitor=True)
    a1nv = Cpt(EpicsSignal, '.A1NV', kind=Kind.config, auto_monitor=True)
    a1cd = Cpt(EpicsSignal, '.A1CD', auto_monitor=True)
    aspv = Cpt(EpicsSignal, '.ASPV', kind=Kind.config, auto_monitor=True)
    ascd = Cpt(EpicsSignal, '.ASCD', auto_monitor=True)

    positioners = DDC(
        _sscan_positioners(
            "1 2 3 4".split()
        )
    )
    detectors = DDC(
        _sscan_detectors(
            APS_utils.itemizer("%02d", range(1,71))
        )
    )
    triggers = DDC(
        _sscan_triggers(
            "1 2 3 4".split()
        )
    )

    def set(self, value, **kwargs):
        """interface to use bps.mv()"""
        if value != 1:
            return

        working_status = DeviceStatus(self)
        started = False

        def execute_scan_cb(value, timestamp, **kwargs):
            value = int(value)
            if started and value == 0:
                working_status._finished()

        self.execute_scan.subscribe(execute_scan_cb)
        self.execute_scan.set(1)
        started = True
        return working_status

    def reset(self):
        """set all fields to default values"""
        self.desc.put(self.desc.pvname.split(".")[0])
        self.number_points.put(1000)
        for part in (self.positioners, self.detectors, self.triggers):
            for ch_name in part.component_names:
                channel = getattr(part, ch_name)
                channel.reset()
        self.a1pv.put("")
        self.acqm.put("NORMAL")
        if self.name.find("scanH") > 0:
            self.acqt.put("1D ARRAY")
        else:
            self.acqt.put("SCALAR")
        self.aspv.put("")
        self.bspv.put("")
        self.pasm.put("STAY")
        self.bswait.put("Wait")
        self.a1cd.put(1)
        self.ascd.put(1)
        self.bscd.put(1)
        self.reference_detector.put(1)
        self.atime.put(0)
        self.awct.put(0)
        self.copyto.put(0)
        self.detector_delay.put(0)
        self.positioner_delay.put(0)
        while self.wcnt.get() > 0:
            self.wait.put(0)

    def select_channels(self):
        """
        Select channels that are configured in EPICS
        """
        for part in (self.positioners, self.detectors, self.triggers):
            channel_names = []      # part.get_configured_channels()
            channel_names = [ch for ch in part.component_names if getattr(part, ch).defined_in_EPICS]

            part.configuration_attrs = channel_names
            part.read_attrs = channel_names
            part.kind = Kind.normal

    @property
    def defined_in_EPICS(self):
        """True if will be used in EPICS"""
        self.select_channels()
        channels = len(self.positioners.read_attrs)
        channels += len(self.detectors.read_attrs)
        #channels += len(self.triggers.read_attrs)
        return channels > 0


class SscanDevice(Device):
    """
    synApps XXX IOC setup of sscan records: $(P):scan$(N)

    .. autosummary::

        ~reset
        ~select_channels

    """

    scan_dimension = Cpt(EpicsSignalRO, 'ScanDim', auto_monitor=True)
    scan_pause = Cpt(EpicsSignal, 'scanPause', auto_monitor=True)
    abort_scans = Cpt(EpicsSignal, 'AbortScans', auto_monitor=True)
    scan1 = Cpt(SscanRecord, 'scan1')
    scan2 = Cpt(SscanRecord, 'scan2')
    scan3 = Cpt(SscanRecord, 'scan3')
    scan4 = Cpt(SscanRecord, 'scan4')
    scanH = Cpt(SscanRecord, 'scanH')
    resume_delay = Cpt(EpicsSignal, 'scanResumeSEQ.DLY1', auto_monitor=True)

    def reset(self):
        """set all fields to default values"""
        for chnum in "1 2 3 4 H".split():
            getattr(self, "scan" + chnum).reset()

    def select_channels(self):
        """
        Select only the scans that are configured in EPICS
        """
        scans = ["scan"+ch for ch in "1 2 3 4 H".split()]
        attrs = []
        for nm in self.component_names:
            if nm in scans and not getattr(self, nm).defined_in_EPICS:
                continue
            attrs.append(nm)
        self.read_attrs = attrs
