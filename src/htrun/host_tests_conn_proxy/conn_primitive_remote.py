#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Basic connector interface for use with remote connections."""
import time
from .. import DEFAULT_BAUD_RATE
from .conn_primitive import ConnectorPrimitive


class RemoteConnectorPrimitive(ConnectorPrimitive):
    """Connector interface for remote clients (Global Resource Manager)."""

    def __init__(self, name, config, importer=__import__):
        """Initialise object."""
        ConnectorPrimitive.__init__(self, name)
        self.config = config
        self.target_id = self.config.get("target_id", None)
        self.grm_host = config.get("grm_host", None)
        self.grm_port = config.get("grm_port", None)
        if self.grm_port:
            self.grm_port = int(self.grm_port)
        self.grm_module = config.get("grm_module", "unknown")
        self.platform_name = config.get("platform_name", None)
        self.baudrate = config.get("baudrate", DEFAULT_BAUD_RATE)
        self.image_path = config.get("image_path", None)
        self.forced_reset_timeout = config.get("forced_reset_timeout", 0)
        self.allocate_requirements = {
            "platform_name": self.platform_name,
            "power_on": True,
            "connected": True,
        }

        if self.config.get("tags"):
            self.allocate_requirements["tags"] = {}
            for tag in config["tags"].split(","):
                self.allocate_requirements["tags"][tag] = True

        # Global Resource Mgr tool-kit
        self.remote_module = None
        self.selected_resource = None
        self.client = None

        # Initialize remote resource manager
        self.__remote_init(importer)

    def __remote_init(self, importer):
        """Initialise DUT using GRM APIs.

        Args:
            importer: Importer function to import GRM module.

        Returns:
            True if successfully initialises, else False.
        """
        # We want to load global resource manager module by name from command line
        try:
            self.remote_module = importer(self.grm_module)
        except ImportError as error:
            self.logger.prn_err(
                "unable to load global resource manager '%s' module!" % self.grm_module
            )
            self.logger.prn_err(str(error))
            self.remote_module = None
            return False

        self.logger.prn_inf(
            "remote resources initialization: remote(host=%s, port=%s)"
            % (self.grm_host, self.grm_port)
        )

        # Connect to remote global resource manager
        self.client = self.remote_module.create(host=self.grm_host, port=self.grm_port)

        # First get the resources
        resources = self.client.get_resources()
        self.logger.prn_inf("remote resources count: %d" % len(resources))

        # Query for available resource
        # Automatic selection and allocation of a resource
        try:
            self.selected_resource = self.client.allocate(self.allocate_requirements)
        except Exception as error:
            self.logger.prn_err(
                "can't allocate resource: '%s', reason: %s"
                % (self.platform_name, str(error))
            )
            return False

        # Remote DUT connection, flashing and reset...
        try:
            self.__remote_flashing(self.image_path, forceflash=True)
            self.__remote_connect(baudrate=self.baudrate)
            self.__remote_reset(delay=self.forced_reset_timeout)
        except Exception as error:
            self.logger.prn_err(str(error))
            self.__remote_release()
            return False
        return True

    def __remote_connect(self, baudrate=DEFAULT_BAUD_RATE):
        """Open remote connection to DUT."""
        self.logger.prn_inf(
            "opening connection to platform at baudrate='%s'" % baudrate
        )
        if not self.selected_resource:
            raise Exception("remote resource not exists!")
        try:
            serial_parameters = self.remote_module.SerialParameters(baudrate=baudrate)
            self.selected_resource.open_connection(parameters=serial_parameters)
        except Exception:
            self.logger.prn_inf("open_connection() failed")
            raise

    def __remote_disconnect(self):
        if not self.selected_resource:
            raise Exception("remote resource not exists!")
        try:
            if self.connected():
                self.selected_resource.close_connection()
        except Exception as error:
            self.logger.prn_err(
                "RemoteConnectorPrimitive.disconnect() failed, reason: " + str(error)
            )

    def __remote_reset(self, delay=0):
        """Use GRM remote API to reset DUT."""
        self.logger.prn_inf("remote resources reset...")
        if not self.selected_resource:
            raise Exception("remote resource not exists!")
        try:
            if self.selected_resource.reset() is False:
                raise Exception("remote resources reset failed!")
        except Exception:
            self.logger.prn_inf("reset() failed")
            raise

        # Post-reset sleep
        if delay:
            self.logger.prn_inf("waiting %.2f sec after reset" % delay)
            time.sleep(delay)

    def __remote_flashing(self, filename, forceflash=False):
        """Use GRM remote API to flash DUT."""
        self.logger.prn_inf("remote resources flashing with '%s'..." % filename)
        if not self.selected_resource:
            raise Exception("remote resource not exists!")
        try:
            if self.selected_resource.flash(filename, forceflash=forceflash) is False:
                raise Exception("remote resource flashing failed!")
        except Exception:
            self.logger.prn_inf("flash() failed")
            raise

    def read(self, count):
        """Read data from DUT.

        Args:
            count: number of bytes of data to read.

        Returns:
            Data read.
        """
        if not self.connected():
            raise Exception("remote resource not exists!")
        data = str()
        try:
            data = self.selected_resource.read(count)
        except Exception as error:
            self.logger.prn_err(
                "RemoteConnectorPrimitive.read(%d): %s" % (count, str(error))
            )
        return data

    def write(self, payload, log=False):
        """Write to DUT.

        Args:
            payload: data to write to the DUT.
            log: If true, log the transmission.

        Returns:
            True if successful, else False.
        """
        if self.connected():
            try:
                self.selected_resource.write(payload)
                if log:
                    self.logger.prn_txd(payload)
                return True
            except Exception as error:
                self.LAST_ERROR = "remote write error: %s" % str(error)
                self.logger.prn_err(str(error))
        return False

    def flush(self):
        """Flush ignored with remote target."""
        pass

    def allocated(self):
        """Check if resources allocated for remote target.

        Returns:
            True if resources allocated for remote target.
        """
        return (
            self.remote_module
            and self.selected_resource
            and self.selected_resource.is_allocated
        )

    def connected(self):
        """Check if connected to remote target.

        Returns:
            True if resources allocated and resource is connected, else False.
        """
        return self.allocated() and self.selected_resource.is_connected

    def __remote_release(self):
        try:
            if self.allocated():
                self.selected_resource.release()
                self.selected_resource = None
        except Exception as error:
            self.logger.prn_err(
                "RemoteConnectorPrimitive.release failed, reason: " + str(error)
            )

    def finish(self):
        """Disconnect and release the allocated resources."""
        if self.allocated():
            self.__remote_disconnect()
            self.__remote_release()

    def reset(self):
        """Reset the DUT."""
        self.__remote_reset(delay=self.forced_reset_timeout)

    def __del__(self):
        """Finish use of object before deletion."""
        self.finish()
