from marshmallow.fields import Nested, List
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from model import SymbolModel

# IMPORTANT: This is needed to make the marshmallow_sqlalchemy work
# import after the models are defined and before the marshmallow schemas
from sqlalchemy.orm import configure_mappers

configure_mappers()


class SymbolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SymbolModel

    currency_pairs = List(Nested("CurrencyPairSchema"))
