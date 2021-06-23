#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Host test to check if DUT target name matches expectation."""
import re
from .. import BaseHostTest


class DetectPlatformTest(BaseHostTest):
    """Host test which checks if DUT target name matches expected."""

    PATTERN_MICRO_NAME = r"Target '(\w+)'"
    re_detect_micro_name = re.compile(PATTERN_MICRO_NAME)

    def result(self):
        """Not required in this test."""
        raise NotImplementedError

    def test(self, selftest):
        """Search for target name in DUT serial."""
        result = True

        c = selftest.mbed.serial_readline()  # {{start}} preamble
        if c is None:
            return selftest.RESULT_IO_SERIAL

        selftest.notify(c.strip())
        selftest.notify("HOST: Detecting target name...")

        c = selftest.mbed.serial_readline()
        if c is None:
            return selftest.RESULT_IO_SERIAL
        selftest.notify(c.strip())

        # Check for target name
        m = self.re_detect_micro_name.search(c)
        if m and len(m.groups()):
            micro_name = m.groups()[0]
            micro_cmp = selftest.mbed.options.micro == micro_name
            result = result and micro_cmp
            selftest.notify(
                "HOST: MUT Target name '%s', expected '%s'... [%s]"
                % (
                    micro_name,
                    selftest.mbed.options.micro,
                    "OK" if micro_cmp else "FAIL",
                )
            )

        for i in range(0, 2):
            c = selftest.mbed.serial_readline()
            if c is None:
                return selftest.RESULT_IO_SERIAL
            selftest.notify(c.strip())

        return selftest.RESULT_SUCCESS if result else selftest.RESULT_FAILURE
