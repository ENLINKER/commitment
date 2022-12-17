
import sys

from pyring.one_time import PrivateKey


def get_object_size(obj):
    assert (type(obj) is not list and type(obj) is not dict)
    if type(obj) is PrivateKey:
        return sys.getsizeof(obj.as_bytes())
    else:
        return sys.getsizeof(obj)


def get_list_size(obj):
    assert (obj is not None)
    # if not obj:
    #     return 0
    ct = 0
    for o in obj:
        ct += get_object_size(o)
    return ct


def get_dict_size(obj):
    assert (obj is not None)
    # if not obj:
    #     return 0
    ct = 0
    for k, v in obj.items():
        ct += get_object_size(k) + get_object_size(v)
    return ct
