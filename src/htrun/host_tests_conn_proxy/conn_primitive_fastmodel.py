#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Basic connector interface for use with fastmodels."""
from .conn_primitive import ConnectorPrimitive, ConnectorPrimitiveException


class FastmodelConnectorPrimitive(ConnectorPrimitive):
    """Connector interface for use with fastmodels."""

    def __init__(self, name, config):
        """Initialise object."""
        ConnectorPrimitive.__init__(self, name)
        self.config = config
        self.fm_config = config.get("fm_config", None)
        self.platform_name = config.get("platform_name", None)
        self.image_path = config.get("image_path", None)
        self.polling_timeout = int(config.get("polling_timeout", 60))

        # FastModel Agent tool-kit
        self.fm_agent_module = None
        self.resource = None

        # Initialize FastModel
        if self.__fastmodel_init():

            # Equivalent to DUT connection, flashing and reset...
            self.__fastmodel_launch()
            self.__fastmodel_load(self.image_path)
            self.__fastmodel_run()

    def __fastmodel_init(self):
        """Initialise models using fm_agent APIs.

        Returns:
            True on success.

        Raises:
            ConnectorPrimitiveException if fm_agent cannot be loaded or initialised.
        """
        self.logger.prn_inf("Initializing FastModel...")

        try:
            self.fm_agent_module = __import__("fm_agent")
        except ImportError as e:
            self.logger.prn_err(
                "unable to load mbed-fastmodel-agent module. "
                "Check the module installed correctly."
            )
            self.fm_agent_module = None
            self.logger.prn_err("Importing failed : %s" % str(e))
            raise ConnectorPrimitiveException("Importing failed : %s" % str(e))
        try:
            self.resource = self.fm_agent_module.FastmodelAgent(logger=self.logger)
            self.resource.setup_simulator(self.platform_name, self.fm_config)
            if self.__resource_allocated():
                pass
        except self.fm_agent_module.SimulatorError as e:
            self.logger.prn_err("module fm_agent, create() failed: %s" % str(e))
            raise ConnectorPrimitiveException(
                "FastModel Initializing failed as throw SimulatorError!"
            )

        return True

    def __fastmodel_launch(self):
        """Launch the FastModel.

        Raises:
            ConnectorPrimitiveException if fails to start simulator.
        """
        self.logger.prn_inf("Launching FastModel...")
        try:
            if not self.resource.start_simulator():
                raise ConnectorPrimitiveException(
                    "FastModel running failed, start_simulator() returned False!"
                )
        except self.fm_agent_module.SimulatorError as e:
            self.logger.prn_err("start_simulator() failed: %s" % str(e))
            raise ConnectorPrimitiveException(
                "FastModel launching failed as throw FastModelError!"
            )

    def __fastmodel_run(self):
        """Use fm_agent API to run the FastModel.

        Raises:
            ConnectorPrimitiveException if fails to run simulator.
        """
        self.logger.prn_inf("Running FastModel...")
        try:
            if not self.resource.run_simulator():
                raise ConnectorPrimitiveException(
                    "FastModel running failed, run_simulator() returned False!"
                )
        except self.fm_agent_module.SimulatorError as e:
            self.logger.prn_err("run_simulator() failed: %s" % str(e))
            raise ConnectorPrimitiveException(
                "FastModel running failed as throw SimulatorError!"
            )

    def __fastmodel_load(self, filename):
        """Use fm_agent API to load image to FastModel.

        Functional equivalent to flashing DUT.

        Raises:
            ConnectorPrimitiveException if fails to load simulator.
        """
        self.logger.prn_inf("loading FastModel with image '%s'..." % filename)
        try:
            if not self.resource.load_simulator(filename):
                raise ConnectorPrimitiveException(
                    "FastModel loading failed, load_simulator() returned False!"
                )
        except self.fm_agent_module.SimulatorError as e:
            self.logger.prn_err("run_simulator() failed: %s" % str(e))
            raise ConnectorPrimitiveException(
                "FastModel loading failed as throw SimulatorError!"
            )

    def __resource_allocated(self):
        """Check whether FastModel resource has been allocated.

        Returns:
            True if resource allocated, else False.
        """
        if self.resource:
            return True
        else:
            self.logger.prn_err("FastModel resource not available!")
            return False

    def read(self, count):
        """Read data from FastModel.

        Args:
            count: not used for FastModel.

        Returns:
            Data read from fastmodel, False if resource not allocated.
        """
        if self.__resource_allocated():
            try:
                data = self.resource.read()
            except self.fm_agent_module.SimulatorError as e:
                self.logger.prn_err(
                    "FastmodelConnectorPrimitive.read() failed: %s" % str(e)
                )
            else:
                return data
        else:
            return False

    def write(self, payload, log=False):
        """Write to FastModel.

        Args:
            payload: data to write to the DUT.
            log: If true, log the transmission.

        Returns:
            True if successful, else False.
        """
        if self.__resource_allocated():
            if log:
                self.logger.prn_txd(payload)
            try:
                self.resource.write(payload)
            except self.fm_agent_module.SimulatorError as e:
                self.logger.prn_err(
                    "FastmodelConnectorPrimitive.write() failed: %s" % str(e)
                )
            else:
                return True
        else:
            return False

    def flush(self):
        """Not supported with FastModel."""
        pass

    def connected(self):
        """Check if FastModel is connected.

        Returns:
            True if FastModel is connected.
        """
        if self.__resource_allocated():
            return self.resource.is_simulator_alive
        else:
            return False

    def finish(self):
        """Shutdown the FastModel and release the allocation."""
        if self.__resource_allocated():
            try:
                self.resource.shutdown_simulator()
                self.resource = None
            except self.fm_agent_module.SimulatorError as e:
                self.logger.prn_err(
                    "FastmodelConnectorPrimitive.finish() failed: %s" % str(e)
                )

    def reset(self):
        """Reset fastmodel simulator."""
        if self.__resource_allocated():
            try:
                if not self.resource.reset_simulator():
                    self.logger.prn_err(
                        "FastModel reset failed, reset_simulator() return False!"
                    )
            except self.fm_agent_module.SimulatorError as e:
                self.logger.prn_err(
                    "FastmodelConnectorPrimitive.reset() failed: %s" % str(e)
                )

    def __del__(self):
        """Shutdown fastmodel before deletion."""
        self.finish()
