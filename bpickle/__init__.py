"""
Copyright (c) 2006, Gustavo Niemeyer <gustavo@niemeyer.net>
Port to python 3 was done by Chris Glass <chris.glass@canonical.com>

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of the copyright holder nor the names of its
      contributors may be used to endorse or promote products derived from
      this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

This file is modified from the original to work with python3, but should be
wire compatible and behave the same way (bugs notwithstanding).
"""


dumps_table = {}
loads_table = {}


def dumps(obj, _dt=dumps_table):
    try:
        return _dt[type(obj)](obj).encode("UTF-8")
    except KeyError as e:
        raise ValueError("Unsupported type: %s" % e)


def loads(byte_string, _lt=loads_table):
    if not byte_string:
        raise ValueError("Can't load empty string")
    unicode_string = byte_string.decode()
    try:
        return _lt[unicode_string[0]](unicode_string, 0)[0]
    except KeyError as e:
        raise ValueError("Unknown type character: %s" % e)
    except IndexError:  #pragma: nocover
        # NOTE: Not sure if reachable (chrisglass during py3 conversion)
        raise ValueError("Corrupted data")


def dumps_bool(obj):
    return "b%d" % int(obj)


def dumps_int(obj):
    return "i%s;" % obj


def dumps_float(obj):
    return "f%r;" % obj


def dumps_str(obj):
    return "s%s:%s" % (len(obj), obj)


def dumps_list(obj, _dt=dumps_table):
    return "l%s;" % "".join([_dt[type(val)](val) for val in obj])


def dumps_tuple(obj, _dt=dumps_table):
    return "t%s;" % "".join([_dt[type(val)](val) for val in obj])


def dumps_dict(obj, _dt=dumps_table):
    keys = list(obj.keys())
    keys.sort()
    res = []
    append = res.append
    for key in keys:
        val = obj[key]
        append(_dt[type(key)](key))
        append(_dt[type(val)](val))
    return "d%s;" % "".join(res)


def dumps_none(obj):
    return "n"


def loads_bool(str, pos):
    return bool(int(str[pos+1])), pos+2


def loads_int(str, pos):
    endpos = str.index(";", pos)
    return int(str[pos+1:endpos]), endpos+1


def loads_float(str, pos):
    endpos = str.index(";", pos)
    return float(str[pos+1:endpos]), endpos+1


def loads_str(str, pos):
    startpos = str.index(":", pos)+1
    endpos = startpos+int(str[pos+1:startpos-1])
    return str[startpos:endpos], endpos


def loads_list(str, pos, _lt=loads_table):
    pos += 1
    res = []
    append = res.append
    while str[pos] != ";":
        obj, pos = _lt[str[pos]](str, pos)
        append(obj)
    return res, pos+1


def loads_tuple(str, pos, _lt=loads_table):
    pos += 1
    res = []
    append = res.append
    while str[pos] != ";":
        obj, pos = _lt[str[pos]](str, pos)
        append(obj)
    return tuple(res), pos+1


def loads_dict(str, pos, _lt=loads_table):
    pos += 1
    res = {}
    while str[pos] != ";":
        key, pos = _lt[str[pos]](str, pos)
        val, pos = _lt[str[pos]](str, pos)
        res[key] = val
    return res, pos+1


def loads_none(str, pos):
    return None, pos+1


dumps_table.update({       bool: dumps_bool,
                            int: dumps_int,
                          float: dumps_float,
                            str: dumps_str,
                           list: dumps_list,
                          tuple: dumps_tuple,
                           dict: dumps_dict,
                     type(None): dumps_none     })

loads_table.update({ "b": loads_bool,
                     "i": loads_int,
                     "f": loads_float,
                     "s": loads_str,
                     "u": loads_str,
                     "l": loads_list,
                     "t": loads_tuple,
                     "d": loads_dict,
                     "n": loads_none     })

