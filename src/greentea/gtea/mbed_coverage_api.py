#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import os

"""
def __default_coverage_start_callback(self, key, value, timestamp):
    # {{__coverage_start;PATH;PAYLOAD}}
    # PAYLAODED is HEX coded string
    lcov_path, lcov_payload = value.split(';')
    try:
        bin_payload = coverage_pack_hex_payload(lcov_payload)
        coverage_dump_file(lcov_path, bin_payload)

        self.log("dumped %d bytes to '%s'"% (len(bin_payload), lcov_path))
    except Exception as e:
        self.log("LCOV:" + str(e))
"""


def coverage_pack_hex_payload(payload):
    """! Convert a block of hex string data back to binary and return the binary data
    @param payload String with hex encoded ascii data, e.g.: '6164636772...'
    @return bytearray with payload with data
    """
    # This payload might be packed with dot compression
    # where byte value 0x00 is coded as ".", and not as "00"
    payload = payload.replace(".", "00")

    hex_pairs = map(
        "".join, zip(*[iter(payload)] * 2)
    )  # ['61', '64', '63', '67', '72', ... ]
    bin_payload = bytearray([int(s, 16) for s in hex_pairs])
    return bin_payload


def coverage_dump_file(build_path, path, payload):
    """! Creates file and dumps payload to it on specified path (even if path doesn't exist)
    @param path Path to file
    @param payload Binary data to store in a file
    @return True if operation was completed
    """
    result = True
    try:
        d, filename = os.path.split(path)
        if not os.path.isabs(d) and not os.path.exists(d):
            # For a relative path that does not exist. Try adding ./build/<target> prefix
            d = build_path
            path = os.path.join(d, filename)
        if not os.path.exists(d):
            os.makedirs(d)
        with open(path, "wb") as f:
            f.write(payload)
    except IOError as e:
        print(str(e))
        result = False
    return result
