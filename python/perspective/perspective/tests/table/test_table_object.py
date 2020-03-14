# *****************************************************************************
#
# Copyright (c) 2019, the Perspective Authors.
#
# This file is part of the Perspective library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
import six
from perspective.table import Table
from datetime import date, datetime

class CustomObjectBlank(object):
    pass

class CustomObjectStore(object):
    def __init__(self, value):
        self._value = value

    def _psp_dtype_(self):
        return "object"

    def __int__(self):
        return int(self._value)

    def __repr__(self):
        return 'test'

class CustomObjectRepr(object):
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return str(self._value)

class CustomObjectIntPromoteToString(CustomObjectRepr):
    def _psp_dtype_(self):
        return int

class CustomObjectFloatPromoteToString(CustomObjectRepr):
    def _psp_dtype_(self):
        return float

class CustomObjectIntBoth(CustomObjectRepr):
    def _psp_dtype_(self):
        return int

    def _psp_repr_(self):
        return int(self._value) + 1

class CustomObjectFloatBoth(CustomObjectRepr):
    def _psp_dtype_(self):
        return float

    def _psp_repr_(self):
        return float(self._value) + 1.0

class CustomObjectIntConvert(CustomObjectRepr):
    def _psp_dtype_(self):
        return int

    def __int__(self):
        return int(self._value)

    def __repr__(self):
        return 'test'

class CustomObjectFloatConvert(CustomObjectRepr):
    def _psp_dtype_(self):
        return float

    def __float__(self):
        return float(self._value)

    def __repr__(self):
        return 'test'


class CustomObjectIntConvertFromFloat(CustomObjectRepr):
    def _psp_dtype_(self):
        return int

    def __float__(self):
        return float(self._value)

    def __repr__(self):
        return 'test'

class CustomObjectFloatConvertFromInt(CustomObjectRepr):
    def _psp_dtype_(self):
        return float

    def __int__(self):
        return int(self._value)

    def __repr__(self):
        return 'test'

class TestTableObjectsExtract(object):
    def test_table_custom_object(self):
        data = {"a": [CustomObjectBlank()]}
        tbl = Table(data)
        assert tbl.schema() == {"a": str}

        assert tbl.size() == 1
        assert '<perspective.tests.table.test_table_object.CustomObjectBlank object at 0x' in tbl.view().to_dict()["a"][0]

    def test_table_custom_object_repr(self):
        data = {"a": [CustomObjectRepr(1), CustomObjectRepr(2)]}
        tbl = Table(data)
        assert tbl.schema() == {"a": str}

        assert tbl.size() == 2
        assert tbl.view().to_dict() == {"a": ["1", "2"]}

    def test_table_custom_object_repr_update(self):
        data = {"a": [CustomObjectIntBoth(1), CustomObjectIntBoth(2)]}
        tbl = Table(data)
        assert tbl.schema() == {"a": int}
        assert tbl.size() == 2
        assert tbl.view().to_dict() == {"a": [2, 3]}

        tbl.update([{"a": CustomObjectIntBoth(3)}, {"a": CustomObjectIntBoth(4)}])
        assert tbl.size() == 4
        assert tbl.view().to_dict() == {"a": [2, 3, 4, 5]}

    def test_custom_object_int_promote_to_string(self):
        data = {"a": [CustomObjectIntPromoteToString(1), CustomObjectIntPromoteToString(2)]}
        tbl = Table(data)
        assert tbl.schema() == {"a": str}

        assert tbl.size() == 2
        assert tbl.view().to_dict() == {"a": ["1", "2"]}
   
    def test_custom_object_float_promote_to_string(self):
        data = {"a": [CustomObjectFloatPromoteToString(1), CustomObjectFloatPromoteToString(2)]}
        tbl = Table(data)
        assert tbl.schema() == {"a": str}

        assert tbl.size() == 2
        assert tbl.view().to_dict() == {"a": ["1", "2"]}
   
    def test_custom_object_int_both(self):
        data = {"a": [CustomObjectIntBoth(1), CustomObjectIntBoth(2)]}
        tbl = Table(data)
        assert tbl.schema() == {"a": int}

        assert tbl.size() == 2
        # We do value + 1 just to make sure
        assert tbl.view().to_dict() == {"a": [2, 3]}

    def test_custom_object_float_both(self):
        data = {"a": [CustomObjectFloatBoth(1), CustomObjectFloatBoth(2)]}
        tbl = Table(data)
        assert tbl.schema() == {"a": float}

        assert tbl.size() == 2
        # We do value + 1 just to make sure
        assert tbl.view().to_dict() == {"a": [2.0, 3.0]}

    def test_custom_object_int_convert(self):
        data = {"a": [CustomObjectIntConvert(1), CustomObjectIntConvert(2)]}
        tbl = Table(data)
        assert tbl.schema() == {"a": int}

        assert tbl.size() == 2
        assert tbl.view().to_dict() == {"a": [1, 2]}

    def test_custom_object_float_convert(self):
        data = {"a": [CustomObjectFloatConvert(1), CustomObjectFloatConvert(2)]}
        tbl = Table(data)
        assert tbl.schema() == {"a": float}

        assert tbl.size() == 2
        assert tbl.view().to_dict() == {"a": [1.0, 2.0]}

    def test_custom_object_int_convert_from_float(self):
        data = {"a": [CustomObjectIntConvertFromFloat(1), CustomObjectIntConvertFromFloat(2)]}
        tbl = Table(data)
        assert tbl.schema() == {"a": int}

        assert tbl.size() == 2
        assert tbl.view().to_dict() == {"a": [1, 2]}

    def test_custom_object_float_convert_from_int(self):
        data = {"a": [CustomObjectFloatConvertFromInt(1), CustomObjectFloatConvertFromInt(2)]}
        tbl = Table(data)
        assert tbl.schema() == {"a": float}
        assert tbl.size() == 2
        assert tbl.view().to_dict() == {"a": [1.0, 2.0]}
    
class TestTableObjectsStore(object):
    def test_object_passthrough(self):
        t = CustomObjectStore(1)
        t2 = CustomObjectStore(2)
        t3 = CustomObjectStore(3)

        data = {"a": [t, t2, t3]}
        tbl = Table(data)
        assert tbl.schema() == {"a": object}
        assert tbl.size() == 3
        assert tbl.view().to_dict() == {"a": [t, t2, t3]}
    


