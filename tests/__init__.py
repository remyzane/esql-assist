
from esql.generator import execute
from tests.__utility import get_test_cases, check_case_files, show_error, show_difference, check_consistency

es_method = None
es_call_info = []

case_files_do = []
case_files_re = []
case_files_all = []

# do_clear_test = True

# DO: positive sequence;    RE: recover is inverted sequence execution
case_list = [
    ('DO',      'tc_schema/table_create.cson'),         # ----------  Schema
    ('RE',   'tc_schema/table_drop.cson'),

    ('DO',      'tc_data/insert.cson'),                 # ----------  Data
    ('DO',      'tc_data/select.cson'),
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
