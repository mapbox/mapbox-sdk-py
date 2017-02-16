# Python 2/3 compatibility

import sys

if sys.version_info >= (3, ):
    from urllib.parse import urlparse
    text_types = (str, )
else:
    from urlparse import urlparse
    text_types = (str, unicode)
