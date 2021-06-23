#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Base classes for implementing host test classes."""
import inspect
import six
from time import time
from inspect import isfunction, ismethod


class BaseHostTestAbstract:
    """Abstract base class for host tests, with setup, test, and teardown methods.

    Attributes:
        name: Name of the host test, used for local registration.
        script_location: Path to the source file the host test is loaded from.
    """

    name = ""  # name of the host test (used for local registration)
    __event_queue = None  # To main even loop
    __dut_event_queue = None  # To DUT
    script_location = None  # Path to source file used to load host test
    __config = {}

    def __notify_prn(self, text):
        if self.__event_queue:
            self.__event_queue.put(("__notify_prn", text, time()))

    def __notify_conn_lost(self, text):
        if self.__event_queue:
            self.__event_queue.put(("__notify_conn_lost", text, time()))

    def __notify_sync_failed(self, text):
        if self.__event_queue:
            self.__event_queue.put(("__notify_sync_failed", text, time()))

    def __notify_dut(self, key, value):
        """Send data over serial to DUT."""
        if self.__dut_event_queue:
            self.__dut_event_queue.put((key, value, time()))

    def notify_complete(self, result=None):
        """Notify main event loop that host test finished processing.

        Args:
            result: True if success, False if failure. If None, no action in main event
            loop.
        """
        if self.__event_queue:
            self.__event_queue.put(("__notify_complete", result, time()))

    def reset_dut(self, value):
        """Reset device under test.

        Args:
            value: Value representing reset type.
        """
        if self.__event_queue:
            self.__event_queue.put(("__reset_dut", value, time()))

    def reset(self):
        """Reset the device under test and continue running the host test."""
        if self.__event_queue:
            self.__event_queue.put(("__reset", "0", time()))

    def notify_conn_lost(self, text):
        """Notify main event loop of a DUT-host test connection error.

        Args:
            text: Text to be added to the event queue.
        """
        self.__notify_conn_lost(text)

    def log(self, text):
        """Send log message to main event loop.

        Args:
            text: Log message to send.
        """
        self.__notify_prn(text)

    def send_kv(self, key, value):
        """Send Key-Value data to DUT.

        Args:
            key: Key to send.
            value: Value to send.
        """
        self.__notify_dut(key, value)

    def setup_communication(self, event_queue, dut_event_queue, config={}):
        """Configure class for communication.

        Args:
            event_queue: Main event loop queue.
            dut_event_queue: Event queue for communication with DUT.
            config: Dictionary object storing configuration data.
        """
        self.__event_queue = event_queue
        self.__dut_event_queue = dut_event_queue
        self.__config = config

    def get_config_item(self, name):
        """Get an item from the host test configuration.

        Args:
            name: Key of the item to get.

        Returns:
            Value from the config.
        """
        return self.__config.get(name, None)

    def setup(self):
        """Register tests and callbacks."""
        raise NotImplementedError

    def result(self):
        """Return host test result."""
        raise NotImplementedError

    def teardown(self):
        """Teardown test. Blocking method."""
        raise NotImplementedError


def event_callback(key):
    """Define decorator for an event callback method.

    Args:
        key: value to assign to attribute "event_key".
    """

    def decorator(func):
        func.event_key = key
        return func

    return decorator


class HostTestCallbackBase(BaseHostTestAbstract):
    """Class implementing callbacks for HostTestBase."""

    def __init__(self):
        """Initialize object."""
        BaseHostTestAbstract.__init__(self)
        self.__callbacks = {}
        self.__restricted_callbacks = [
            "__coverage_start",
            "__testcase_start",
            "__testcase_finish",
            "__testcase_summary",
            "__exit",
            "__exit_event_queue",
        ]

        self.__consume_by_default = [
            "__coverage_start",
            "__testcase_start",
            "__testcase_finish",
            "__testcase_count",
            "__testcase_name",
            "__testcase_summary",
            "__rxd_line",
        ]

        self.__assign_default_callbacks()
        self.__assign_decorated_callbacks()

    def __callback_default(self, key, value, timestamp):
        # self.log("CALLBACK: key=%s, value=%s, timestamp=%f"% (key, value, timestamp))
        pass

    def __default_end_callback(self, key, value, timestamp):
        self.notify_complete(value == "success")

    def __assign_default_callbacks(self):
        for key in self.__consume_by_default:
            self.__callbacks[key] = self.__callback_default
        self.register_callback("end", self.__default_end_callback)

    def __assign_decorated_callbacks(self):
        """Register callback methods decorated with @event_callback.

        Example:
        Define a method with @event_callback decorator:

         @event_callback('<event key>')
         def event_handler(self, key, value, timestamp):
            do something..
        """
        for name, method in inspect.getmembers(self, inspect.ismethod):
            key = getattr(method, "event_key", None)
            if key:
                self.register_callback(key, method)

    def register_callback(self, key, callback, force=False):
        """Register callback for a specific event.

        Args:
            key: String with name of the event.
            callback: Callable which will be registered for event "key".
            force: If True, don't check if key is reserved or restricted.
        """
        if type(key) is not str:
            raise TypeError("event non-string keys are not allowed")

        if not callable(callback):
            raise TypeError("event callback should be callable")

        # Check if callback has all required parameters
        # If callback is a class method, it should have 4 arguments
        # (self, key, value, timestamp)
        if ismethod(callback):
            arg_count = six.get_function_code(callback).co_argcount
            if arg_count != 4:
                err_msg = "callback 'self.%s('%s', ...)' defined with %d arguments" % (
                    callback.__name__,
                    key,
                    arg_count,
                )
                err_msg += (
                    ", should have 4 arguments: self.%s(self, key, value, timestamp)"
                    % callback.__name__
                )
                raise TypeError(err_msg)

        # If callback is a function, it should have 3 arguments (key, value, timestamp)
        if isfunction(callback):
            arg_count = six.get_function_code(callback).co_argcount
            if arg_count != 3:
                err_msg = "callback '%s('%s', ...)' defined with %d arguments" % (
                    callback.__name__,
                    key,
                    arg_count,
                )
                err_msg += (
                    ", should have 3 arguments: %s(key, value, timestamp)"
                    % callback.__name__
                )
                raise TypeError(err_msg)

        if not force:
            if key.startswith("__"):
                raise ValueError("event key starting with '__' are reserved")

            if key in self.__restricted_callbacks:
                raise ValueError(
                    "we predefined few callbacks you can't use e.g. '%s'" % key
                )

        self.__callbacks[key] = callback

    def get_callbacks(self):
        """Get registered callbacks.

        Returns:
            Dict with event name: callback pairs.
        """
        return self.__callbacks

    def setup(self):
        """Register tests and callbacks."""
        pass

    def result(self):
        """Return host test result."""
        pass

    def teardown(self):
        """Blocking, teardown test."""
        pass


class BaseHostTest(HostTestCallbackBase):
    """Base Class for Host Tests."""

    __BaseHostTest_Called = False

    def base_host_test_inited(self):
        """Ensure BaseHostTest has been initialized.

        Returns:
            True if constructor has been called, else False.
        """
        return self.__BaseHostTest_Called

    def __init__(self):
        """Initialize object."""
        HostTestCallbackBase.__init__(self)
        self.__BaseHostTest_Called = True
