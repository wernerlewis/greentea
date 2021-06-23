#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Base connector interface."""
from ..host_tests_logger import HtrunLogger


class ConnectorPrimitiveException(Exception):
    """Base connector interface exception."""

    pass


class ConnectorPrimitive(object):
    """Base implementation of the connector interface."""

    def __init__(self, name):
        """Initialise base connector interface."""
        self.LAST_ERROR = None
        self.logger = HtrunLogger(name)
        self.polling_timeout = 60

    def write_kv(self, key, value):
        """Form and send Key-Value protocol message.

        Returns:
            buffer with K-V message sent to DUT on success, None on failure.
        """
        kv_buff = "{{%s;%s}}" % (key, value) + "\n"

        if self.write(kv_buff):
            self.logger.prn_txd(kv_buff.rstrip())
            return kv_buff
        else:
            return None

    def read(self, count):
        """Read data from DUT.

        Args:
            count: Number of bytes to read.
        Returns:
            Bytes read.
        """
        raise NotImplementedError

    def write(self, payload, log=False):
        """Write data to DUT.

        Args:
            payload: Buffer with data to send.
            log: Enable logging for this function.

        Returns:
            Payload sent, if possible to establish that.
        """
        raise NotImplementedError

    def flush(self):
        """Flush read/write channels of DUT."""
        raise NotImplementedError

    def reset(self):
        """Reset the DUT."""
        raise NotImplementedError

    def connected(self):
        """Check if there is a connection to DUT.

        Returns:
            True if read/write/flush API able to connect to DUT.
        """
        raise NotImplementedError

    def error(self):
        """Get last error received.

        Returns:
            Value of self.LAST_ERROR
        """
        return self.LAST_ERROR

    def finish(self):
        """Handle DUT destructor, close resource operations."""
        raise NotImplementedError
