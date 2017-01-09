import sys
from typing import Tuple
from esql import parser
from esql.utility import recursive_import
from esql.parser.ast import Element

# provide convenience for import in sub module
from esql.parser import ast, rst, TK

RstDict = None

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
    def __init__(self, sql, _ast: Element, _rst=None, explain_only=False):
        self.sql = sql
        self.ast = _ast
        self.rst = _rst
        self.explain_only = explain_only

    @staticmethod
    def execute(sql):
        _ast, explain_only = _parse(sql)
        _rst = None
        if _ast.type in RstDict:
            rst_class = RstDict[_ast.type]
            _rst = rst_class(_ast)

        processor_class = ProcessorDict.get(_ast.type, Processor)
        processor = processor_class(sql, _ast, _rst, explain_only)

        return processor.rst.dsl()


def init():
    global RstDict, ProcessorDict
    from esql import parser
    from esql.parser.rst import Node
    recursive_import(parser)
    RstDict = {}
    for rst_class in Node.__subclasses__():
        if hasattr(rst_class, 'mapping'):
            RstDict[rst_class.mapping] = rst_class
    
    recursive_import(sys.modules[__name__])
    ProcessorDict = {}
    for processor_class in Processor.__subclasses__():
        ProcessorDict[processor_class.mapping] = processor_class
