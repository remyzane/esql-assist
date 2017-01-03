from tests import case_files_all, get_test_cases, execute


def test_case():
    use_case_group = get_test_cases(case_files_all)
    print()
    for case_file, use_case in use_case_group.items():
        print('    ' + case_file + ' ...')
        for _item in use_case:
            sql = _item['sql']
            print(execute(sql))