#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Hello World Host Test."""
from .. import BaseHostTest


class HelloTest(BaseHostTest):
    """Test if DUT correctly returns hello_world k-v pair."""

    HELLO_WORLD = "Hello World"

    __result = None

    def _callback_hello_world(self, key, value, timestamp):
        self.__result = value == self.HELLO_WORLD
        self.notify_complete()

    def setup(self):
        """Register hello_world callback."""
        self.register_callback("hello_world", self._callback_hello_world)

    def result(self):
        """Check if successfully received "hello_world" kv pair.

        Returns:
            True if key received with expected value, False if value not matching,
            None if key "hello_world" not received.
        """
        return self.__result

    def teardown(self):
        """No teardown required."""
        pass
