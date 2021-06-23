#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Host test to check if echo response matches sent data."""

import uuid
from .. import BaseHostTest


class EchoTest(BaseHostTest):
    """Implementation of echo host test."""

    __result = None
    echo_count = 0
    count = 0
    uuid_sent = []
    uuid_recv = []

    def __send_echo_uuid(self):
        """Send uuid to DUT."""
        if self.echo_count:
            str_uuid = str(uuid.uuid4())
            self.send_kv("echo", str_uuid)
            self.uuid_sent.append(str_uuid)
            self.echo_count -= 1

    def _callback_echo(self, key, value, timestamp):
        """Handle received echo kv pair."""
        self.uuid_recv.append(value)
        self.__send_echo_uuid()

    def _callback_echo_count(self, key, value, timestamp):
        """Handle received echo_count kv pair."""
        # Handshake
        self.echo_count = int(value)
        self.send_kv(key, value)
        # Send first echo to echo server on DUT
        self.__send_echo_uuid()

    def setup(self):
        """Register callbacks."""
        self.register_callback("echo", self._callback_echo)
        self.register_callback("echo_count", self._callback_echo_count)

    def result(self):
        """Check if sent and received uuid(s) match.

        Returns:
            True if uuid(s) match, else False.
        """
        self.__result = self.uuid_sent == self.uuid_recv
        return self.__result

    def teardown(self):
        """No teardown required."""
        pass
