from marshmallow import Schema, fields, post_load
from marshmallow.validate import Length, Range

from somemart.models import Item, Review


class ItemSchema(Schema):
    """ Item validation schema. """

    id = fields.Int(dump_only=True)
    title = fields.Str(validate=Length(1, 64))
    description = fields.Str(validate=Length(1, 1024))
    price = fields.Int(validate=Range(1, 1000000), strict=True)

    @post_load
    def make(self, data):
        return Item(**data)  # returns Item object


class ReviewSchema(Schema):
    """ Review validation schema. """

    id = fields.Int(dump_only=True)
    grade = fields.Int(validate=Range(1, 10), strict=True)
    text = fields.Str(validate=Length(1, 1024))

    @post_load
    def make(self, data):
        return Review(**data)  # returns Review object
