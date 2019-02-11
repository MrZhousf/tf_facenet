# -*- coding:utf-8 -*-


def is_empty(obj):
    str_obj = str(obj)
    if str_obj is None or str_obj == 'None':
        return True
    if str_obj.strip() == '':
        return True
    return False


def is_not_empty(obj):
    str_obj = str(obj)
    if str_obj is None or str_obj == 'None':
        return False
    if str_obj.strip() == '':
        return False
    return True


def contain(obj, what):
    str_obj = str(obj)
    str_what = str(what)
    if is_not_empty(str_obj) and is_not_empty(str_what):
        if str_obj.find(str_what) >= 0:
            return True
    return False


def not_contain(obj, what):
    str_obj = str(obj)
    str_what = str(what)
    if is_not_empty(str_obj) and is_not_empty(str_what):
        if str_obj.find(str_what) >= 0:
            return False
    return True
