
import os
import cson
from collections import OrderedDict

from esql.utility.configure import load_cson

tests_path = os.path.realpath(os.path.join(__file__, '..'))


def check_case_files(case_files):
    for case_file in case_files:
        assert os.path.exists(os.path.join(tests_path, case_file))

    for tc_path in os.listdir(tests_path):
        if tc_path.startswith('tc_'):
            for tc_file in os.listdir(os.path.join(tests_path, tc_path)):
                if tc_file.endswith('.yml'):
                    case_file = os.path.join(tc_path, tc_file)
                    if case_file not in case_files:
                        print(os.linesep + '    ' + case_file + ' --', end='')


def get_test_cases(case_files):
    unit_test_cases = OrderedDict()
    for cson_file in case_files:
        test_cases = load_cson(cson_file, tests_path)
        unit_test_cases[cson_file] = test_cases or []
    return unit_test_cases


def show_object(ast, title=None, indent=''):
    if title:
        print('%s%s %s %s' % (os.linesep, '-' * 30, title, os.linesep))
    if indent is None:
        print(ast)
    else:
        print('    ' + indent + cson.dumps(ast, indent=4).replace('\n', '\n    ' + indent))


def show_difference(sql, source, target, _type, difference, indent=''):
    print('%s------------ SQL: %s%s' % (os.linesep, '-' * 60, os.linesep))
    print(sql)
    show_object(source, 'run result [%s]' % _type, indent)
    show_object(target, ' use case [%s] ' % _type, indent)
    if difference:
        source_diff, target_diff = difference
        if source_diff is not target_diff:
            show_object(source_diff, ' diff in result ', indent)
            show_object(target_diff, 'diff in use case', indent)


def show_error(sql, message):
    print('%s    sql: %s%s' % (os.linesep, '-' * 60, os.linesep))
    print(sql)
    print('%s  error: %s%s' % (os.linesep, '-' * 60, os.linesep))
    print(message)


def clear_empty_item(dictionary, need_clear_items):
    for item in need_clear_items:
        if item in dictionary and dictionary[item] in (None, '', [], {}):
            dictionary.pop(item)


def check_consistency(source, target, ignores=None, can_ellipsis=False):
    if type(source) in (int, float, str, bool):
        if source != target:
            return source, target
        return
    elif type(source) in (list, tuple) and type(target) in (list, tuple):
        return check_consistency_list(source, target, ignores)
    elif type(source) is dict and type(target) is dict:
        return check_consistency_dict(source, target, ignores, can_ellipsis=can_ellipsis)
    elif source is target:
        return
    return source, target


def check_consistency_list(source, target, ignores=None):
    source_index = 0
    for target_index in range(0, len(target)):
        if source_index == len(source):
            # source complete traverse, but target not end
            if target[target_index] == '...' and target_index == len(target) - 1:
                return  # although target not complete traverse, but only the ellipsis.
            else:
                return source, target
        target_item = target[target_index]
        source_item = source[source_index]
        if target_item != '...':
            difference = check_consistency(source_item, target_item, ignores)
            if difference:
                return difference
            source_index += 1
        else:
            if target_index == len(target) - 1:
                return  # omit the ending

            target_next = target[target_index + 1]
            while source_index < len(source):
                if source_item == target_next:      # 'list', 'tuple', 'dict' also support '=='
                    break
                else:
                    source_index += 1
                    if source_index == len(source):
                        return source, target       # source complete traverse, but target not end
                    source_item = source[source_index]
            if source_item != target_next:
                return source, target
    # target complete traverse, but source not end
    if source_index < len(source):
        return source, target


def check_consistency_dict(source, target, ignores=None, can_ellipsis=False):
    if (not source and target) or (not target and source):
        return source, target
    if ignores:
        for ignore in ignores:
            source.pop(ignore, None)
            target.pop(ignore, None)
    allow_empty_items = ('groups', 'limits', 'highlights', 'conditions', 'scores', 'orders', 'alias', 'object', 'range')
    clear_empty_item(source, allow_empty_items)
    clear_empty_item(target, allow_empty_items)
    if can_ellipsis:
        for key in source.keys():
            if key not in target:
                source.pop(key)
    allow_omit = '...' in target    # omit some definition
    source_keys = source.keys()
    target_keys = target.keys()
    if not allow_omit:
        if set(source_keys).symmetric_difference(set(target_keys)):
            return source, target
    for source_key, source_value in source.items():
        if allow_omit and source_key not in target:
            continue
        difference = check_consistency(source_value, target[source_key], ignores)
        if difference:
            return difference
