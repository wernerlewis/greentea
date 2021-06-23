#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Reset plugin for ublox platform."""
from .host_test_plugins import HostTestPluginBase


class HostTestPluginResetMethod_ublox(HostTestPluginBase):
    """Reset method for ublox platform."""

    # Plugin interface
    name = "HostTestPluginResetMethod_ublox"
    type = "ResetMethod"
    capabilities = ["ublox"]
    required_parameters = []
    stable = False

    def is_os_supported(self, os_name=None):
        """Check if OS supported by plugin.

        Args:
            os_name: Name of the OS.

        Returns:
            True if OS is Windows, else False.
        """
        # If no OS name provided use host OS name
        if not os_name:
            os_name = self.host_os_support()

        # This plugin only works on Windows
        if os_name and os_name.startswith("Windows"):
            return True
        return False

    def setup(self, *args, **kwargs):
        """Configure plugin.

        Should be called before execute() method is used.
        """
        # Note you need to have jlink.exe on your system path!
        self.JLINK = "jlink.exe"
        return True

    def execute(self, capability, *args, **kwargs):
        """Execute capability by name.

        Args:
            capability: Capability name, ublox to reset.
            args: Additional arguments.
            kwargs: Additional arguments.

        Returns:
            Value returned by executed capability.
        """
        result = False
        if self.check_parameters(capability, *args, **kwargs) is True:
            if capability == "ublox":
                # Example:
                # JLINK.exe --CommanderScript aCommandFile
                cmd = [self.JLINK, "-CommanderScript", r"reset.jlink"]
                result = self.run_command(cmd)
        return result


def load_plugin():
    """Get plugin available in this module.

    Returns:
        Plugin object.
    """
    return HostTestPluginResetMethod_ublox()
