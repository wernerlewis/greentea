#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Copy plugin for JN51xx platform."""
import os
from .host_test_plugins import HostTestPluginBase


class HostTestPluginCopyMethod_JN51xx(HostTestPluginBase):
    """Copy plugin for JN51xx."""

    # Plugin interface
    name = "HostTestPluginCopyMethod_JN51xx"
    type = "CopyMethod"
    capabilities = ["jn51xx"]
    required_parameters = ["image_path", "serial"]

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
        """Configure plugin.

        Should be called before execute() method is used.
        """
        self.JN51XX_PROGRAMMER = "JN51xxProgrammer.exe"
        return True

    def execute(self, capability, *args, **kwargs):
        """Execute capability by name.

        Args:
            capability: Capability name, jn51xx to copy.
            args: Additional arguments.
            kwargs: Additional arguments.

        Returns:
            Value returned by executed capability.
        """
        if not kwargs["image_path"]:
            self.print_plugin_error("Error: image path not specified")
            return False

        if not kwargs["serial"]:
            self.print_plugin_error("Error: serial port not set (not opened?)")
            return False

        result = False
        if self.check_parameters(capability, *args, **kwargs):
            if kwargs["image_path"] and kwargs["serial"]:
                image_path = os.path.normpath(kwargs["image_path"])
                serial_port = kwargs["serial"]
                if capability == "jn51xx":
                    # Example:
                    # JN51xxProgrammer.exe -s COM15 -f <file> -V0
                    cmd = [
                        self.JN51XX_PROGRAMMER,
                        "-s",
                        serial_port,
                        "-f",
                        image_path,
                        "-V0",
                    ]
                    result = self.run_command(cmd)
        return result


def load_plugin():
    """Get plugin available in this module.

    Returns:
        Plugin object.
    """
    return HostTestPluginCopyMethod_JN51xx()
