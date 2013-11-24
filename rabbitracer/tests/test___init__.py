# -*- coding: utf-8 -*-

import nose


class Test(object):

    def test(self):
        pass


if __name__ == "__main__":
    nose.main(argv=['nosetests', '-s', '-v'], defaultTest=__file__)
