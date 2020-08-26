# -*- coding: utf-8 -*- 

import pyutil.common.type_util as type_util 
import pyutil.db.util as db_util 


def test():
    print ":::", OrderBy([("a", "asc"), ("b", "desc")])
    print "===", OrderBy((("a", "b", "c"), "desc"))
    print "|||", OrderBy(("abc", "desc"))
    print Where([{"ab":3, "c":("IN", (1,2))}, {"d":999}])


if __name__ == '__main__':
    test()
