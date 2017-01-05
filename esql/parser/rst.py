from typing import List
from esql.parser import ast
from esql.parser.ast import TK
from esql.parser.utility import *


class Node(object):
    """ Abstract base class for RST nodes.
    """
    __slots__ = ()


class TableName(Node):
    __slots__ = ('index_name', 'doc_type')

    def __init__(self, tree):
        for item in tree:
            if item.type == TK.DOT:
                self.index_name = item.c0.value
                self.doc_type = item.c1.value


class FieldDefine(Node):
    __slots__ = ('name', 'type')

    def __init__(self, tree: ast.Element = None):
        if tree.type == TK.COLUMN_DEFINE:
            self.name = tree.value
            self.type = tree.c0.value


class TableCreate(Node):
    """ Create Table
    """
    __slots__ = ('table', 'fields')

    def __init__(self, tree, table: TableName = None, fields: List[FieldDefine] = None):
        self.table = table
        self.fields = fields or []

        for item in tree.children:
            if item.type == TK.TABLE_NAME:
                self.table = TableName(item.children)
            elif item.type == TK.TABLE_COLUMNS:
                for field_tree in item.children:
                    self.fields.append(FieldDefine(field_tree))
