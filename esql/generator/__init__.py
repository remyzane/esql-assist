
import sys

from esql import parser
from esql.utility import recursive_import

# provide convenience for import in sub module
from esql.parser import rst

GeneratorDict = None


class Generator(object):
    """ Generate ES Mapping from RST
    """


def init():
    global GeneratorDict
    recursive_import(sys.modules[__name__])
    GeneratorDict = {}
    for processor_class in Generator.__subclasses__():
        GeneratorDict[processor_class.__name__.upper()] = processor_class


def has_jobs(items):
    pass


def execute(sql):
    ast = parser.parse(sql)

    print(ast.cson())



    # generator_class = GeneratorDict[parser.get_ast_sign(_ast)]
    # _generator = generator_class(sql, _ast)
    # return _generator.execute()
