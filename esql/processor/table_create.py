
from esql.processor import ast, rst, Processor


class TableCreate(Processor):

    mapping = ast.TK.TOK_CREATE_TABLE

    def __init__(self, sql, _ast, explain_only=False):
        Processor.__init__(self, sql, _ast, explain_only)
        self.rst = rst.TableCreate(self.ast)

    def explain(self):
        dsl = {'index': self.rst.table.index_name,
               'doc_type': self.rst.table.doc_type,
               'body': {self.rst.table.doc_type: {}}}
        dsl['body'][self.rst.table.doc_type]['properties'] = self.rst.fields.dsl()
        return dsl
