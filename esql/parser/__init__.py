from ply.lex import lex
from ply.yacc import yacc

from esql.parser.ast import lexis, grammar, transform, TK

lexer = None
parser = None
debug = False

rst_signs = None
rst_classes = None


def init(config):
    global lexer, parser, debug, rst_signs, rst_classes
    debug = config.get('debug', False)
    optimize = config.get('optimize', True)
    lexer = lex(module=lexis, optimize=optimize, debug=debug)
    parser = yacc(debug=debug, module=grammar)

    from esql.parser import rst
    rst_signs = []
    rst_classes = []
    for node_class in rst.Node.__subclasses__():
        rst_signs.append(node_class.__name__.upper())
        rst_classes.append(node_class)


def get_rst_sign(obj):
    """ Get sign by node object.
    """
    return rst_signs[rst_classes.index(obj.__class__)]


def get_rst_class(sign1, sign2=''):
    """ Get node subclass by sign.
    """
    return rst_classes[rst_signs.index(sign1 + sign2)]


def parse(sql):
    _ast = parser.parse(input=sql, lexer=lexer.clone(), debug=debug)
    return transform(_ast)  # rst
