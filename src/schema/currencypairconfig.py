from marshmallow_enum import EnumField
from marshmallow.fields import List
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


from utils.marshmallow import Nested
from enums import ExchangeType, Interval, StrategyType
from model import CurrencyPairConfigModel

# IMPORTANT: This is needed to make the marshmallow_sqlalchemy work
# import after the models are defined and before the marshmallow schemas
from sqlalchemy.orm import configure_mappers

configure_mappers()


class CurrencyPairConfigSchema(SQLAlchemyAutoSchema):
    exchange = EnumField(ExchangeType, by_value=True)
    interval = EnumField(Interval, by_value=True)
    strategy = EnumField(StrategyType, by_value=True)

    class Meta:
        model = CurrencyPairConfigModel
        include_fk = True
        load_instance = True

    signal = Nested("SignalSchema")
    orders = List(Nested("OrderSchema"))
    strategy_config = List(Nested("StrategyConfigSchema"))
