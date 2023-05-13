from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from model import BalanceModel

# IMPORTANT: This is needed to make the marshmallow_sqlalchemy work
# import after the models are defined and before the marshmallow schemas
from sqlalchemy.orm import configure_mappers

configure_mappers()


class BalanceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BalanceModel
        include_fk = True
        load_instance = True
