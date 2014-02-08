# -*- coding: utf-8 -*-

import nose
import sys

from nose.tools.trivial import eq_

from rabbitracer import _parse_args, _build_uri


class Test_Main(object):

    def test_parse_default(self):
        sys.argv = ['rabbitracer']
        args = _parse_args()
        eq_(args.hostname, 'localhost')
        eq_(args.username, 'guest')
        eq_(args.password, 'guest')
        eq_(args.virtualhost, '/')
        eq_(args.pretty_print, False)

    def test_build_uri(self):
        sys.argv = ['rabbitracer']
        args = _parse_args()
        uri = _build_uri(args)
        eq_(uri, 'amqp://guest:guest@/')

if __name__ == "__main__":
    nose.main(argv=['nosetests', '-s', '-v'], defaultTest=__file__)
