#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Copy plugin for SiLabs."""
import os
from .host_test_plugins import HostTestPluginBase


class HostTestPluginCopyMethod_Silabs(HostTestPluginBase):
    """Copy plugin for SiLabs platform."""

    # Plugin interface
    name = "HostTestPluginCopyMethod_Silabs"
    type = "CopyMethod"
    capabilities = ["eACommander", "eACommander-usb"]
    required_parameters = ["image_path", "destination_disk"]
    stable = True

    def __init__(self):
        """Initialise object."""
        HostTestPluginBase.__init__(self)

    def setup(self, *args, **kwargs):
        """Configure plugin."""
        self.EACOMMANDER_CMD = "eACommander.exe"
        return True

    def execute(self, capability, *args, **kwargs):
        """Execute capability by name.

        Args:
            capability: Capability name, eACommander or eACommander-usb to copy.
            args: Additional arguments.
            kwargs: Additional arguments.

        Returns:
            True if copy successful, else False.
        """
        result = False
        if self.check_parameters(capability, *args, **kwargs) is True:
            image_path = os.path.normpath(kwargs["image_path"])
            destination_disk = os.path.normpath(kwargs["destination_disk"])
            if capability == "eACommander":
                cmd = [
                    self.EACOMMANDER_CMD,
                    "--serialno",
                    destination_disk,
                    "--flash",
                    image_path,
                    "--resettype",
                    "2",
                    "--reset",
                ]
                result = self.run_command(cmd)
            elif capability == "eACommander-usb":
                cmd = [
                    self.EACOMMANDER_CMD,
                    "--usb",
                    destination_disk,
                    "--flash",
                    image_path,
                ]
                result = self.run_command(cmd)
        return result


def load_plugin():
    """Get plugin available in this module.

    Returns:
        Plugin object.
    """
    return HostTestPluginCopyMethod_Silabs()
