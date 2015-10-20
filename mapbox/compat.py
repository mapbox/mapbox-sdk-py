# compatibility module.

import itertools
import sys


map = itertools.imap if sys.version_info < (3,) else map
zip = itertools.izip if sys.version_info < (3,) else zip
