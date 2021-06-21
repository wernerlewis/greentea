#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Host test and test results classes."""
from sys import stdout

from .target_base import TargetBase
from . import __version__


class HostTestResults:
    """Implementation of methods for converting string results to specific integer."""

    RESULT_SUCCESS = "success"
    RESULT_FAILURE = "failure"
    RESULT_ERROR = "error"
    RESULT_END = "end"
    RESULT_UNDEF = "undefined"
    RESULT_TIMEOUT = "timeout"
    RESULT_IOERR_COPY = "ioerr_copy"
    RESULT_IOERR_DISK = "ioerr_disk"
    RESULT_IO_SERIAL = "ioerr_serial"
    RESULT_NO_IMAGE = "no_image"
    RESULT_NOT_DETECTED = "not_detected"
    RESULT_MBED_ASSERT = "mbed_assert"
    RESULT_PASSIVE = "passive"
    RESULT_BUILD_FAILED = "build_failed"
    RESULT_SYNC_FAILED = "sync_failed"

    def __init__(self):
        """Initialise object."""
        self.TestResultsList = [
            self.RESULT_SUCCESS,
            self.RESULT_FAILURE,
            self.RESULT_ERROR,
            self.RESULT_END,
            self.RESULT_UNDEF,
            self.RESULT_TIMEOUT,
            self.RESULT_IOERR_COPY,
            self.RESULT_IOERR_DISK,
            self.RESULT_IO_SERIAL,
            self.RESULT_NO_IMAGE,
            self.RESULT_NOT_DETECTED,
            self.RESULT_MBED_ASSERT,
            self.RESULT_PASSIVE,
            self.RESULT_BUILD_FAILED,
            self.RESULT_SYNC_FAILED,
        ]

    def get_test_result_int(self, test_result_str):
        """Map test result string to unique integer.

        Args:
            test_result_str: Test result in string format.

        Returns:
            Int representation of test result, or -1 if unknown.
        """
        if test_result_str in self.TestResultsList:
            return self.TestResultsList.index(test_result_str)
        return -1

    def __getitem__(self, test_result_str):
        """Return numerical result code of test result.

        Args:
            test_result_str: Test result in string format.
        """
        return self.get_test_result_int(test_result_str)


class Test(HostTestResults):
    """Base class for host test's test runner."""

    def __init__(self, options):
        """Initialise class."""
        HostTestResults.__init__(self)
        self.target = TargetBase(options)

    def run(self):
        """Execute test and forward results via serial port to test suite."""
        pass

    def setup(self):
        """Register tests and callbacks."""
        pass

    def notify(self, msg):
        """Notification, push message to stdout and flush buffer.

        Args:
            msg: Message to push to stdout.
        """
        stdout.write(msg)
        stdout.flush()

    def print_result(self, result):
        """Print test result notification.

        Args:
            result: Member of HostTestResults.RESULT_* to print.
        """
        self.notify("{{%s}}\n" % result)
        self.notify("{{%s}}\n" % self.RESULT_END)

    def finish(self):
        """Finish tasks and close resources."""
        pass

    def get_hello_string(self):
        """Get hello string to use as first print.

        Returns:
            String indicating htrun version.
        """
        return "host test executor ver. " + __version__


class DefaultTestSelectorBase(Test):
    """Test class with serial port initialisation.

    This is a base for other test selectors.
    """

    def __init__(self, options):
        """Initialise object."""
        Test.__init__(self, options=options)
