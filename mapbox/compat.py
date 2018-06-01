import sys

if sys.version_info[0] >= 3:  # pragma: no cover
    string_type = str
else:  # pragma: no cover
    string_type = basestring
