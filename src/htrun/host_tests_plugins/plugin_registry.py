#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Registry to store and access available plugins."""
from prettytable import PrettyTable, HEADER


class HostTestPluginRegistry:
    """Registry storing plugins and objects representing them."""

    # Here we actually store all the plugins
    PLUGINS = {}  # 'Plugin Name' : Plugin Object

    def print_error(self, text):
        """Print error directly to console.

        Args:
            text: Error message.
        """
        print("Plugin load failed. Reason: %s" % text)

    def register_plugin(self, plugin):
        """Register and store plugin in registry.

        Args:
            plugin: Plugin object to register.

        Returns:
            True if plugin setup and registration successful, else False.
        """
        # TODO:
        # - check for unique caps for specified type
        if plugin.name not in self.PLUGINS:
            if plugin.setup():  # Setup plugin can be completed without errors
                self.PLUGINS[plugin.name] = plugin
                return True
            else:
                self.print_error("%s setup failed" % plugin.name)
        else:
            self.print_error("%s already loaded" % plugin.name)
        return False

    def call_plugin(self, type, capability, *args, **kwargs):
        """Call plugin from registry.

        Args:
            type: Plugin type.
            capability: Plugin capability to call.
            args: Additional parameters passed to plugin.
            kwargs: Additional parameters passed to plugin.

        Returns:
            Value returned from plugin call.
        """
        for plugin_name in self.PLUGINS:
            plugin = self.PLUGINS[plugin_name]
            if plugin.type == type and capability in plugin.capabilities:
                return plugin.execute(capability, *args, **kwargs)
        return False

    def get_plugin_caps(self, type):
        """Get list of all capabilities for plugin of a set type.

        Args:
            type: Type of plugin to get.

        Returns:
            List of all capabilities matching type.
        """
        result = []
        for plugin_name in self.PLUGINS:
            plugin = self.PLUGINS[plugin_name]
            if plugin.type == type:
                result.extend(plugin.capabilities)
        return sorted(result)

    def load_plugin(self, name):
        """Load module from system (by import).

        Args:
            name: Name of the module to import.

        Returns:
            Result of __import__ operation.
        """
        mod = __import__("module_%s" % name)
        return mod

    def get_string(self):
        """Get tabulated plugin information.

        Returns:
            String with formatted prettytable.
        """
        column_names = [
            "name",
            "type",
            "capabilities",
            "stable",
            "os_support",
            "required_parameters",
        ]
        pt = PrettyTable(column_names, junction_char="|", hrules=HEADER)
        for column in column_names:
            pt.align[column] = "l"
        for plugin_name in sorted(self.PLUGINS.keys()):
            name = self.PLUGINS[plugin_name].name
            type = self.PLUGINS[plugin_name].type
            stable = self.PLUGINS[plugin_name].stable
            capabilities = ", ".join(self.PLUGINS[plugin_name].capabilities)
            is_os_supported = self.PLUGINS[plugin_name].is_os_supported()
            required_parameters = ", ".join(
                self.PLUGINS[plugin_name].required_parameters
            )
            row = [
                name,
                type,
                capabilities,
                stable,
                is_os_supported,
                required_parameters,
            ]
            pt.add_row(row)
        return pt.get_string()

    def get_dict(self):
        """Get dictionary with plugin information.

        Returns:
            Dictionary with information about plugins.
        """
        result = {}
        for plugin_name in sorted(self.PLUGINS.keys()):
            name = self.PLUGINS[plugin_name].name
            type = self.PLUGINS[plugin_name].type
            stable = self.PLUGINS[plugin_name].stable
            capabilities = self.PLUGINS[plugin_name].capabilities
            is_os_supported = self.PLUGINS[plugin_name].is_os_supported()
            required_parameters = self.PLUGINS[plugin_name].required_parameters
            result[plugin_name] = {
                "name": name,
                "type": type,
                "stable": stable,
                "capabilities": capabilities,
                "os_support": is_os_supported,
                "required_parameters": required_parameters,
            }
        return result

    def __str__(self):
        """Return prettytable formatted data."""
        return self.get_string()
