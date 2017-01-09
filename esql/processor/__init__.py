import sys
from typing import Tuple
from esql import parser
from esql.utility import recursive_import
from esql.parser.ast import Element

# provide convenience for import in sub module
from esql.parser import ast, rst, TK

ProcessorDict = None


def _parse(sql) -> Tuple[Element, bool]:
    _ast = parser.parse(sql)
    if _ast.type == TK.TOK_EXPLAIN:
        return _ast.sub(0), True
    else:
        return _ast, False


class Processor(object):
    """ RST & ES Mapping Generate
    """
    def __init__(self, sql, _ast: Element, explain_only=False):
        self.sql = sql
        self.ast = _ast
        self.explain_only = explain_only

    @staticmethod
    def execute(sql):
        _ast, explain_only = _parse(sql)
        processor_class = ProcessorDict[_ast.type]
        processor = processor_class(sql, _ast, explain_only)
        return processor.explain()


def init():
    global ProcessorDict
    recursive_import(sys.modules[__name__])
    ProcessorDict = {}
    for processor_class in Processor.__subclasses__():
        ProcessorDict[processor_class.mapping] = processor_class
