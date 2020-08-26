# -*- coding: utf-8 -*- 

import pyutil.db.magic as magic
import pyutil.db.lang as Lang
import pyutil.db.util as db_util
import pyutil.common.util as common_util
import pyutil.common.type_util as type_util
import pyutil.common.sys_utf8 as sys_utf8
import time, datetime
import sys

'''
Mysql senior operations
'''
class mellow:
    def __init__(self, db_config):
        print "db_config:", db_config
        self.db_config = db_config
        self.magic = magic.magic(db_config)
        self.columns = {}

    
    def __excute_and_parse_datetime(self, lang, out):
        if out == list:
            return db_util.ParseUtime(self.magic.query(lang))
        elif out == dict:
            return db_util.ParseUtime(self.magic.query_dict(lang))
        else:
            print "Warning: Not Support return type"
            return None

    
    def Find(self, tabName, fieldList=[], indexMap={}, limit=(), orderby=((),"asc"), out=list):
        '''
        实现查找数据功能
        tabName:表名
        fieldList:查询字段名称
                    不传递参数，则查询所有列
                    传递参数str,只查询一个字段，如fieldList='name',fieldList="phone_number as 'phone_no'"
                    传递参数list,查询一个或多个字段["user_id", "name AS uame"]
        indexMap:查询条件
                    传递参数dict: fieldList = {'id': 1，"age": ("in",["18","20"])，"id_c": ("like",["13","55"])}
                    传递参数str: fieldList = "where id = 1"
                    传递参数list,tupple: fieldList = [[[id],[2]]]
        limit:查询数据条数限制,如limit=(0,2)
        orderby:排序方式,可接收数据类型:list,tupple
        out:输出数据格式，支持list(默认),dict
        '''
        if isinstance(indexMap, dict):
            indexMap = common_util.FilterMap(indexMap, self.Columns(tabName))
        fieldsLang = Lang.Fields(fieldList)
        whereLang = Lang.Where(indexMap)
        limitLang = " LIMIT %s, %s" % (str(limit[0]), str(limit[1])) if limit and len(limit) == 2 else ""

        orderbyLang = Lang.OrderBy(orderby)
        lang = "SELECT %s FROM %s %s %s %s" % (fieldsLang, tabName, whereLang, orderbyLang, limitLang)
        return self.__excute_and_parse_datetime(lang, out)


    def Search(self, tabName, fieldList=[], indexMap={}, orderby=((),"asc"), limit=(), out=list):
        '''
        同Find()方法
        '''
        return self.Find(tabName, fieldList, indexMap=indexMap, orderby=orderby, limit=limit, out=out)


    def Max(self, tabName, field, indexMap={}):
        '''
        根据条件查找记录最大值
        tabName:表名
        field:查询字段名称
        indexMap:查询条件,可接收数据类型:dict(默认),str,list,tupple    
        '''

        indexMap = common_util.FilterMap(indexMap, self.Columns(tabName))
        whereLang = Lang.Where(indexMap)
        lang = "SELECT MAX(`%s`) FROM `%s` %s " % (field, tabName, whereLang)
        rows = self.magic.query(lang)
        if len(rows)>0:
            return rows[0][0]
        else:
            return None


    def Min(self, tabName, field):
        '''
        根据条件查找记录最小值
        tabName:表名
        field:查询字段名称
        '''    
        rows = self.Find(tabName, ["MIN(%s)" % field])
        if rows:
            return rows[0][0]
        else:
            return None


    def Count(self, tabName, indexMap={}):
        '''
        查询符合条件的记录数
        tabName:表名
        indexMap:查询条件,可接收数据类型:dict(默认),str,list,tupple
        '''
        if not self.ExistTable(tabName):
            return 0

        if isinstance(indexMap, dict):
            indexMap = common_util.FilterMap(indexMap, self.Columns(tabName))

        lang = "SELECT count(1) FROM `%s` %s " % (tabName, Lang.Where(indexMap))
        rows = self.magic.query(lang)
        return rows[0][0] if rows else 0


    def Exist(self, tabName, indexMap):
        '''
        判断指定条件的数据是否存在
        tabName:表名
        indexMap:限制条件,可接收数据类型:dict,str,list,tupple
        '''
        if not indexMap:
            return False

        if isinstance(indexMap, dict):
            indexMap = common_util.FilterMap(indexMap, self.Columns(tabName))

        lang = "SELECT count(1) FROM `%s` %s " % (tabName, Lang.Where(indexMap))

        rows = self.magic.query(lang)
        return True if len(rows)>0 and int(rows[0][0]) > 0 else False


    def ExistTable(self, tabName):
        '''
        判断某个表是否存在
        tabName:表名
        '''
        if not tabName:
            return False
        lang = "SELECT table_name FROM information_schema.TABLES WHERE table_name = '%s' " % (tabName)
        rows = self.magic.query(lang)
        return True if rows else False


    def RunSql(self, language, autocommit=False, out=list):
        '''
        执行输入sql语句
        language:sql语句
        autocommit:是否自动提交:默认(False)
        out:输出格式,支持list(默认),dict
        '''
        action = language.strip().split(" ")[0].upper()
        if action == "SELECT":
            return self.__excute_and_parse_datetime(language, out)
        elif action in ["CREATE", "UPDATE", "INSERT", "ALTER", "DELETE", "DROP"]:
            return self.magic.execute(language, autocommit=autocommit)
        else:
            print "Error, RunSql not support language:", language
            return None


    def Update(self, tabName, dataMap, indexMap, num=1):
        '''
        根据条件更新数据
        tabName:表名
        dataMap:更新的字段和更新数据
        indexMap:更新条件,可接收数据类型:dict,str,list,tupple
        '''
        if not indexMap or not dataMap:
            return -1, -1

        if num==1 :
            row_count = self.Count(tabName, indexMap)
            if  row_count > 1:
                print "Error, Will affect multi rows,  pyutil.db.mellow Update tabName=", tabName, ",indexMap:", indexMap
                return -1, -1
            elif row_count < 1:
                print "Error, Record not exist, affect 0 rows,  pyutil.db.mellow Update tabName=", tabName, ",indexMap:", indexMap
                return -1, -1

        columns = self.Columns(tabName)
        if isinstance(dataMap, dict):
            dataMap = common_util.FilterMap(dataMap, columns)
        if isinstance(indexMap, dict):
            indexMap = common_util.FilterMap(indexMap, columns)

        lang = "UPDATE `%s` SET %s %s"  % (tabName, Lang.Assign(dataMap), Lang.Where(indexMap))
        return self.magic.execute(lang, autocommit=True)


    def Insert(self, tabName, dataMap):
        '''
        实现插入数据功能
        输入参数
        tabName:表名
        dataMap:更新字段、数据,可接收数据类型:dict
        '''
        if not dataMap:
            print "Error, When call pyutil.db.mellow Insert tabName=", tabName, ",dataMap:", dataMap
            return -1, -1

        if isinstance(dataMap, dict):
            dataMap = db_util.ParseUtime(common_util.FilterMap(dataMap, self.Columns(tabName)))

        names, values = [], []
        for k, v in dataMap.items():
            if v is None or v =="":
                continue
            names.append("`%s`" % (str(k)))
            if isinstance(v,int) or isinstance(v,long):
                values.append(str(v))
            elif isinstance(v, str) or isinstance(v, unicode):
                values.append("'"+db_util.escape_string(v)+"'")
            elif isinstance(v,float):
                values.append(str(v))
            else:
                print "Error unknowed type of val:", v, ",type=", type(v), ",key=", k
                return -1, -1
        lang = "INSERT INTO `%s`(%s) VALUES(%s)" % (tabName, " , ".join(names),  ",".join(values))
        return self.magic.execute(lang, autocommit=True)


    def InsertMany(self, tabName, fields, values):
        '''
        实现插入数据功能
        输入参数
        tabName:表名
        fields:表中的字段列表
        values:表中的属性值列表
        '''
        if not fields:
            print "Error, When call pyutil.db.mellow Insert tabName=", tabName, ",fields is empty"
            return -1, -1

        if not isinstance(values, list):
            print "Error, When call pyutil.db.mellow Insert valus is not a list"
            return -1, -1
        fields = '('+ ','.join(['`'+str(i)+'`' for i in fields])+')'

        lines = []
        for item in values:
            item = db_util.ParseUtime(item)
            for i, v in enumerate(item):
                if isinstance(v,int) or isinstance(v,long):
                    item[i] = str(v)
                elif isinstance(v, str) or isinstance(v, unicode):
                    item[i] = "'"+db_util.escape_string(v)+"'"
                else:
                    item[i] = str(v)
            line = "(" + ",".join(item) + ")"
            lines.append(line)

        lang = "INSERT INTO `%s`%s VALUES%s" % (tabName, fields,  ",".join(lines))
        return self.magic.execute(lang, autocommit=True)


    def UpOrInsert(self, tabName, dataMap, indexMap):
        '''
        插入数据,如果存在,则进行更新
        tabName:表名
        dataMap:要操作字段、数据,数据类型:dict
        indexMap:限制条件,可接收数据类型:dict(默认),str,list,tupple
        '''
        if not indexMap or not dataMap or not isinstance(dataMap, dict):
            return -1, -1
        dataMap = db_util.ParseUtime(common_util.FilterMap(dataMap, self.Columns(tabName)))
        if self.Exist(tabName, indexMap):
            lang = "UPDATE `%s` SET %s %s" % (tabName, Lang.Assign(dataMap), Lang.Where(indexMap))
            return  self.magic.execute(lang, autocommit=True)
        else:
            return self.Insert(tabName, dataMap)

    def InsertOrNot(self, tabName, dataMap, indexMap):
        '''
        插入数据,如果数据存在,则不进行操作
        tabName:表名
        dataMap:要操作字段、数据,数据类型:dict
        indexMap:限制条件,可接收数据类型:dict(默认),str,list,tupple    
        '''
        
        if not indexMap or not dataMap or not isinstance(dataMap, dict):
            return -1, -1
        dataMap = db_util.ParseUtime(common_util.FilterMap(dataMap, self.Columns(tabName)))
        if self.Exist(tabName, indexMap):
            return 0, 1
        else :
            return self.Insert(tabName, dataMap) 
        

    def Delete(self, tabName, indexMap={}):
        '''
        删除指定数据
        tabName:表名
        indexMap:限制条件,可接收数据类型:dict(默认),str,list,tupple    
        '''
        if not indexMap:
            print "Error!!! Dangrous, Must not delete empty indexMap, tabName:", tabName
            return

        lang = "DELETE FROM `%s` %s" % (tabName, Lang.Where(indexMap))
        return self.magic.execute(lang, autocommit=True)

    def FindVal(self, tabName, field, indexMap, defaultVal):
        '''
        查询某个字段的值
        tabName:表名
        field:查询字段名称,可接收数据类型:list,str
        indexMap:查询条件,可接收数据类型:dict(默认),str,list,tupple
        defaultVal:默认值
        '''
        rows = self.Find(tabName, field, indexMap)
        return rows[0][0] if rows else defaultVal

    @db_util.func_cache
    def Tables(self):
        rows = self.magic.query("SHOW TABLES")
        return [ row[0] for row in rows ]


    def TableExist(self, table_name):
        rows = self.magic.query("SELECT table_name FROM information_schema.TABLES WHERE table_name ='%s'" % (table_name))
        return not rows


    @db_util.func_cache
    def PrimaryKeys(self, tabName):
        rows = self.magic.query("DESC `%s`" % (tabName))
        primarys = []
        for row in rows:
            if row[3] == "PRI":
                primarys.append(row[0].encode('utf-8'))
        return primarys

    @db_util.func_cache
    def Columns(self, tabName):
        rows = self.magic.query("DESC `%s`" % (tabName))
        columns = []
        for row in rows:
            columns.append(row[0].encode('utf-8'))
        return columns


    @db_util.func_cache
    def ColumnsType(self, tabName):
        rows = self.magic.query("DESC `%s`" % (tabName))
        columns = {}
        for row in rows:
            field_name, field_type = row[0], row[1]
            if field_type.find("(") >0:
                field_type = field_type[:field_type.find("(")]
            if field_type in ["int", "bigint", "tinyint"] >=0 :
                columns[field_name.encode('utf-8')] = int
            elif field_type in ["char", "varchar", "text"]:
                columns[field_name.encode('utf-8')] = str
            elif field_type in ["timestamp", "datetime"]:
                columns[field_name.encode('utf-8')] = datetime.datetime
            elif field_type in ["date"]:
                columns[field_name.encode('utf-8')] = datetime.date
            elif field_type in ["bool"] :
                columns[field_name.encode('utf-8')] = bool
            elif field_type in ["float", "double"] :
                columns[field_name.encode('utf-8')] = float
            else:
                print "Unkonwn field type for:", field_type
                columns[field_name.encode('utf-8')] = None
        return columns


    def StartTransaction(self):
        self.magic.start_transaction()


    def Rollback(self):
        self.magic.rollback()


    def Commit(self):
        self.magic.commit()
