from marshmallow import post_load
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from enums import StrategyType
from model import StrategyConfigModel

# IMPORTANT: This is needed to make the marshmallow_sqlalchemy work
# import after the models are defined and before the marshmallow schemas
from sqlalchemy.orm import configure_mappers

configure_mappers()


class StrategyConfigSchema(SQLAlchemyAutoSchema):
    strategy = EnumField(StrategyType, by_value=True)

    class Meta:
        model = StrategyConfigModel
        include_fk = True
        load_instance = True
