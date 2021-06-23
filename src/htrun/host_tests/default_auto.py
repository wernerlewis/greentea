#
# Copyright (c) 2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Host Test class with no supervision."""
from .. import BaseHostTest


class DefaultAuto(BaseHostTest):
    """Basic Host Test with no supervision.

    Test runner will wait for serial port output from MUT, with no supervision during
    execution on MUT.
    """

    pass
