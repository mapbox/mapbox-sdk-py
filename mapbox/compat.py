# compatibility module.

import itertools
import sys


if sys.version_info < (3,):
    map = itertools.imap
else:
    map = itertools.map
