"""
Ophyd support for the iocStats support


Public Structures

.. autosummary::

    ~IocStatsDevice

"""

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     jemian@anl.gov
# :copyright: (c) 2017-2020, UChicago Argonne, LLC
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------

from ophyd import Component, Device, EpicsSignalRO, Signal


class IocStatsDevice(Device):

    _app_dir1 = Component(EpicsSignalRO, "APP_DIR1", kind="omitted", auto_monitor=True)
    _app_dir2 = Component(EpicsSignalRO, "APP_DIR2", kind="omitted", auto_monitor=True)
    _startup_script1 = Component(
        EpicsSignalRO, "ST_SCRIPT1", kind="omitted", auto_monitor=True
    )
    _startup_script2 = Component(
        EpicsSignalRO, "ST_SCRIPT2", kind="omitted", auto_monitor=True
    )
    access = Component(EpicsSignalRO, "ACCESS", string=True, auto_monitor=True)
    ca_client_count = Component(EpicsSignalRO, "CA_CLNT_CNT", auto_monitor=True)
    ca_connection_count = Component(EpicsSignalRO, "CA_CONN_CNT", auto_monitor=True)
    cpu_count = Component(EpicsSignalRO, "CPU_CNT", auto_monitor=True)
    engineer = Component(EpicsSignalRO, "ENGINEER", auto_monitor=True)
    epics_version = Component(EpicsSignalRO, "EPICS_VERS", auto_monitor=True)
    file_descriptors_free = Component(EpicsSignalRO, "FD_FREE", auto_monitor=True)
    file_descriptors_max_ = Component(EpicsSignalRO, "FD_MAX", auto_monitor=True)
    heartbeat = Component(EpicsSignalRO, "HEARTBEAT", auto_monitor=True)
    host_name = Component(EpicsSignalRO, "HOSTNAME", auto_monitor=True)
    ioc_cpu_load = Component(EpicsSignalRO, "IOC_CPU_LOAD", auto_monitor=True)
    iso8601 = Component(EpicsSignalRO, "iso8601", auto_monitor=True)
    kernel_version = Component(EpicsSignalRO, "KERNEL_VERS", auto_monitor=True)
    location = Component(EpicsSignalRO, "LOCATION", auto_monitor=True)
    max_array_bytes = Component(EpicsSignalRO, "CA_MAX_ARRAY", auto_monitor=True)
    memory_free = Component(EpicsSignalRO, "MEM_FREE", auto_monitor=True)
    memory_max = Component(EpicsSignalRO, "MEM_MAX", auto_monitor=True)
    memory_used = Component(EpicsSignalRO, "MEM_USED", auto_monitor=True)
    records_count = Component(EpicsSignalRO, "RECORD_CNT", auto_monitor=True)
    startup_time = Component(EpicsSignalRO, "STARTTOD", auto_monitor=True)
    suspended_task_count = Component(EpicsSignalRO, "SUSP_TASK_CNT", auto_monitor=True)
    system_cpu_load = Component(EpicsSignalRO, "SYS_CPU_LOAD", auto_monitor=True)
    time_of_day = Component(EpicsSignalRO, "TOD", auto_monitor=True)
    timezone = Component(EpicsSignalRO, "TIMEZONE", auto_monitor=True)
    uptime = Component(EpicsSignalRO, ":UPTIME", auto_monitor=True)

    # components updated from EpicsSignals
    application_directory = Component(Signal, value="")
    memory_used_percentage = Component(Signal, value=0)
    startup_script = Component(Signal, value="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def ad_update(value, *args, **kwargs):
            """
            update ``application_directory`` Signal

            Instead of a @property, keep a Signal updated
            so it will be recorded with a Device.read()
            """
            self.application_directory.put(
                self._app_dir1.get() + self._app_dir2.get()
            )

        self._app_dir1.subscribe(ad_update)
        self._app_dir2.subscribe(ad_update)

        def ss_update(value, *args, **kwargs):
            """
            update ``startup_script`` Signal

            Instead of a @property, keep a Signal updated
            so it will be recorded with a Device.read()
            """
            self.startup_script.put(
                self._startup_script1.get() + self._startup_script2.get()
            )

        self._startup_script1.subscribe(ss_update)
        self._startup_script2.subscribe(ss_update)

        def mem_used_update(value, *args, **kwargs):
            """
            update ``memory_used_percentage`` Signal

            Instead of a @property, keep a Signal updated
            so it will be recorded with a Device.read()
            """
            self.memory_used_percentage.put(
                100 * self.memory_used.get() / self.memory_max.get()
            )

        self.memory_used.subscribe(mem_used_update)
