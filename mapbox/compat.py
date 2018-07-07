"""This module contains a block of code that ensures 
compatibility across Python 2.x and 3.x
"""

import sys

if sys.version_info[0] >= 3:  # pragma: no cover
    string_type = str
else:  # pragma: no cover
    string_type = basestring
