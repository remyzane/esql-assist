import json
from esql.processor import ast, rst, TK, Processor


class TableCreate(Processor):

    mapping = ast.TK.CREATE_TABLE

    def __init__(self, sql, _ast):
        Processor.__init__(self, sql)
        self.rst = rst.TableCreate(_ast)

    def explain(self):
        self.rst.table
        self.rst.fields[0]
        # body, _id, _parent = self.build_insert_body()
        # params = {
        #     'index': self.rst.table.index_name,
        #     'doc_type': self.rst.table.doc_type,
        #     'body': body
        # }
        # if _id:
        #     params['id'] = _id
        # if _parent:
        #     params['parent'] = _parent

        # return params
        return {
    "body": {
        "info": {
            "properties": {
                "a": {
                    "index": "not_analyzed",
                    "type": "string"
                },
                "b": {
                    "type": "integer"
                }
            }
        }
    },
    "index": "table_name",
    "doc_type": "info"
}
