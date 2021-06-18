#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import re
import pkg_resources
from .host_test_plugins import HostTestPluginBase


class HostTestPluginResetMethod_Target(HostTestPluginBase):

    # Plugin interface
    name = "HostTestPluginResetMethod_Target"
    type = "ResetMethod"
    stable = True
    capabilities = ["default"]
    required_parameters = ["serial"]

    def __init__(self):
        """! ctor
        @details We can check module version by referring to version attribute
        import pkg_resources
        print pkg_resources.require("htrun")[0].version
        '2.7'
        """
        HostTestPluginBase.__init__(self)

    def safe_sendBreak(self, serial):
        """! pyserial 3.x API implementation of send_brea / break_condition
        @details
        http://pyserial.readthedocs.org/en/latest/pyserial_api.html#serial.Serial.send_break
        http://pyserial.readthedocs.org/en/latest/pyserial_api.html#serial.Serial.break_condition
        """
        result = True
        try:
            serial.send_break()
        except:
            # In Linux a termios.error is raised in sendBreak and in setBreak.
            # The following break_condition = False is needed to release the reset signal on the target mcu.
            try:
                serial.break_condition = False
            except Exception as e:
                self.print_plugin_error(
                    "Error while doing 'serial.break_condition = False' : %s" % str(e)
                )
                result = False
        return result

    def setup(self, *args, **kwargs):
        """! Configure plugin, this function should be called before plugin execute() method is used."""
        return True

    def execute(self, capability, *args, **kwargs):
        """! Executes capability by name

        @param capability Capability name
        @param args Additional arguments
        @param kwargs Additional arguments
        @details Each capability e.g. may directly just call some command line program or execute building pythonic function
        @return Capability call return value
        """
        if not kwargs["serial"]:
            self.print_plugin_error("Error: serial port not set (not opened?)")
            return False

        result = False
        if self.check_parameters(capability, *args, **kwargs) is True:
            if kwargs["serial"]:
                if capability == "default":
                    serial = kwargs["serial"]
                    result = self.safe_sendBreak(serial)
        return result


def load_plugin():
    """! Returns plugin available in this module"""
    return HostTestPluginResetMethod_Target()
