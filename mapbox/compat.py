# compatibility module.

import itertools
import sys


map = itertools.imap if sys.version_info < (3,) else map
