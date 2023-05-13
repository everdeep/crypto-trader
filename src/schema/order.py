from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from enums import ExchangeType, OrderStatus, OrderType, OrderSide
from model import OrderModel

# IMPORTANT: This is needed to make the marshmallow_sqlalchemy work
# import after the models are defined and before the marshmallow schemas
from sqlalchemy.orm import configure_mappers

configure_mappers()


class OrderSchema(SQLAlchemyAutoSchema):
    exchange = EnumField(ExchangeType, by_value=True)
    side = EnumField(OrderSide, by_value=True)
    status = EnumField(OrderStatus, by_value=True)
    type = EnumField(OrderType, by_value=True)

    class Meta:
        model = OrderModel
        include_fk = True
        load_instance = True
