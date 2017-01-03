from tests import get_test_cases, execute


es_method = None
es_call_info = []

case_files_do = []
case_files_re = []
case_files_all = []

# do_clear_test = True

# DO: positive sequence;    RE: recover is inverted sequence execution
case_list = [
    ('DO',  'data/elastic/table_create.cson'),          # ----------  Schema
    ('RE',  'data/elastic/table_drop.cson'),

    ('DO',  'data/elastic/data_insert.cson'),           # ----------  Data
    ('DO',  'data/elastic/data_select.cson'),
]

for operation, item in case_list:
    if operation == 'DO':
        case_files_do.append(item)
        case_files_all.append(item)

# inverted sequence
case_list.reverse()

for operation, item in case_list:
    if operation == 'RE':
        case_files_re.append(item)
        case_files_all.append(item)



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
    use_case_group = get_test_cases(case_files_all)
    print()
    for case_file, use_case in use_case_group.items():
        print('    ' + case_file + ' ...')
        for _item in use_case:
            sql = _item['sql']
            print(execute(sql))


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
