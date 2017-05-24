# -*- coding: utf-8 -*-
#
# This file is part of the Anitya project.
# Copyright (C) 2014-2016  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""
Exceptions used by Anitya.

Authors:
    Pierre-Yves Chibon <pingou@pingoured.fr>
"""


class AnityaException(Exception):
    ''' Generic class covering all the exceptions generated by anitya. '''
    pass


class AnityaPluginException(AnityaException):
    ''' Generic exception class that can be used by the plugin to indicate
    an error.
    '''
    pass


class ProjectExists(AnityaException):
    """
    Raised when a project already exists in the database.

    This is only raised when a project is part of an ecosystem, since projects
    outside of an ecosystem have no uniqueness constraints.
    """
    def __init__(self, requested_project):
        self.requested_project = requested_project

    def to_dict(self):
        return {
            u'requested_project': self.requested_project.__json__(),
        }

    def __str__(self):
        return 'Unable to create project since it already exists.'


class AnityaInvalidMappingException(AnityaException):
    ''' Specific exception class for invalid mapping. '''

    def __init__(self, pkgname, distro, found_pkgname,
                 found_distro, project_id, project_name, link=None):
        self.pkgname = pkgname
        self.distro = distro
        self.found_pkgname = found_pkgname
        self.found_distro = found_distro
        self.project_id = project_id
        self.project_name = project_name
        self.link = link

    @property
    def message(self):
        return 'Could not edit the mapping of {pkgname} on ' \
            '{distro}, there is already a package {found_pkgname} on ' \
            '{found_distro} as part of the project <a href="{link}">' \
            '{project_name}</a>.'.format(
                pkgname=self.pkgname,
                distro=self.distro,
                found_pkgname=self.found_pkgname,
                found_distro=self.found_distro,
                project_id=self.project_id,
                project_name=self.project_name,
                link=self.link,
            )


class InvalidVersion(AnityaException):
    """
    Raised when the version string is not valid for the given version scheme.

    Args:
        version (str): The version string that failed to parse.
        exception (Exception): The underlying exception that triggered this one.
    """

    def __init__(self, version, exception=None):
        self.version = version
        self.exception = exception

    def __str__(self):
        if self.exception:
            return 'Invalid version "{v}": {e}'.format(v=self.version, e=str(self.exception))
        else:
            return 'Invalid version "{v}"'.format(v=self.version)
