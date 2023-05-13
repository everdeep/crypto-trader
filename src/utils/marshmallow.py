from sqlalchemy import create_engine
from marshmallow import fields
from config import app_config

ENGINE = create_engine(app_config.SQLALCHEMY_DATABASE_URI, echo=False, pool_size=20, max_overflow=0)

class Nested(fields.Nested):
    """Nested field that inherits the session from its parent."""

    def _deserialize(self, *args, **kwargs):
        if hasattr(self.schema, "session"):
            self.schema.session = self.root.session  # overwrite session here
            self.schema.transient = self.root.transient
        return super()._deserialize(*args, **kwargs)