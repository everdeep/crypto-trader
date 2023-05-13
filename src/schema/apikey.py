from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from enums import ExchangeType
from model import ApiKeyModel

# IMPORTANT: This is needed to make the marshmallow_sqlalchemy work
# import after the models are defined and before the marshmallow schemas
from sqlalchemy.orm import configure_mappers

configure_mappers()


class ApiKeySchema(SQLAlchemyAutoSchema):
    exchange = EnumField(ExchangeType, by_value=True)

    class Meta:
        fields = ("api_key", "api_secret")
        model = ApiKeyModel
        include_fk = True
