from tests import case_files_re, get_test_cases, execute


def clear():
    use_case_group = get_test_cases(case_files_re)
    print()
    for case_file, use_case in use_case_group.items():
        print('    clearing ' + case_file + ' ...')
        for _item in use_case:
            sql = _item['sql']
            print(execute(sql))


def test_case():
    clear()
    global es_method


    # ESql.red_keys = True
    # ESql.root_allow_remote = False
    # use_case_group_do = get_test_cases(case_files_do)
    # use_case_group_clear = dict()
    # if 'do_clear_test' in globals() and do_clear_test:
    #     use_case_group_clear = get_test_cases(case_files_re)
    #     check_case_files_do(case_files_do + case_files_re)
    # else:
    #     check_case_files_do(case_files_do)
    #
    # print()
    # # create test
    # for file_path, use_case in use_case_group_do.items():
    #     print('    ' + file_path + ' ...')
    #     for item in use_case:
    #         do_use_case(item)
    #
    #
    # # clear test
    # for file_path, use_case in use_case_group_clear.items():
    #     print('    ' + file_path + ' ...')
    #     for item in use_case:
    #         do_use_case(item)
    #
    # Processor.es = es_method
