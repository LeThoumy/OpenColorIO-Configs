#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Defines various package utilities objects.
"""

from __future__ import division

import itertools
import os
import re
from collections import OrderedDict

import PyOpenColorIO as ocio

__author__ = 'ACES Developers'
__copyright__ = 'Copyright (C) 2014 - 2015 - ACES Developers'
__license__ = ''
__maintainer__ = 'ACES Developers'
__email__ = 'aces@oscars.org'
__status__ = 'Production'

__all__ = ['ColorSpace',
           'mat44_from_mat33',
           'filter_words',
           'files_walker',
           'replace',
           'sanitize',
           'compact',
           'colorspace_prefixed_name',
           'unpack_default']


class ColorSpace(object):
    """
    A container for data needed to define an *OCIO* *ColorSpace*.
    """

    def __init__(self,
                 name,
                 aliases=None,
                 description=None,
                 bit_depth=ocio.Constants.BIT_DEPTH_F32,
                 equality_group='',
                 family=None,
                 is_data=False,
                 to_reference_transforms=None,
                 from_reference_transforms=None,
                 allocation_type=ocio.Constants.ALLOCATION_UNIFORM,
                 allocation_vars=None,
                 aces_transform_id=None):
        """
        Object description.

        Parameters
        ----------
        parameter : type
            Parameter description.

        Returns
        -------
        type
             Return value description.
        """

        if aliases is None:
            aliases = []

        if to_reference_transforms is None:
            to_reference_transforms = []

        if from_reference_transforms is None:
            from_reference_transforms = []

        if allocation_vars is None:
            allocation_vars = [0, 1]

        self.name = name
        self.aliases = aliases
        self.bit_depth = bit_depth
        self.description = description
        self.equality_group = equality_group
        self.family = family
        self.is_data = is_data
        self.to_reference_transforms = to_reference_transforms
        self.from_reference_transforms = from_reference_transforms
        self.allocation_type = allocation_type
        self.allocation_vars = allocation_vars
        self.aces_transform_id = aces_transform_id


def mat44_from_mat33(mat33):
    """
    Creates a 4x4 matrix from given 3x3 matrix.

    Parameters
    ----------
    parameter : type
        Parameter description.

    Returns
    -------
    type
         Return value description.
    """

    return [mat33[0], mat33[1], mat33[2], 0,
            mat33[3], mat33[4], mat33[5], 0,
            mat33[6], mat33[7], mat33[8], 0,
            0, 0, 0, 1]


def filter_words(words, filters_in=None, filters_out=None, flags=0):
    """
    Object description.

    Parameters
    ----------
    parameter : type
        Parameter description.

    Returns
    -------
    type
         Return value description.
    """

    filtered_words = []
    for word in words:
        if filters_in:
            filter_matched = False
            for filter in filters_in:
                if re.search(filter, word, flags):
                    filter_matched = True
                    break
            if not filter_matched:
                continue

        if filters_out:
            filter_matched = False
            for filter in filters_out:
                if re.search(filter, word, flags):
                    filter_matched = True
                    break
            if filter_matched:
                continue
        filtered_words.append(word)
    return filtered_words


def files_walker(directory, filters_in=None, filters_out=None, flags=0):
    """
    Object description.

    Parameters
    ----------
    parameter : type
        Parameter description.

    Returns
    -------
    type
         Return value description.
    """

    for parent_directory, directories, files in os.walk(
            directory, topdown=False, followlinks=True):
        for file in files:
            path = os.path.join(parent_directory, file)
            if os.path.isfile(path):
                if not filter_words((path,), filters_in, filters_out, flags):
                    continue

                yield path


def replace(string, data):
    """
    Replaces the data occurrences in the string.

    Parameters
    ----------
    string : str or unicode
        String to manipulate.
    data : dict
        Replacement occurrences.

    Returns
    -------
    unicode
        Manipulated string.

    Examples
    --------
    >>> patterns = {'John' : 'Luke',
    ...             'Jane' : 'Anakin',
    ...             'Doe' : 'Skywalker',
    ...             'Z6PO' : 'R2D2'}
    >>> data = 'Users are: John Doe, Jane Doe, Z6PO.'
    >>> replace(data,patterns )
    u'Users are: Luke Skywalker, Anakin Skywalker, R2D2.'
    """

    for old, new in data.iteritems():
        string = string.replace(old, new)
    return string


def sanitize(path):
    """
    Object description.

    Parameters
    ----------
    parameter : type
        Parameter description.

    Returns
    -------
    type
         Return value description.
    """

    return replace(path, {' ': '_', ')': '_', '(': '_'})


def compact(string):
    """
    Removes blanks, underscores, dashes and parentheses.

    Parameters
    ----------
    string : str or unicode
        String to compact.

    Returns
    -------
    str or unicode
         A compact version of that string.
    """

    return replace(string.lower(),
                   OrderedDict(((' ', '_'),
                                ('(', '_'),
                                (')', '_'),
                                ('.', '_'),
                                ('-', '_'),
                                ('___', '_'),
                                ('__', '_'),
                                ('_', ''))))


def colorspace_prefixed_name(colorspace):
    """
    Returns given *OCIO* colorspace prefixed name with its family name.

    Parameters
    ----------
    colorspace : Colorspace
        Colorspace to prefix.

    Returns
    -------
    str or unicode
         Family prefixed *OCIO* colorspace name.
    """
    prefix = colorspace.family.replace('/', ' - ')

    return '%s - %s' % (prefix, colorspace.name)


def unpack_default(iterable, length=3, default=None):
    """
    Unpacks given iterable maintaining given length and filling missing
    entries with given default.

    Parameters
    ----------
    iterable : object
        Iterable.
    length : int
        Iterable length.
    default : object
        Filling default object.

    Returns
    -------
    iterable
    """

    return itertools.islice(
        itertools.chain(iter(iterable), itertools.repeat(default)), length)
