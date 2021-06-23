#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Plugins used by host tests to reset and flash DUT.

This package can be extended for additional flash and reset methods.
"""

from . import plugin_registry

# This plugins provide 'flashing' and 'reset' methods to host test scripts
from . import module_copy_shell
from . import module_copy_to_target
from . import module_reset_target
from . import module_power_cycle_target
from . import module_copy_pyocd
from . import module_reset_pyocd

# Additional, non standard platforms
from . import module_copy_silabs
from . import module_reset_silabs
from . import module_copy_stlink
from . import module_reset_stlink
from . import module_copy_ublox
from . import module_reset_ublox
from . import module_reset_mps2
from . import module_copy_mps2

# import module_copy_jn51xx
# import module_reset_jn51xx


# Plugin registry instance
HOST_TEST_PLUGIN_REGISTRY = plugin_registry.HostTestPluginRegistry()

# Static plugin registration
# Some plugins are commented out if they are not stable or not commonly used
HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_copy_to_target.load_plugin())
HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_copy_shell.load_plugin())
HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_reset_target.load_plugin())
HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_copy_pyocd.load_plugin())

# Extra platforms support
HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_copy_mps2.load_plugin())
HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_reset_mps2.load_plugin())
HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_copy_silabs.load_plugin())
HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_reset_silabs.load_plugin())
HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_copy_stlink.load_plugin())
HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_reset_stlink.load_plugin())
HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_power_cycle_target.load_plugin())
HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_reset_pyocd.load_plugin())
HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_reset_ublox.load_plugin())
HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_copy_ublox.load_plugin())
# HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_copy_jn51xx.load_plugin())
# HOST_TEST_PLUGIN_REGISTRY.register_plugin(module_reset_jn51xx.load_plugin())

# TODO: extend plugin loading to files with name module_*.py loaded ad-hoc


###############################################################################
# Functional interface for host test plugin registry
###############################################################################
def call_plugin(type, capability, *args, **kwargs):
    """Call plugin from registry.

    Args:
        type: Plugin type.
        capability: Plugin capability to call.
        args: Additional parameters passed to plugin.
        kwargs: Additional parameters passed to plugin.

    Returns:
        Value returned from plugin call.
    """
    return HOST_TEST_PLUGIN_REGISTRY.call_plugin(type, capability, *args, **kwargs)


def get_plugin_caps(type):
    """Get list of all capabilities for plugin of a set type.

    Args:
        type: Type of plugin to get.

    Returns:
        List of all capabilities matching type.
    """
    return HOST_TEST_PLUGIN_REGISTRY.get_plugin_caps(type)


def get_plugin_info():
    """Get plugin info.

    Returns:
        Dictionary formatted from HOST_TEST_PLUGIN_REGISTRY.
    """
    return HOST_TEST_PLUGIN_REGISTRY.get_dict()


def print_plugin_info():
    """Print plugins information in human readable way."""
    print(HOST_TEST_PLUGIN_REGISTRY)
