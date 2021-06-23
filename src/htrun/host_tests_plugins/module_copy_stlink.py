#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Copy plugin for STLink."""
import os
from .host_test_plugins import HostTestPluginBase


class HostTestPluginCopyMethod_Stlink(HostTestPluginBase):
    """Copy plugin for STLink."""

    # Plugin interface
    name = "HostTestPluginCopyMethod_Stlink"
    type = "CopyMethod"
    capabilities = ["stlink"]
    required_parameters = ["image_path"]

    def __init__(self):
        """Initialise object."""
        HostTestPluginBase.__init__(self)

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
        """Configure plugin."""
        self.ST_LINK_CLI = "ST-LINK_CLI.exe"
        return True

    def execute(self, capability, *args, **kwargs):
        """Execute capability by name.

        Args:
            capability: Capability name, stlink to copy.
            args: Additional arguments.
            kwargs: Additional arguments.

        Returns:
            True if copy successful, else False.
        """
        result = False
        if self.check_parameters(capability, *args, **kwargs) is True:
            image_path = os.path.normpath(kwargs["image_path"])
            if capability == "stlink":
                # Example:
                # ST-LINK_CLI.exe -p
                # "C:\Work\mbed\build\test\DISCO_F429ZI\GCC_ARM\MBED_A1\basic.bin"
                cmd = [self.ST_LINK_CLI, "-p", image_path, "0x08000000", "-V"]
                result = self.run_command(cmd)
        return result


def load_plugin():
    """Get plugin available in this module.

    Returns:
        Plugin object.
    """
    return HostTestPluginCopyMethod_Stlink()
