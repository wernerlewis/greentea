#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Null Host Test."""
from .. import BaseHostTest


class DevNullTest(BaseHostTest):
    """Null Host Test."""

    __result = None

    def _callback_result(self, key, value, timestamp):
        # We should not see result data in this test
        self.__result = False

    def _callback_to_stdout(self, key, value, timestamp):
        self.__result = True
        self.log("_callback_to_stdout !")

    def setup(self):
        """Register callbacks."""
        self.register_callback("end", self._callback_result)
        self.register_callback("to_null", self._callback_result)
        self.register_callback("to_stdout", self._callback_to_stdout)

    def result(self):
        """Get result for test.

        Returns:
            True if to_stdout received, False if to_null or end received, else None.
        """
        return self.__result
