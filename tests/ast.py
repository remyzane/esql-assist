import cson
from esql import parser
from tests import get_test_cases, tests_data_path, check_consistency, show_difference


def test_cases():
    use_case_group = get_test_cases('ast')
    print()
    for case_file, use_case in use_case_group.items():
        print('    ' + case_file[len(tests_data_path) + 1:] + ' ...')
        for _item in use_case:
            sql = _item['sql']
            ast = parser.parse(sql)
            source = cson.loads(ast.cson())
            target = _item['ast']

            difference = check_consistency(source, target)
            if difference:
                show_difference(sql, source, target, 'ast', difference)
