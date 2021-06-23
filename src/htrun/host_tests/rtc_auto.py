#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Real time clock host test."""
import re
from time import strftime, gmtime
from .. import BaseHostTest


class RTCTest(BaseHostTest):
    """Implementation of RTC host test."""

    PATTERN_RTC_VALUE = r"\[(\d+)\] \[(\d+-\d+-\d+ \d+:\d+:\d+ [AaPpMm]{2})\]"
    re_detect_rtc_value = re.compile(PATTERN_RTC_VALUE)

    __result = None
    timestamp = None
    rtc_reads = []

    def _callback_timestamp(self, key, value, timestamp):
        self.timestamp = int(value)

    def _callback_rtc(self, key, value, timestamp):
        self.rtc_reads.append((key, value, timestamp))

    def _callback_end(self, key, value, timestamp):
        self.notify_complete()

    def setup(self):
        """Register callbacks."""
        self.register_callback("timestamp", self._callback_timestamp)
        self.register_callback("rtc", self._callback_rtc)
        self.register_callback("end", self._callback_end)

    def result(self):
        """Check if all received timestamps are correct.

        Returns:
            True on success, else False.
        """

        def check_strftimes_format(t):
            """Check timestamp received matches regex and time is correct.

            Args:
                t: Value received in RTC kv pair.

            Returns:
                True if t matches format and time is correct, else False.
            """
            m = self.re_detect_rtc_value.search(t)
            if m and len(m.groups()):
                sec, time_str = int(m.groups()[0]), m.groups()[1]
                correct_time_str = strftime("%Y-%m-%d %H:%M:%S", gmtime(float(sec)))
                return time_str == correct_time_str
            return False

        ts = [t for _, t, _ in self.rtc_reads]
        self.__result = all(filter(check_strftimes_format, ts))
        return self.__result

    def teardown(self):
        """No teardown required."""
        pass
