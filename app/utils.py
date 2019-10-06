from flask import jsonify
from flask_marshmallow.sqla import ModelSchema


def is_sequence(data):
    return hasattr(type(data), '__iter__')

class ModelTransfer:
    def __init__(self, schema):
        self._schema = schema
        if issubclass(schema, ModelSchema):
            self._schema = schema()
        else:
            self._schema = None



    def to_response(self, data, status=200):
        if self._schema:
            is_many = is_sequence(data)
            output = self._schema.dump(data, many=is_many)
            return jsonify(output), status
        else:
            raise RuntimeError("Not a chema model")




