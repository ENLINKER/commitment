
import sys

from pyring.one_time import PrivateKey


def get_object_size(obj):
    if type(obj) is list:
        return get_list_size(obj)
    elif type(obj) is dict:
        return get_dict_size(obj)
    elif type(obj) is PrivateKey:
        return sys.getsizeof(obj.as_bytes())
    else:
        return sys.getsizeof(obj)


def get_list_size(obj):
    assert (obj is not None)
    ct = 0
    for o in obj:
        ct += get_object_size(o)
    return ct


def get_dict_size(obj):
    assert (obj is not None)
    ct = 0
    for k, v in obj.items():
        ct += get_object_size(k) + get_object_size(v)
    return ct
