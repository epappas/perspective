# *****************************************************************************
#
# Copyright (c) 2019, the Perspective Authors.
#
# This file is part of the Perspective library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
import six
import sys
from perspective.table import Table
from datetime import date, datetime

class CustomObjectStore(object):
    def __init__(self, value):
        self._value = value

    def _psp_dtype_(self):
        return "object"

    def __int__(self):
        return int(self._value)

    def __repr__(self):
        return 'test'


t = CustomObjectStore(1)
data = {"a": [t]}

# one for `t`, one for `data`, one for argument to sys.getrefcount
assert sys.getrefcount(t) == 3

tbl = Table(data)
assert tbl.schema() == {"a": object}
assert tbl.size() == 1
assert tbl.view().to_dict() == {"a": [t]}


# Count references
# 1 for `t`, one for `data`, one for argument to sys.getrefcount, and one for the table
print(sys.getrefcount(t), " should be ", 4)
# assert sys.getrefcount(t) == 4

tbl.update([data])
assert tbl.view().to_dict() == {"a": [t, t]}
assert tbl.size() == 2

# 2 copies in the table now
print(sys.getrefcount(t), " should be ", 5)
# assert sys.getrefcount(t) == 5

tbl.update([data])
assert tbl.view().to_dict() == {"a": [t, t, t]}
assert tbl.size() == 3

# 3 copies in the table now
print(sys.getrefcount(t), " should be ", 6)   
# assert sys.getrefcount(t) == 6

tbl.update([data])
assert tbl.view().to_dict() == {"a": [t, t, t, t]}
assert tbl.size() == 4

# 4 copies in the table now
print(sys.getrefcount(t), " should be ", 7)   
# assert sys.getrefcount(t) == 6

tbl.clear()
assert tbl.view().to_dict() == {}
assert tbl.size() == 0
# # 1 for `t`, one for `data`, one for argument to sys.getrefcount
print(sys.getrefcount(t), " should be ", 3)
assert sys.getrefcount(t) == 3



