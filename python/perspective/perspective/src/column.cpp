/******************************************************************************
 *
 * Copyright (c) 2020, the Perspective Authors.
 *
 * This file is part of the Perspective library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */
#ifdef PSP_ENABLE_PYTHON

#include <perspective/first.h>
#include <perspective/column.h>
#include <perspective/base.h>
#include <perspective/python/column.h>
#include <perspective/python/base.h>

namespace perspective {

template <>
void t_column::object_copied<PSP_OBJECT_TYPE>(std::uint64_t ptr) const {
    static int x = 0;
    // get what was there and incref if can
    py::print("incrementing ", ptr);
    // if (x > 0)
    //     assert(false);
    if (ptr){
        py::handle handle = reinterpret_cast<PSP_OBJECT_TYPE>(ptr);
        handle.inc_ref();
        x += 1;
    } else {
        assert(false);
    }
}

template <>
void t_column::object_cleared<PSP_OBJECT_TYPE>(std::uint64_t ptr) const {
    static int x = 0;
    // get what was there and decref if can
    py::print("decrementing ", ptr);
    // if (x > 0)
    //     assert(false);
    // assert(false);
    if (ptr){
        py::handle handle = reinterpret_cast<PSP_OBJECT_TYPE>(ptr);
        handle.dec_ref();
        x += 1;
    } else {
        assert(false);
    }
}
}

#endif