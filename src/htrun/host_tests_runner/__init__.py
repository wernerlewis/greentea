#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Basic host test implementations wiht flash and reset algorithms.

Functionality can be overridden by set of plugins which can provide specialised
flashing and reset implementations.
"""

from pkg_resources import get_distribution

__version__ = get_distribution("greentea").version
