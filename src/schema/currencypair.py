from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from model import CurrencyPairModel

# IMPORTANT: This is needed to make the marshmallow_sqlalchemy work
# import after the models are defined and before the marshmallow schemas
from sqlalchemy.orm import configure_mappers

configure_mappers()


class CurrencyPairSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CurrencyPairModel
        include_fk = True
