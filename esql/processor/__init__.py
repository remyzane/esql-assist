
import sys

from esql import parser
from esql.utility import recursive_import

# provide convenience for import in sub module
from esql.parser import ast, rst, TK

ProcessorDict = None


class Processor(object):
    """ RST & ES Mapping Generate
    """
    def __init__(self, sql):
        self.sql = sql

    def execute(self):
        return self.explain()


def init():
    global ProcessorDict
    recursive_import(sys.modules[__name__])
    ProcessorDict = {}
    for processor_class in Processor.__subclasses__():
        ProcessorDict[processor_class.mapping] = processor_class


def get_processor(sql):
    _ast = parser.parse(sql)
    processor_class = ProcessorDict[_ast.type]
    return processor_class(sql, _ast)


def explain(sql):
    return get_processor(sql).explain()


def execute(sql):
    return get_processor(sql).execute()
