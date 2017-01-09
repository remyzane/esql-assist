

from ql.parse.ASTNode import Node as Element
# provide convenience for import in sub module
from ql.parse.parser import TOKEN as TK
from ql.parse import lexer as lexis
from ql.parse import parser as grammar
from esql.utility import AutoNumber


# def sub(elm, index) -> Element:
#     return elm.children[index]
#
#
# def sub_token(elm, _type) -> Element:
#     if elm.children:
#         for child in elm.children:
#             if child.type == _type:
#                 return child


# from collections import OrderedDict
#
# class Element(object):
#     """ Ast element
#     """
#
#     def __init__(self, _type, _value=None, children: list=None):
#         self.type = _type
#         self.value = _value
#         self.children = children
#
#         # provide convenience for coding
#         def _get_child_by_index(_children, index) -> Element:
#             return _children[index]
#         if children:
#             self.c0 = _get_child_by_index(children, 0)
#             children_len = len(children)
#             if children_len > 1:
#                 self.c1 = _get_child_by_index(children, 1)
#             if children_len > 2:
#                 self.c2 = _get_child_by_index(children, 2)
#
#     def tree(self):
#         """ Generate a serializable tree
#         """
#         ret = OrderedDict({'type': self.type.name})
#
#         if self.value and self.type not in [TK.TOK_DOT, TK.TOK_KEY_VALUE]:
#             ret['value'] = self.value
#
#         if self.children:
#             children_index = 0
#             for item in self.children:
#                 ret['c%d' % children_index] = item.tree()
#                 children_index += 1
#         return ret


# def transform(obj: ASTNode) -> Element:
#     """ Generate a ast element tree
#     """
#     if obj.children:
#         children = []
#         for child in obj.children:
#             children.append(transform(child))
#         return Element(TK[obj.tokType.name[4:]], obj.tokValue, children)
#     else:
#         return Element(TK[obj.tokType.name[4:]], obj.tokValue, obj.children)


# # generate TK class
# from ql.parse.parser import TOKEN
# print('class TK(AutoNumber):')
# for item in TOKEN:
#     print('    %s = ()' % item.name[4:])
#
#
# class TK(AutoNumber):
#     IDENTIFIER = ()
#     VALUE = ()
#     DOT = ()
#     CORE_TYPE = ()
#     SORT_MODE = ()
#     LIST = ()
#     DICT = ()
#     TUPLE = ()
#     EXPRESSION = ()
#     COLUMN_DEFINE = ()
#     META_DEFINE = ()
#     TABLE_COLUMNS = ()
#     TABLE_NAME = ()
#     TABLE_METAS = ()
#     TABLE_OPTIONS = ()
#     CREATE_TABLE = ()
#     QUERY = ()
#     FUNCTION = ()
#     KEY_VALUE = ()
#     COMPARE = ()
#     REVERSED = ()
#     COMPLEX = ()
#     SELECT = ()
#     FROM = ()
#     WHERE = ()
#     LIMIT = ()
#     ORDERBY = ()
#     GROUPBY = ()
#     SELEXPR = ()
#     SORT = ()
#     INSERT_INTO = ()
#     INSERT_COLUMNS = ()
#     BULK_INTO = ()
#     INSERT_ROW = ()
#     INSERT_ROWS = ()
#     UPSERT_INTO = ()
#     UPDATE = ()
#     SET_COLUMNS_CLAUSE = ()
