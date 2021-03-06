import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from .base import BaseModel
from .services.external_identity import ExternalIdentityManager


class ExternalIdentityMixin(ExternalIdentityManager, BaseModel):
    @declared_attr
    def __tablename__(self):
        return 'external_identities'

    @declared_attr
    def external_id(self):
        return sa.Column(sa.Unicode(255), default=u'', primary_key=True)

    @declared_attr
    def external_user_name(self):
        return sa.Column(sa.Unicode(255), default=u'')

    @declared_attr
    def local_user_name(self):
        return sa.Column(sa.Unicode(50), sa.ForeignKey('users.user_name',
                                                       onupdate='CASCADE',
                                                       ondelete='CASCADE'),
                         primary_key=True)

    @declared_attr
    def provider_name(self):
        return sa.Column(sa.Unicode(50), default=u'', primary_key=True)

    @declared_attr
    def access_token(self):
        return sa.Column(sa.String(255), default=u'')

    @declared_attr
    def alt_token(self):
        return sa.Column(sa.String(255), default=u'')

    @declared_attr
    def token_secret(self):
        return sa.Column(sa.String(255), default=u'')
