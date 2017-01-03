
from typing import List


class Node(object):
    """ Abstract base class for AST nodes.
    """
    __slots__ = ()


class TableName(Node):
    __slots__ = ('index_name', 'doc_type')

    def __init__(self, index_name=None, doc_type=None):
        self.index_name = index_name
        self.doc_type = doc_type


class FieldName(Node):
    __slots__ = ('name', 'is_object')

    def __init__(self, name=None, is_object: bool=None):
        self.name = name
        self.is_object = is_object


FieldNameList = List[FieldName]


class FieldNames(Node, FieldNameList):
    """ FieldName List
    """


class FieldValues(Node, list):
    """ FieldValue List
    """


class ShowVersion(Node):
    """ SHOW VERSION
    """
    __slots__ = ()


class Insert(Node):
    """ INSERT
    """
    __slots__ = ('table', 'fields', 'values')

    def __init__(self, table: TableName = None, fields: FieldNames = None, values: FieldValues = None):
        self.table = table
        self.fields = fields
        self.values = values

        if len(fields) != len(values):
            raise Exception('Number columns or values error!')

# class Query(Node):
#     """ SELECT
#     """
#     __slots__ = ('select', 'from', 'conditions', 'groups', 'limits', 'orders', 'scores', 'highlights')
