
import sys


def get_list_size(obj):
    if not obj:
        return 0
    return sys.getsizeof(obj[0]) * len(obj)


def get_dict_size(obj):
    if not obj:
        return 0
    ct = 0
    for k, v in enumerate(obj):
        ct += sys.getsizeof(k) + sys.getsizeof(v)
    return ct
