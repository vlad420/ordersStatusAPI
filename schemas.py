from marshmallow import Schema, fields


class OrderStatusSchema(Schema):
    order_id = fields.String(required=True)
    status = fields.String(dump_only=True)
    