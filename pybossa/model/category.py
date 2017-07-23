# -*- coding: utf8 -*-
# This file is part of PYBOSSA.
#
# Copyright (C) 2015 Scifabric LTD.
#
# PYBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PYBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PYBOSSA.  If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy import Integer, Text
from sqlalchemy.schema import Column, ForeignKey

from pybossa.core import db
from pybossa.model import DomainObject, make_timestamp


class Category(db.Model, DomainObject):
    '''A Table with Categories for Projects.'''

    __tablename__ = 'category'

    #: Category ID
    id = Column(Integer, primary_key=True)
    #: Name of the Category
    name = Column(Text, nullable=False, unique=True)
    #: Slug for the Category URL
    short_name = Column(Text, nullable=False, unique=True)
    #: Description of the Category
    description = Column(Text, nullable=False)
    #: UTC timestamp when the Category was created
    created = Column(Text, default=make_timestamp)

    @classmethod
    def public_attributes(self):
        """Return a list of public attributes."""
        return ['description', 'short_name', 'created', 'id', 'name']

    def public_info_keys(self):
        """Return a list of public info keys."""
        return []
