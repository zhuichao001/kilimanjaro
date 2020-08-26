# -*- coding: utf-8 -*- 

import pyutil.common.type_util as type_util 
import pyutil.db.util as db_util 

def Fields(fieldList):
    fields = ""
    if not fieldList:
        fields = " * "
    elif isinstance(fieldList, str):
        arr = fieldList.split()
        if len(arr)>=3 and arr[-2].upper() == 'AS':
            fields =  " ".join(arr[:-2]) + " AS `%s`" % ( arr[-1] )
        else:
            fields = fieldList
    elif isinstance(fieldList, list):
        fieldList = [f for f in fieldList if f]
        for i,f in enumerate([name for name in fieldList if name]):
            arr = fieldList[i].split()
            if len(arr)>=3 and arr[-2].upper() == 'AS':
                fieldList[i] = " ".join(arr[:-2]) + " AS `%s`" % ( arr[-1] )
            elif fieldList[i].find('(') > 0:
                fieldList[i] = fieldList[i].replace("(", "(`").replace(")", "`)")
            elif fieldList[i][0] in ['"', '\''] and fieldList[i][-1] in ['"', '\'']:
                continue 
            else:
                fieldList[i] = '`' + fieldList[i] + '`'
        fields =  ", ".join(fieldList)
    else:
        print "fieldList:::", fieldList
        raise Exception("Not Support filedList type, filedList="+str(type(fieldList)))
    return db_util.escape_string(fields)

def Where(kvMap):
    def whereStr(indexMap):
        conditions = []
        for key, val in indexMap.items():
            if type_util.is_int(val):
                conditions.append("`%s`=%d" % (key, val))
            elif type_util.is_array(val) and len(val)==2 :
                if str(val[0]).strip()=="<>" and len(val[1])==2:
                    conditions.append("`%s` >= '%s' AND `%s` <= '%s'" % (key, db_util.escape_string(str(val[1][0])), key, db_util.escape_string(str(val[1][1])) ))
                elif val[0].upper()=="LIKE":
                    if type_util.is_array(val[1]):
                        conditions.append( " AND ".join([" `%s` " % (key) + ' LIKE "%'+db_util.escape_string(sub_name)+'%"' for sub_name in val[1]] ) )
                    else:
                        conditions.append( " `%s` " % (key) + ' LIKE "%'+db_util.escape_string(str(val[1]))+'%"' )
                elif val[0].upper()=="IN":  #("IN", "123,234") or ("IN", [123,234])
                    if type_util.is_str(val[1]):
                        conditions.append("`%s` IN (%s)" % (key,  db_util.escape_string(val[1])))
                    if type_util.is_array(val[1]):
                        items = ["'" + db_util.escape_string(str(_val)) +"'" if type_util.is_str(_val) else str(_val) for _val in val[1]]
                        conditions.append("`%s` IN (%s)" % (key, ",".join(items)))
                elif val[0].upper()=="NOT IN":  #("NOT IN", "123,234") or ("NOT IN", [123,234])
                    if type_util.is_str(val[1]):
                        conditions.append("`%s` NOT IN (%s)" % (key,  db_util.escape_string(val[1])))
                    if type_util.is_array(val[1]):
                        items = ["'" + db_util.escape_string(str(_val)) +"'" if type_util.is_str(_val) else str(_val) for _val in val[1]]
                        conditions.append("`%s` NOT IN (%s)" % (key, ",".join(items)))
                else:
                    conditions.append("`%s` %s '%s'" % (key, val[0], db_util.escape_string(str(val[1]))))
            else:
                conditions.append( " `%s` = '%s'" % (key, db_util.escape_string(str(val)) ) )
        return " AND ".join(conditions)

    where = ""
    if not kvMap:
        where = " "
    elif type_util.is_str(kvMap):
        where = kvMap if kvMap.upper().strip().startswith("WHERE") else " WHERE " + kvMap
    elif type_util.is_dict(kvMap):
        where = " WHERE " + whereStr(kvMap)
    elif type_util.is_array(kvMap):
        where = " WHERE " + " OR ".join([ '('+whereStr(indexMap)+')' for indexMap in kvMap ])
    else:
        print "Error, Where condition is not support, type:", type(kvMap), kvMap
        where = " "
    return where

def OrderBy(order_by_params):
    lang = ""
    if not order_by_params:
        lang = " "
    elif not type_util.is_array(order_by_params):
        lang = " "
    elif len(order_by_params) ==2 and str(order_by_params[1]).upper() in ["ASC", "DESC"]:
        fieldList, seq = order_by_params
        if not fieldList:
            lang = " "
        elif type_util.is_str(fieldList):
            lang = "ORDER BY %s %s " % (",".join(["`"+f.strip()+"`" for f in fieldList.split(",")]), seq)
        elif type_util.is_array(fieldList):
            lang = "ORDER BY %s %s " % (",".join(["`"+str(f).strip()+"`" for f in fieldList]), seq)
        else:
            lang = " "
    else:
        lang = "ORDER BY " + ", ".join(["`"+item[0]+"` "+item[1] for item in order_by_params])
    return db_util.escape_string(lang)

def Assign(kvMap):
    arr = []
    for k in kvMap:
        v = kvMap[k]

        if isinstance(v, int):
            arr.append("`%s`=%d" % (k, v))
        elif isinstance(v, basestring) and v == "":
            arr.append("`%s`=DEFAULT(`%s`)" % (k, k))
        else:
            arr.append("`%s`='%s'" % (k, db_util.escape_string(v)))
    assigns = ", ".join(arr)
    return assigns
