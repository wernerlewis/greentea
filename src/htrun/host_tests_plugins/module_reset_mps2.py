#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Plugin for ARM_MPS2 platforms. Not fully functional."""
import os
import time

from .host_test_plugins import HostTestPluginBase


class HostTestPluginResetMethod_MPS2(HostTestPluginBase):
    """Plugin used to reset ARM_MPS2 platform.

    Supports: reboot.txt to startup from standby state, reboots when in run mode.
    """

    # Plugin interface
    name = "HostTestPluginResetMethod_MPS2"
    type = "ResetMethod"
    capabilities = ["reboot.txt"]
    required_parameters = ["disk"]

    def __init__(self):
        """Initialise object."""
        HostTestPluginBase.__init__(self)

    def touch_file(self, path):
        """Touch file and set timestamp to items.

        Args:
            path: Path of file to touch.
        """
        with open(path, "a"):
            os.utime(path, None)

    def setup(self, *args, **kwargs):
        """Configure plugin."""
        return True

    def execute(self, capability, *args, **kwargs):
        """Execute capability by name.

        Args:
            capability: Capability name, reboot.txt to reset board.
            args: Additional arguments.
            kwargs: Additional arguments.

        Returns:
            True if copy successful, else False.
        """
        result = False
        if not kwargs["disk"]:
            self.print_plugin_error("Error: disk not specified")
            return False

        destination_disk = kwargs.get("disk", None)

        # This optional parameter can be used if TargetID is provided (-t switch)
        target_id = kwargs.get("target_id", None)
        pooling_timeout = kwargs.get("polling_timeout", 60)
        if self.check_parameters(capability, *args, **kwargs) is True:

            if capability == "reboot.txt":
                reboot_file_path = os.path.join(destination_disk, capability)
                reboot_fh = open(reboot_file_path, "w")
                reboot_fh.close()
                # Make sure the file is written to the board before continuing
                if os.name == "posix":
                    self.run_command("sync -f %s" % reboot_file_path, shell=True)
                time.sleep(3)  # sufficient delay for device to boot up
                result, destination_disk = self.check_mount_point_ready(
                    destination_disk, target_id=target_id, timeout=pooling_timeout
                )
        return result


def load_plugin():
    """Get plugin available in this module.

    Returns:
        Plugin object.
    """
    return HostTestPluginResetMethod_MPS2()
