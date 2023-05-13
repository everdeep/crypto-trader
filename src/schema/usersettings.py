from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from model import UserSettingsModel

# IMPORTANT: This is needed to make the marshmallow_sqlalchemy work
# import after the models are defined and before the marshmallow schemas
from sqlalchemy.orm import configure_mappers

configure_mappers()


class UserSettingsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserSettingsModel
        include_fk = True
