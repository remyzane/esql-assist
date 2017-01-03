import json
from esql.generator import ast, Generator


class Insert(Generator):

    def __init__(self, sql, ast_obj: ast.Insert):
        self.sql = sql
        self.ast = ast_obj

    def build_insert_body(self):
        _id = None
        _parent = None
        body = {}
        for i in range(len(self.ast.fields)):
            if self.ast.fields[i] == '_id':
                _id = self.ast.values[i]
            elif self.ast.fields[i] == '_parent':
                _parent = self.ast.values[i]
            else:
                if self.ast.fields[i].is_object:
                    try:
                        values = json.loads(self.ast.values[i])
                        body[self.ast.fields[i].name] = values
                    except Exception:
                        pass
                else:
                    body[self.ast.fields[i].name] = self.ast.values[i]
        return body, _id, _parent

    def execute(self):
        body, _id, _parent = self.build_insert_body()
        params = {
            'index': self.ast.table.index_name,
            'doc_type': self.ast.table.doc_type,
            'body': body
        }
        if _id:
            params['id'] = _id
        if _parent:
            params['parent'] = _parent

        return params
