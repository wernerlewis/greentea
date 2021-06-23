#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Reset plugin using serial connection."""
from termios import error as termios_err

from .host_test_plugins import HostTestPluginBase


class HostTestPluginResetMethod_Target(HostTestPluginBase):
    """Generic reset method with serial connection."""

    # Plugin interface
    name = "HostTestPluginResetMethod_Target"
    type = "ResetMethod"
    stable = True
    capabilities = ["default"]
    required_parameters = ["serial"]

    def __init__(self):
        """Initialise object."""
        HostTestPluginBase.__init__(self)

    def safe_sendBreak(self, serial):
        """Send break condition over serial.

        Args:
            serial: Serial connection to use.

        Returns:
            True on success, else False.
        """
        result = True
        try:
            serial.send_break()
        except termios_err:
            # In Linux a termios.error is raised in sendBreak and in setBreak.
            # The following break_condition = False is needed to release the reset
            # signal on the target mcu.
            try:
                serial.break_condition = False
            except Exception as e:
                self.print_plugin_error(
                    "Error while doing 'serial.break_condition = False' : %s" % str(e)
                )
                result = False
        return result

    def setup(self, *args, **kwargs):
        """Configure plugin."""
        return True

    def execute(self, capability, *args, **kwargs):
        """Execute capability by name.

        Args:
            capability: Capability name, serial to reset.
            args: Additional arguments.
            kwargs: Additional arguments.

        Returns:
            True if copy successful, else False.
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
    """Get plugin available in this module.

    Returns:
        Plugin object.
    """
    return HostTestPluginResetMethod_Target()
