
from esql.processor import ast, rst, Processor


class TableCreate(Processor):

    mapping = ast.TK.CREATE_TABLE

    def __init__(self, sql, _ast):
        Processor.__init__(self, sql)
        self.rst = rst.TableCreate(_ast)

    def explain(self):
        dsl = {'index': self.rst.table.index_name,
               'doc_type': self.rst.table.doc_type,
               'body': {self.rst.table.doc_type: {'properties': {}}}}
        properties = dsl['body'][self.rst.table.doc_type]['properties']

        for field in self.rst.fields:
            properties[field.name] = {'type': field.type}

        return dsl
