# -*- encoding: utf-8 -*-
"""
test_levenshtein.py

Copyright 2012 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import unittest

from w3af.core.controllers.misc.fuzzy_string_cmp import relative_distance_boolean, relative_distance


class TestLevenshtein(unittest.TestCase):

    def test_all(self):
        acceptance_tests = [
            ('a', 'a', 1.0),
            ('a', 'a', 0.1),
            ('a', 'a', 0.0),
            ('a', 'b', 1.0),
            ('a', 'b', 0.1),
            ('a', 'b', 0.0),
            ('a', 'ab', 1.0),
            ('a', 'ab', 0.1),
            ('a', 'b', 0.0000000000000000001),
            ('a', 'b' * 100, 1.0),
            ('a', 'ab', 0.66666666666),
            ('a', 'aab', 0.5),
            ('a', 'aaab', 0.4),
            (
                'a',
                'aaaab',
                0.33333333333333333333333333333333333333333333333333333333,
            ),
            ('a' * 25, 'a', 1.0),
            ('aaa', 'aa', 1.0),
            ('a', 'a', 1.0),
            ('a' * 25, 'a', 0.076923076923076927),
            ('aaa', 'aa', 0.8),
            ('a', 'a', 0.0),
        ]

        msg = 'relative_distance_boolean and relative_distance returned'\
                  ' different results for the same parameters:\n'\
                  '    - %s\n'\
                  '    - %s\n'\
                  '    - Threshold: %s\n'
        for e, d, f in acceptance_tests:
            res1 = relative_distance_boolean(e, d, f)
            res2 = relative_distance(e, d) >= f

            self.assertEqual(res1, res2, msg % (e, d, f))

    def test_relative_distance(self):
        acceptance_tests = [
            ('a', 'a', 1.0),
            ('ab ac ad', 'ab ae ad', 0.6),
            ('ab ac ae', 'ab af ad', 0.3),
            ('ab ac ad', 'aa ae af', 0.0),
            ('a', 'b', 0.0),
            ('aaaa', 'aaab', 0.75),
            ('a' * 25, 'a', 0.04),
        ]

        for e, d, f in acceptance_tests:
            res = relative_distance(e, d)
            msg = "return value:%f, given value:%f" % (res, f)
            self.assertTrue(res >= f, msg)