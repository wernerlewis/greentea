#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Plugin for reset with pyOCD."""
from .host_test_plugins import HostTestPluginBase

try:
    from pyocd.core.helpers import ConnectHelper

    PYOCD_PRESENT = True
except ImportError:
    PYOCD_PRESENT = False


class HostTestPluginResetMethod_pyOCD(HostTestPluginBase):
    """PyOCD reset plugin."""

    # Plugin interface
    name = "HostTestPluginResetMethod_pyOCD"
    type = "ResetMethod"
    stable = True
    capabilities = ["pyocd"]
    required_parameters = ["target_id"]

    def __init__(self):
        """Initialise object."""
        HostTestPluginBase.__init__(self)

    def setup(self, *args, **kwargs):
        """Configure plugin."""
        return True

    def execute(self, capability, *args, **kwargs):
        """Execute capability by name.

        Args:
            capability: Capability name, pyocd to reset.
            args: Additional arguments.
            kwargs: Additional arguments.

        Returns:
            True if reset successful, else False.
        """
        if not PYOCD_PRESENT:
            self.print_plugin_error(
                'The "pyocd" feature is not installed. Please run '
                '"pip install mbed-os-tools[pyocd]" to enable the "pyocd" reset plugin.'
            )
            return False

        if not kwargs["target_id"]:
            self.print_plugin_error("Error: target_id not set")
            return False

        result = False
        if self.check_parameters(capability, *args, **kwargs) is True:
            if kwargs["target_id"]:
                if capability == "pyocd":
                    target_id = kwargs["target_id"]
                    with ConnectHelper.session_with_chosen_probe(
                        unique_id=target_id, resume_on_disconnect=False
                    ) as session:
                        session.target.reset()
                        session.target.resume()
                        result = True
        return result


def load_plugin():
    """Get plugin available in this module.

    Returns:
        Plugin object.
    """
    return HostTestPluginResetMethod_pyOCD()
