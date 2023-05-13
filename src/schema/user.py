from marshmallow.fields import Nested, List
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from model import UserModel

# IMPORTANT: This is needed to make the marshmallow_sqlalchemy work
# import after the models are defined and before the marshmallow schemas
from sqlalchemy.orm import configure_mappers

configure_mappers()


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "dob",
            "phone",
            "address",
            "portfolio",
            "settings",
            "roles",
            "is_verified",
            # "orders",
            # "currency_pair_configs",
        )
        model = UserModel

    settings = List(Nested("UserSettingsSchema"))
    address = Nested("AddressSchema")
    portfolio = Nested("PortfolioSchema")
