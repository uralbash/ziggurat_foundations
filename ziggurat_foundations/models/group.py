import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from .base import BaseModel
from .services.group import GroupService
from ..utils import get_db_session


class GroupMixin(BaseModel):
    """ base mixin for group object"""

    _ziggurat_service = GroupService

    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    @declared_attr
    def __tablename__(self):
        return 'groups'

    # lists app wide permissions we might want to assign to groups
    __possible_permissions__ = ()

    @declared_attr
    def id(self):
        return sa.Column(sa.Integer(), primary_key=True, )

    @declared_attr
    def group_name(self):
        return sa.Column(sa.Unicode(128), nullable=False)

    @declared_attr
    def description(self):
        return sa.Column(sa.Text())

    @declared_attr
    def member_count(self):
        return sa.Column(sa.Integer, nullable=False, default=0)

    @declared_attr
    def users(self):
        """ relationship for users belonging to this group"""
        return sa.orm.relationship('User',
                                   secondary='users_groups',
                                   order_by='User.user_name',
                                   passive_deletes=True,
                                   passive_updates=True,
                                   backref='groups')

    # dynamic property - useful
    @declared_attr
    def users_dynamic(self):
        """ dynamic relationship for users belonging to this group
            one can use filter """
        return sa.orm.relationship('User',
                                   secondary='users_groups',
                                   order_by='User.user_name',
                                   lazy="dynamic")

    @declared_attr
    def permissions(self):
        """ non-resource permissions assigned to this group"""
        return sa.orm.relationship('GroupPermission',
                                   backref='groups',
                                   cascade="all, delete-orphan",
                                   passive_deletes=True,
                                   passive_updates=True)

    @declared_attr
    def resource_permissions(self):
        """ permissions to specific resources this group has"""
        return sa.orm.relationship('GroupResourcePermission',
                                   backref='groups',
                                   cascade="all, delete-orphan",
                                   passive_deletes=True,
                                   passive_updates=True)

    @declared_attr
    def resources(cls):
        """ Returns all resources directly owned by group, can be used to assign
        ownership of new resources::

            user.resources.append(resource) """
        return sa.orm.relationship('Resource',
                                   cascade="all",
                                   passive_deletes=True,
                                   passive_updates=True,
                                   backref='owner_group')

    @declared_attr
    def resources_dynamic(cls):
        """ Returns all resources directly owned by group, can be used to assign
        ownership of new resources::

            user.resources.append(resource) """
        return sa.orm.relationship('Resource',
                                   cascade="all",
                                   passive_deletes=True,
                                   passive_updates=True,
                                   lazy='dynamic')

    @sa.orm.validates('permissions')
    def validate_permission(self, key, permission):
        """ validates if group can get assigned with permission"""
        assert permission.perm_name in self.__possible_permissions__
        return permission

    def __repr__(self):
        return '<Group: %s, %s>' % (self.group_name, self.id)


    @classmethod
    def all(cls, db_session=None):
        db_session = get_db_session(db_session)
        return GroupService.all(db_session=db_session)


    @classmethod
    def by_group_name(cls, group_name, db_session=None):
        """ fetch group by name"""
        db_session = get_db_session(db_session)
        return GroupService.by_group_name(group_name=group_name, db_session=db_session)


    def get_user_paginator(self, page=1, item_count=None, items_per_page=50,
                           user_ids=None, GET_params=None, db_session=None):
        db_session = get_db_session(db_session, self)
        return GroupService.get_user_paginator(
            self, page=page, item_count=item_count, items_per_page=items_per_page,
            user_ids=user_ids, GET_params=GET_params)


    def resources_with_possible_perms(self, perm_names=None, resource_ids=None,
                                      resource_types=None,
                                      db_session=None):
        db_session = get_db_session(db_session, self)
        return GroupService.resources_with_possible_perms(
            self, perm_names=perm_names, resource_ids=resource_ids,
            resource_types=resource_types, db_session=db_session)
