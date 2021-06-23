#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Host test measuring deviation between microsecond ticks."""
from .. import BaseHostTest


class WaitusTest(BaseHostTest):
    """Read single characters from stdio and measure time between occurrences."""

    __result = None
    DEVIATION = 0.10  # +/-10%
    ticks = []

    def _callback_exit(self, key, value, timeout):
        self.notify_complete()

    def _callback_tick(self, key, value, timestamp):
        """Append tick of format: {{tick;%d}} to list."""
        self.log("tick! " + str(timestamp))
        self.ticks.append((key, value, timestamp))

    def setup(self):
        """Register callbacks."""
        self.register_callback("exit", self._callback_exit)
        self.register_callback("tick", self._callback_tick)

    def result(self):
        """Check if all tick deltas were within allowed deviation.

        Returns:
            True if delta between each tick was within DEVIATION, else False.
        """

        def sub_timestamps(t1, t2):
            """Check if delta between timestamps is within allowed deviation.

            Args:
                t1: Timestamp of later tick.
                t2: Timestamp of earlier tick.

            Returns:
                True if delta is in allowed deviation, else False.
            """
            delta = t1 - t2
            deviation = abs(delta - 1.0)
            # return True if delta > 0 and deviation <= self.DEVIATION else False
            return deviation <= self.DEVIATION

        # Check if time between ticks was accurate
        if self.ticks:
            # If any ticks were recorded
            timestamps = [timestamp for _, _, timestamp in self.ticks]
            self.log(str(timestamps))
            m = map(sub_timestamps, timestamps[1:], timestamps[:-1])
            self.log(str(m))
            self.__result = all(m)
        else:
            self.__result = False
        return self.__result

    def teardown(self):
        """No teardown required."""
        pass
