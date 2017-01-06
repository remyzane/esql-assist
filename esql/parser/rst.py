from typing import List
from esql.parser import ast
from esql.parser.ast import TK
from esql.parser.utility import *


class Node(object):
    """ Abstract base class for RST nodes.
    """
    __slots__ = ()


class NodeList(list):
    """ Node List
    """


class TableName(Node):
    __slots__ = ('index_name', 'doc_type')

    def __init__(self, tree):
        for item in tree:
            if item.type == TK.DOT:
                self.index_name = item.c0.value
                self.doc_type = item.c1.value


class FieldDefine(Node):
    __slots__ = ('name', 'type', 'fields')

    def __init__(self, tree: ast.Element = None):
        if tree.type == TK.COLUMN_DEFINE:
            self.name = tree.value
            self.type = tree.c0.value
            if self.type == 'object' and tree.c1.children and tree.c1.type == TK.TABLE_COLUMNS:
                self.fields = FieldsDefine(tree.c1.children)

    def dsl(self):
        field = {'type': self.type}
        if hasattr(self, 'fields'):
            field['properties'] = self.fields.dsl()
        return field


class FieldsDefine(NodeList):

    def __init__(self, fields: List[ast.Element] = None):
        for field in fields:
            self.append(FieldDefine(field))

    def dsl(self):
        properties = {}
        for field in self:
            properties[field.name] = field.dsl()
        return properties


class TableCreate(Node):
    """ Create Table
    """
    __slots__ = ('table', 'fields')

    def __init__(self, tree, table: TableName = None, fields: List[FieldDefine] = None):
        self.table = table
        self.fields = fields or []

        for child in tree.children:
            if child.type == TK.TABLE_NAME:
                self.table = TableName(child.children)
            elif child.type == TK.TABLE_COLUMNS:
                self.fields = FieldsDefine(child.children)
