import json
from esql.generator import rst, Generator


class Insert(Generator):

    def __init__(self, sql, _rst: rst.Insert):
        self.sql = sql
        self.rst = _rst

    def build_insert_body(self):
        _id = None
        _parent = None
        body = {}
        for i in range(len(self.rst.fields)):
            if self.rst.fields[i] == '_id':
                _id = self.rst.values[i]
            elif self.rst.fields[i] == '_parent':
                _parent = self.rst.values[i]
            else:
                if self.rst.fields[i].is_object:
                    try:
                        values = json.loads(self.rst.values[i])
                        body[self.rst.fields[i].name] = values
                    except Exception:
                        pass
                else:
                    body[self.rst.fields[i].name] = self.rst.values[i]
        return body, _id, _parent

    def execute(self):
        body, _id, _parent = self.build_insert_body()
        params = {
            'index': self.rst.table.index_name,
            'doc_type': self.rst.table.doc_type,
            'body': body
        }
        if _id:
            params['id'] = _id
        if _parent:
            params['parent'] = _parent

        return params
