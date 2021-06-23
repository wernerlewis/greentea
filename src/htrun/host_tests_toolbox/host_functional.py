#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Tools for handling DUT."""
import sys
import json

from time import sleep
from serial import Serial, SerialException

from .. import host_tests_plugins, DEFAULT_BAUD_RATE


def flash_dev(
    disk=None, image_path=None, copy_method="default", port=None, program_cycle_s=4
):
    """Flash device.

    Args:
        disk: Currently mounted device disk (mount point).
        image_path: Path to binary file for flashing.
        copy_method: Copy method to use.
        port: Port DUT is connected on.
        program_cycle_s: Seconds to sleep after flashing.

    Returns:
        Result from copy plugin.
    """
    if copy_method == "default":
        copy_method = "shell"
    result = False
    result = host_tests_plugins.call_plugin(
        "CopyMethod",
        copy_method,
        image_path=image_path,
        serial=port,
        destination_disk=disk,
    )
    sleep(program_cycle_s)
    return result


def reset_dev(
    port=None,
    disk=None,
    reset_type="default",
    reset_timeout=1,
    serial_port=None,
    baudrate=DEFAULT_BAUD_RATE,
    timeout=1,
    verbose=False,
):
    """Reset device.

    Args:
        port: Port DUT is connected on.
        disk: Currently mounted device disk (mount point).
        reset_type: Reset method to use.
        reset_timeout Switch -R <reset_timeout>.
        serial_port: If set, don't use Serial connection.
        baudrate: Serial port baudrate.
        timeout: Serial port timeout.
        verbose: Verbose mode.
    """
    result = False
    if not serial_port:
        try:
            with Serial(port, baudrate=baudrate, timeout=timeout) as serial_port:
                result = host_tests_plugins.call_plugin(
                    "ResetMethod", reset_type, serial=serial_port, disk=disk
                )
            sleep(reset_timeout)
        except SerialException as e:
            if verbose:
                print("%s" % (str(e)))
            result = False
    return result


def handle_send_break_cmd(
    port, disk, reset_type=None, baudrate=None, timeout=1, verbose=False
):
    """Reset platforms and print serial port output.

    Args:
        port: Port DUT is connected on.
        disk: Currently mounted device disk (mount point).
        reset_type: Reset method to use.
        baudrate: Serial port baudrate.
        timeout: Serial port timeout.
        verbose: Verbose mode.

    Returns:
        True if successful, else False.
    """
    if not reset_type:
        reset_type = "default"

    port_config = port.split(":")
    if len(port_config) == 2:
        # -p COM4:115200
        port = port_config[0]
        baudrate = int(port_config[1]) if not baudrate else baudrate
    elif len(port_config) == 3:
        # -p COM4:115200:0.5
        port = port_config[0]
        baudrate = int(port_config[1]) if not baudrate else baudrate
        timeout = float(port_config[2])

    # Use default baud rate value if not set
    if not baudrate:
        baudrate = DEFAULT_BAUD_RATE

    if verbose:
        print(
            "htrun: serial port configuration: %s:%s:%s"
            % (port, str(baudrate), str(timeout))
        )

    try:
        serial_port = Serial(port, baudrate=baudrate, timeout=timeout)
    except Exception as e:
        print("htrun: %s" % (str(e)))
        print(
            json.dumps(
                {
                    "port": port,
                    "disk": disk,
                    "baudrate": baudrate,
                    "timeout": timeout,
                    "reset_type": reset_type,
                },
                indent=4,
            )
        )
        return False

    serial_port.flush()
    # Reset using one of the plugins
    result = host_tests_plugins.call_plugin(
        "ResetMethod", reset_type, serial=serial_port, disk=disk
    )
    if not result:
        print("htrun: reset plugin failed")
        print(
            json.dumps(
                {
                    "port": port,
                    "disk": disk,
                    "baudrate": baudrate,
                    "timeout": timeout,
                    "reset_type": reset_type,
                },
                indent=4,
            )
        )
        return False

    print("htrun: serial dump started (use ctrl+c to break)")
    try:
        while True:
            test_output = serial_port.read(512)
            if test_output:
                sys.stdout.write("%s" % test_output)
            if "{end}" in test_output:
                if verbose:
                    print()
                    print("htrun: stopped (found '{end}' terminator)")
                break
    except KeyboardInterrupt:
        print("ctrl+c break")

    serial_port.close()
    return True
