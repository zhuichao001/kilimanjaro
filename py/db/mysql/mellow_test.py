import pyutil.db.mellow as mellow
import pyconf.db.default as default

mysql = mellow(default.config)


def test1():
    print mysql.Find("info_user", ["user_id", "name AS uame"], limit=(2,2), out=dict)
    print "--------------------------------------------"
    time.sleep(1)

    print mysql.Find("info_user", ["user_id", "name AS uame"], limit=(2,2), orderby=(("user_id",), "desc"), out=dict)
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    time.sleep(1)

    print mysql.Find("info_user", ["user_id", "name AS uame"], {"id": (">", 99)}, limit=(2,2), orderby=(("user_id",), "asc"), out=dict)
    print "============================================"
    print sys_utf8.Utf8(mysql.Search("info_user", [], {"name": "王"}, limit=(0,2), orderby=(("user_id",), "asc"), out=dict))


def test2():
    print mysql.Tables()
    mysql.Columns("relation_things_company")

    print "------------------"
    result = mysql.ColumnsType("info_building")
    print ":::", result

    print "=================="
    result = mysql.PrimaryKeys("info_company")
    print ":::", result


def test3():
    print mysql.Find("info_user", [], {"joined_time": ("<>", ("2016-06-01 00:00:00", "2016-07-01 00:00:00"))}, out=dict)
    print "--------------------------------------------"


def test4():
    print "============================================"
    print sys_utf8.Utf8(mysql.Search("info_user", [], {"phone_num": ("like",["18","46"])}, limit=(0,30), orderby=(("user_id",), "asc"), out=dict))

def test5():
    import pyconf.db.default as default
    mysql = mellow(default.config)

    print mysql.InsertMany("info_user", ["user_id", "name"], [(1111112, "a"), (1111113, "b")])
    print "--------------------------------------------"


def test6():
    mysql.StartTransaction()
    mysql.InsertMany("info_user", ["user_id", "name"], [(2222222, "bbbbbbbb"), (3333333, "cccccccccc")])
    mysql.InsertMany("info_user", ["user_id", "name"], [(4444444, "dddddddd"), (5555555, "eeeeeeeeee")])
    mysql.Commit()
    print "--------------------------------------------"


def test7():
    mysql.Update("info_user_copy", {"name":"zhc"}, {"user_id":2})
    print "--------------------------------------------"


def test8():
    print mysql.ExistTable("info_user")
    print mysql.Tables()
    print mysql.Tables()
    print "--------------------------------------------"


if __name__ == '__main__':
    test1()


if __name__ == '__main__':
    import pyutil.db.db_config_example as db_config_example
    mellow = mellow.mellow(db_config_example.config)
    print mellow.Update("user", {"name": "1111"}, {"id":4})
    print mellow.Find("user", ["`id`","name as uame"], limit=(2,2), out=dict)
