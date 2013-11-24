# -*- coding: utf-8 -*-

import nose
import sys

from nose.tools.trivial import eq_

from rabbitracer import _parse_args


class Test_Main(object):

    def test_parse_default(self):
        sys.argv = ['rabbitracer']
        args = _parse_args()
        eq_(args.hostname, 'localhost')
        eq_(args.password, 'guest')
        eq_(args.virtualhost, '/')


if __name__ == "__main__":
    nose.main(argv=['nosetests', '-s', '-v'], defaultTest=__file__)
