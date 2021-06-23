#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Copy plugin for ublox platform."""
import os

from .host_test_plugins import HostTestPluginBase


class HostTestPluginCopyMethod_ublox(HostTestPluginBase):
    """Flashing method for ublox platform."""

    # Plugin interface
    name = "HostTestPluginCopyMethod_ublox"
    type = "CopyMethod"
    capabilities = ["ublox"]
    required_parameters = ["image_path"]

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
        self.FLASH_ERASE = "FlashErase.exe"
        return True

    def execute(self, capability, *args, **kwargs):
        """Execute capability by name.

        Args:
            capability: Capability name, ublox to copy.
            args: Additional arguments.
            kwargs: Additional arguments.

        Returns:
            Value returned by executed capability.
        """
        result = False
        if self.check_parameters(capability, *args, **kwargs) is True:
            image_path = os.path.normpath(kwargs["image_path"])
            if capability == "ublox":
                # Example:
                # FLASH_ERASE -c 2 -s 0xD7000 -l 0x20000 -f "binary_file.bin"
                cmd = [
                    self.FLASH_ERASE,
                    "-c",
                    "A",
                    "-s",
                    "0xD7000",
                    "-l",
                    "0x20000",
                    "-f",
                    image_path,
                ]
                result = self.run_command(cmd)
        return result


def load_plugin():
    """Get plugin available in this module.

    Returns:
        Plugin object.
    """
    return HostTestPluginCopyMethod_ublox()
