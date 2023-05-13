from marshmallow.fields import List
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from utils.marshmallow import Nested
from model import PortfolioModel

# IMPORTANT: This is needed to make the marshmallow_sqlalchemy work
# import after the models are defined and before the marshmallow schemas
from sqlalchemy.orm import configure_mappers

configure_mappers()


class PortfolioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PortfolioModel
        include_fk = True
        load_instance = True

    balances = List(Nested("BalanceSchema"))
