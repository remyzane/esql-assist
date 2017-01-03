from ply.lex import lex
from ply.yacc import yacc

# from esql.parser import lexis, grammar
from esql.parser.ql_parse import lexis, grammar, transform, TK

lexer = None
parser = None
debug = False

ast_signs = None
ast_classes = None


def init(config):
    global lexer, parser, debug, ast_signs, ast_classes
    debug = config.get('debug', False)
    optimize = config.get('optimize', True)
    lexer = lex(module=lexis, optimize=optimize, debug=debug)
    parser = yacc(debug=debug, module=grammar)

    from esql.parser import ast
    ast_signs = []
    ast_classes = []
    for node_class in ast.Node.__subclasses__():
        ast_signs.append(node_class.__name__.upper())
        ast_classes.append(node_class)


def get_ast_sign(obj):
    """ Get sign by node object.
    """
    return ast_signs[ast_classes.index(obj.__class__)]


def get_ast_class(sign1, sign2=''):
    """ Get node subclass by sign.
    """
    return ast_classes[ast_signs.index(sign1 + sign2)]


def parse(sql):
    return transform(parser.parse(input=sql, lexer=lexer.clone(), debug=debug))
