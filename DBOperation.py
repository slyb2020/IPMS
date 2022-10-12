import pymysql

from ID_DEFINE import *
import pymysql as MySQLdb
import time
import datetime
import json
import base64
from TransformImage import TransformBase64

def GetEnterpriseInfo(log, whichDB):
    try:
        # db = MySQLdb.connect(host="127.0.0.1", user="root", passwd='', db="智能生产管理系统_调试",charset='utf8')
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `企业名称` from `企业基本信息表` """
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp[0]

def GetAllPasswords(log, whichDB):
    try:
        # db = MySQLdb.connect(host="127.0.0.1", user="root", passwd='', db="智能生产管理系统_调试",charset='utf8')
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `密码`,`处`,`科`,`职别名`,`姓名`,`员工编号`,`工作状态` from `info_staff` """
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    PSW = []
    info = []
    for psw in temp:
        PSW.append(psw[0])
        info.append(psw[1:])
    db.close()
    return 0, PSW,info


def GetStaffInfoWithPassword(log, whichDB, psw):
    try:
        # db = MySQLdb.connect(host="127.0.0.1", user="root", passwd='', db="智能生产管理系统_调试",charset='utf8')
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("1无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("1无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `处`,`科`,`工位名`,`姓名`,`员工编号`,`工作状态` from `info_staff` WHERE `密码`='%s'"""%(psw)
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp

def GetStaffInfoWithID(log, whichDB, ID):
    try:
        # db = MySQLdb.connect(host="127.0.0.1", user="root", passwd='', db="智能生产管理系统_调试",charset='utf8')
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("2无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("2无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `处`,`科`,`工位名`,`姓名`,`员工编号`,`工作状态` from `info_staff` WHERE `员工编号`='%s'"""%(ID)
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp

def GetStaffInfo(log, whichDB):
    try:
        # db = MySQLdb.connect(host="127.0.0.1", user="root", passwd='', db="智能生产管理系统_调试",charset='utf8')
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("2无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("2无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `处`,`科`,`工位名`,`姓名`,`员工编号`,`工作状态` from `info_staff` """
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

def GetAllOrderList(log, whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("3无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("3无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `订单编号`,`订单名称`,`总价`,`产品数量`,`订单交货日期`,`下单时间`,`下单员ID`,`状态`,`子订单编号`,`子订单状态`,`设计审核状态`,`财务审核状态`,`采购审核状态`,`设计审核员ID`,`设计审核时间`,`设计审核意见` from `订单信息` """
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

def GetAllOrderAllInfo(log, whichDB,type):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("4无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("4无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if type == "草稿":
        sql = """SELECT `订单编号`,`订单名称`,`总价`,`产品数量`,`投标时间`,`下单时间`,`下单员ID`,`状态`,`设计审核状态`,`采购审核状态`,`财务审核状态`,`订单部审核状态`,`经理审核状态`,`报价参考日期`,`汇率参考日期` from `订单信息` where `状态`='%s' """%type
    elif type == "在产":
        sql = """SELECT `订单编号`,`订单名称`,`总价`,`产品数量`,`订单交货日期`,`下单时间`,`下单员ID`,`状态`,`报价参考日期`,`汇率参考日期` from `订单信息` where `状态`='%s' """%type
    elif type == "完工":
        sql = """SELECT `订单编号`,`订单名称`,`总价`,`产品数量`,`订单交货日期`,`下单时间`,`下单员ID`,`状态`,`报价参考日期`,`汇率参考日期` from `订单信息` where `状态`='%s' """%type
    elif type == "废弃":
        sql = """SELECT `订单编号`,`订单名称`,`总价`,`产品数量`,`投标时间`,`下单时间`,`下单员ID`,`状态`,`设计审核状态`,`采购审核状态`,`财务审核状态`,`订单部审核状态`,`经理审核状态`,`报价参考日期`,`汇率参考日期` from `订单信息` where `状态`='%s' """%type
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

def GetOrderByOrderID(log, whichDB, orderID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("5无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("5无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `订单编号`,`订单名称`,`总价`,`产品数量`,`订单交货日期`,`下单时间`,`下单员ID`,`状态`,`子订单编号`,`子订单状态`  from `订单信息` where `订单编号` = %s"""%int(orderID)
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp

def GetAllProductMeterialUnitPriceInDB(log, whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("5无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("5无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `产品名称`,`产品型号`,`产品表面材料`,`产品长度`,`产品宽度`,`产品厚度`,`SQM Per Piece`,`X面厚度`,`Y面厚度`,`X面材料id`,`X面材料系数`,`Y面材料id`,`Y面材料系数`,`胶水id`,`胶水系数`,`岩棉id`,`岩棉系数`  from `产品材料单价表`"""
    cursor.execute(sql)
    temp = cursor.fetchall()
    result=[]
    for item in temp:
        item = dict(zip(['产品名称','产品型号','产品表面材料','产品长度','产品宽度','产品厚度','SQM Per Piece','X面厚度','Y面厚度','X面材料id','X面材料系数','Y面材料id','Y面材料系数','胶水id','胶水系数','岩棉id','岩棉系数'], item))
        result.append(item)
    db.close()
    return 0, result

def GetProductMeterialUnitPriceInDB(log, whichDB, dic):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("5无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("5无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `产品厚度`,`SQM Per Piece`,`X面厚度`,`Y面厚度`,`X面材料id`,`X面材料系数`,`Y面材料id`,`Y面材料系数`,`胶水id`,`胶水系数`,`岩棉id`,`岩棉系数`  from `产品材料单价表`
    where `产品名称` = '%s' and `产品型号`='%s' and `产品表面材料`='%s' and `产品长度`='%s' and `产品宽度`='%s' 
      """%(dic['产品名称'],dic['产品型号'],dic['产品表面材料'],dic['产品长度'],dic['产品宽度'])
    cursor.execute(sql)
    temp = cursor.fetchone()
    temp = dict(zip(['产品厚度','SQM Per Piece','X面厚度','Y面厚度','X面材料id','X面材料系数','Y面材料id','Y面材料系数','胶水id','胶水系数','岩棉id','岩棉系数'], temp))
    db.close()
    return 0, temp

def GetAllMeterialUnitPriceByIdInDB(log, whichDB, Date):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("5无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("5无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `材料名`,`单位`,`价格`,`密度`  from `原材料单价表` where `市价更新日期` = '%s' """%(Date)
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    result=[]
    for item in temp:
        item = dict(zip(['材料名','单位','价格','密度'], item))
        result.append(item)
    db.close()
    return 0, result

def GetMeterialUnitPriceByIdInDB(log, whichDB, Date, id):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("5无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("5无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `材料名`,`单位`,`价格`,`密度`  from `原材料单价表` where `市价更新日期` = '%s' """%(Date)
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    if len(temp)>id:
        temp = temp[id]
    temp = dict(zip(['材料名','单位','价格','密度'], temp))
    db.close()
    return 0, temp

def GetProductLaborUnitPriceInDB(log, whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("5无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("5无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `产品名称`,`产品表面材料`,`每平方所需工时`  from `产品工时单价表` """
    cursor.execute(sql)
    temp = cursor.fetchall()
    result=[]
    for item in temp:
        item = dict(zip(['产品名称','产品表面材料','每平方所需工时'], item))
        result.append(item)
    db.close()
    return 0, result

def GetOrderNameByOrderID(log, whichDB, orderID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `订单名称` from `订单信息` where `订单编号` = %s"""%int(orderID)
    cursor.execute(sql)
    temp = cursor.fetchone()[0]  # 获得压条信息
    db.close()
    return 0, temp

def UpdateOrderInfo(log, whichDB,data):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE 订单信息 SET `订单名称`='%s',`总价`='%s',`产品数量`='%s',`状态`='%s' WHERE `订单编号` = '%s'" \
          % (str(data[1]),str(data[2]),str(data[3]),str(data[4]),str(data[0]))
    # sql = "INSERT INTO 图纸信息(`图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`," \
    #       "`热压100`,`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`图纸大类`,`创建时间`,`备注`)" \
    #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
    #       % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],datetime.date.today(),data[17])
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
    db.close()

def UpdateDraftOrderInfoByID(log, whichDB,dic,id):
    id = int(id)
    result=1
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sectionNameDic={
                       "订单名称":"1.订单名称 *",
                       "客户名称":"2.客户单位名称",
                       "客户公司信息":"3.客户公司信息",
                       "联系人":"4.联系人姓名",
                       "联系人电话":"5.联系人电话",
                       "联系人邮箱":"6.联系人email",
                       "投标方式":"2.投标方式",
                       "投标格式":"3.投标格式",
                       "下单时间":"7.下单日期",
                       "投标时间":"1.投标日期"
                    }
    for i,sectionName in enumerate(sectionNameDic.keys()):
        if sectionName == "投标方式":
            value = BIDMODE[int(dic[sectionNameDic[sectionName]])]
        elif sectionName == "投标格式":
            value = BIDMETHOD[int(dic[sectionNameDic[sectionName]])]
        elif sectionName in ["下单时间","投标时间"]:
            value = dic[sectionNameDic[sectionName]].FormatISODate()
        else:
            value = dic[sectionNameDic[sectionName]]
        sql = "UPDATE `订单信息` SET `%s`='%s' where `Index`=%s " %(sectionName,value,id)
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            print("error1")
            db.rollback()
            result=-1

    if dic["1.图纸文件 *"]!='':
        data = TransformBase64(dic["1.图纸文件 *"])
    else:
        data = ""
    sql = "UPDATE `订单信息` SET `客户原始技术图纸名`= '%s' where `Index`= %s "%(json.dumps(dic["1.图纸文件 *"],ensure_ascii=False), id)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("errorName")
        db.rollback()
        result=-1
    if dic["1.图纸文件 *"]!='':
        sql = "UPDATE `订单技术图纸信息` SET `技术图纸`= '%s' where `订单编号`= %s "%(data ,id)
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            print("error图2")
            db.rollback()
            result=-1

    # length = len(data)
    # if length%(1024*1024)>0:
    #     times = int(length/(1024*1024))+1
    # else:
    #     times = int(length/(1024*1024))
    # if times>2:
    #     times=2
    # for i in range(times):
    #     temp=data[i*(1024*1024):(i+1)*1024*1024]
    #     sql = "UPDATE `订单信息` SET `图%s`= '%s' where `Index`= %s "%(i, temp ,id)
    #     try:
    #         cursor.execute(sql)
    #         db.commit()  # 必须有，没有的话插入语句不会执行
    #     except:
    #         print("error图")
    #         db.rollback()
    #         result=-1
    # if times<2:#这部分代码是清空这次没用的存储字段
    #     for i in range(times,2):
    #         temp = ""
    #         sql = "UPDATE `订单信息` SET `图%s`= '%s' where `Index`= %s " % (i, temp, id)
    #         try:
    #             cursor.execute(sql)
    #             db.commit()  # 必须有，没有的话插入语句不会执行
    #         except:
    #             print("error图")
    #             db.rollback()
    #             result = -1
    db.close()
    return result

def UpdateConstructionInDB(log, whichDB,data):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()  #`图纸号`,`宽度`,`厚度`,`重量`,`图纸状态`,`图纸文件名`,`图纸大类`
    sql = "UPDATE 构件图纸信息表 SET `宽度`='%s',`长度`='%s',`厚度`='%s',`重量`='%s',`图纸状态`='%s',`图纸文件名`='%s',`图纸大类`='%s' WHERE `图纸号` = '%s'" \
          % (str(data[1]),str(data[2]),str(data[3]),str(data[4]),str(data[5]),str(data[6]),str(data[7]),str(data[0]))
    # sql = "INSERT INTO 图纸信息(`图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`," \
    #       "`热压100`,`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`图纸大类`,`创建时间`,`备注`)" \
    #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
    #       % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],datetime.date.today(),data[17])
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
    db.close()

def GetAllBoardList(log, whichDB,whichBoard,state='在用'):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if state=='全部':
        sql = """SELECT `板材`,`厚度`,`材质`,`密度`,`支持部件`,`支持宽度`,`颜色`,`状态` from `基材表单` 
                    where `板材`='%s'""" % (whichBoard)
    else:
        sql = """SELECT `板材`,`厚度`,`材质`,`密度`,`支持部件`,`支持宽度`,`颜色`,`状态` from `基材表单` 
                    where `板材`='%s' and `状态`='%s'"""%(whichBoard,state)
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

def GetRGBWithRalID(log,whichDB,RalID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `R`,`G`,`B`,`颜色名`,`颜色别名` from `ral标准色卡` where `RAL代码`='%s'"""%RalID
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp

def GetAllColor(log,whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `RAL代码`,`R`,`G`,`B`,`颜色名`,`颜色别名` from `ral标准色卡` """
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

def GetDeltaWithBluePrintNo(log,whichDB,bluePrintNo):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `面板增量`,`中板增量`,`背板增量` from `图纸信息` where `图纸号`='%s'"""%bluePrintNo
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp

def GetAllCeilingList(log,whichDB, type,state='在用'):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if state == '全部':
        sql = """SELECT `图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`,`热压100`,
                    `热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,'打包9000',`创建时间`,`备注` 
                    ,`a使能`,`a`,`b使能`,`b`,`c使能`,`c`,`d使能`,`d`,`e使能`,`e`,`f使能`,`f`,`CY使能`,`CY`,`图纸名` 
                    from `图纸信息` where `图纸大类`= '天花板'"""
    else:
        sql = """SELECT `图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`,`热压100`,
                    `热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,'打包9000',`创建时间`,`备注` 
                    ,`a使能`,`a`,`b使能`,`b`,`c使能`,`c`,`d使能`,`d`,`e使能`,`e`,`f使能`,`f`,`CY使能`,`CY`,`图纸名`
                    from `图纸信息` where `图纸大类`= '天花板' and `图纸状态`='%s'"""%state
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

def GetAllBluPrintList(log,whichDB, type,state='在用'):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if state == '全部':
        sql = """SELECT `图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`,`热压100`,
                    `热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,'打包9000',`创建时间`,`备注` 
                    ,`a使能`,`a`,`b使能`,`b`,`c使能`,`c`,`d使能`,`d`,`e使能`,`e`,`f使能`,`f`,`CY使能`,`CY`,`图纸名` 
                    from `图纸信息` where `图纸大类`= '墙板'"""
    else:
        sql = """SELECT `图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`,`热压100`,
                    `热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,'打包9000',`创建时间`,`备注` 
                    ,`a使能`,`a`,`b使能`,`b`,`c使能`,`c`,`d使能`,`d`,`e使能`,`e`,`f使能`,`f`,`CY使能`,`CY`,`图纸名`
                    from `图纸信息` where `图纸大类`= '墙板' and `图纸状态`='%s'"""%state
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

def GetAllConstructionList(log,whichDB, type,state='在用'):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if state == '全部':
        sql = """SELECT `图纸号`,`宽度`,`长度`,`厚度`,`重量`,`图纸状态`,`图纸文件名`,`图纸大类` from `构件图纸信息表` """
    else:
        sql = """SELECT `图纸号`,`宽度`,`长度`,`厚度`,`重量`,`图纸状态`,`图纸文件名`,`图纸大类` from `构件图纸信息表` where `图纸状态`='%s'"""%state
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

def GetConstructionDetailWithDrawingNo(log,whichDB,drawingNo):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `图纸号`,`宽度`,`长度`,`厚度`,`重量`,`图纸状态`,`图纸文件名`,`图纸大类` from `构件图纸信息表` where `图纸号`='%s'""" % drawingNo
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp

def SaveBluePrintInDB(log,whichDB,data):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "INSERT INTO 图纸信息(`图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`,`热压100`," \
          "`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`创建时间`,`备注`,`a使能`,`a`," \
          "`b使能`,`b`,`c使能`,`c`,`d使能`,`d`,`e使能`,`e`,`f使能`,`f`," \
          "`CY使能`,`CY`,`图纸名`,`图纸大类`)" \
          "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
          "'%s','%s','%s','%s','%s','%s','%s','%s','%s',%s," \
          "'%s',%s,'%s',%s,'%s',%s,'%s',%s,'%s',%s," \
          "'%s',%s,'%s','%s')"\
          % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],
             data[10],data[11],data[12],data[13],data[14],data[15],datetime.date.today(),data[17],data[18],int(data[19]),
             data[20],int(data[21]),data[22],int(data[23]),data[24],int(data[25]),data[26],int(data[27]),data[28],int(data[29]),
             data[30],int(data[31]),data[32],'墙板')
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
        print("error")
    db.close()

def SaveCeilingInDB(log,whichDB,data):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "INSERT INTO 图纸信息(`图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`,`热压100`," \
          "`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`创建时间`,`备注`,`a使能`,`a`," \
          "`b使能`,`b`,`c使能`,`c`,`d使能`,`d`,`e使能`,`e`,`f使能`,`f`," \
          "`CY使能`,`CY`,`图纸名`,`图纸大类`)" \
          "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
          "'%s','%s','%s','%s','%s','%s','%s','%s','%s',%s," \
          "'%s',%s,'%s',%s,'%s',%s,'%s',%s,'%s',%s," \
          "'%s',%s,'%s','%s')"\
          % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],
             data[10],data[11],data[12],data[13],data[14],data[15],datetime.date.today(),data[17],data[18],int(data[19]),
             data[20],int(data[21]),data[22],int(data[23]),data[24],int(data[25]),data[26],int(data[27]),data[28],int(data[29]),
             data[30],int(data[31]),data[32],'天花板')
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
        print("error")
    db.close()

def SaveConstructionInDB(log,whichDB,data):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "INSERT INTO 构件图纸信息表 (`图纸号`,`宽度`,`长度`,`厚度`,`重量`,`图纸状态`,`图纸文件名`,`图纸大类`)" \
          "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"\
          % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
        print("error")
    db.close()

def UpdateBluePrintInDB(log,whichDB,data):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE 图纸信息 SET `面板增量`='%s',`中板增量`='%s',`背板增量`='%s',`剪板505`='%s',`成型405`='%s'," \
          "`成型409`='%s',`成型406`='%s',`折弯652`='%s',`热压100`='%s',`热压306`='%s',`冲铣`='%s',`图纸状态`='%s',`创建人`='%s'," \
          "`中板`='%s',`打包9000`='%s',`图纸大类`='%s',`创建时间`='%s',`备注`='%s', `图纸大类`='墙板' WHERE `图纸号` = '%s'" \
          % (data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],
             data[13],data[14],data[15],data[16],datetime.date.today(),data[17],data[0])
    # sql = "INSERT INTO 图纸信息(`图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`," \
    #       "`热压100`,`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`图纸大类`,`创建时间`,`备注`)" \
    #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
    #       % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],datetime.date.today(),data[17])
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
    db.close()

def UpdateCeilingInDB(log,whichDB,data):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE 图纸信息 SET `面板增量`='%s',`中板增量`='%s',`背板增量`='%s',`剪板505`='%s',`成型405`='%s'," \
          "`成型409`='%s',`成型406`='%s',`折弯652`='%s',`热压100`='%s',`热压306`='%s',`冲铣`='%s',`图纸状态`='%s',`创建人`='%s'," \
          "`中板`='%s',`打包9000`='%s',`图纸大类`='%s',`创建时间`='%s',`备注`='%s', `图纸大类`='天花板' WHERE `图纸号` = '%s'" \
          % (data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],
             data[13],data[14],data[15],data[16],datetime.date.today(),data[17],data[0])
    # sql = "INSERT INTO 图纸信息(`图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`," \
    #       "`热压100`,`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`图纸大类`,`创建时间`,`备注`)" \
    #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
    #       % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],datetime.date.today(),data[17])
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
        print("error")
    db.close()

def UpdateDraftOrderStateInDB(log,whichDB,orderID,state):
    result=0
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1
    cursor = db.cursor()
    sql = "UPDATE 订单信息 SET `状态`='%s' WHERE `订单编号` = %s" % (state,int(orderID))
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
        print("error")
        result = -1
    db.close()
    return result

def UpdateSubOrderStateInDB(log, whichDB, orderID, subOrderState):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE 订单信息 SET `子订单状态`='%s' WHERE `订单编号` = %s" % (subOrderState,int(orderID))
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
        print("error")
    db.close()

def UpdatePropertyInDB(log,whichDB,propertyDic):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE 系统参数 SET `启动纵切最小板材数`='%s', `任务单每页行数`='%s', `墙角板型号列表`='%s' " %(propertyDic["启动纵切最小板材数"],propertyDic["任务单每页行数"],json.dumps(propertyDic["墙角板型号列表"],ensure_ascii=False))
    # sql = "INSERT INTO 图纸信息(`图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`," \
    #       "`热压100`,`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`图纸大类`,`创建时间`,`备注`)" \
    #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
    #       % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],datetime.date.today(),data[17])
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
        print("error")
    db.close()

def GetPropertyVerticalCuttingParameter(log,whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `启动纵切最小板材数` from `系统参数` """
    cursor.execute(sql)
    temp = cursor.fetchone()
    db.close()
    return 0, temp[0]

def GetPropertyLShapeWallTypeList(log,whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `墙角板型号列表` from `系统参数` """
    cursor.execute(sql)
    temp = cursor.fetchone()
    temp = json.loads(temp[0])
    db.close()
    return 0, temp

def GetPropertySchedulePageRowNumber(log,whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `任务单每页行数` from `系统参数` """
    cursor.execute(sql)
    temp = cursor.fetchone()
    db.close()
    return 0, temp[0]

def GetSubOrderPackageState(log,whichDB,orderID,suborderID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `状态` from `%s` where `子订单号`= '%s' """%(str(orderID),suborderID)

    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    if temp==None:
        return 0,[]
    else:
        return 0, temp[0]

def GetTableListFromDB(log,whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "select table_name from information_schema.tables where table_schema='%s'"%orderDBName[whichDB]
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    result=[]
    for i in temp:
        result.append(i[0])
    return 0, result

def GetPackageListFromDB(log,whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % packageDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "select table_name from information_schema.tables where table_schema='%s'"%packageDBName[whichDB]
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    result=[]
    for i in temp:
        result.append(i[0])
    return 0, result

def InsertNewOrderRecord(log,whichDB):
    return

def CreateNewOrderSheet(log,whichDB,newOrderID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """CREATE TABLE `%d` (
            `Index` INT(11) NOT NULL AUTO_INCREMENT,
            `订单号` INT(11) NOT NULL,
            `子订单号` VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8_general_ci',
            `甲板` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `区域` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `房间` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `图纸` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `产品类型` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `面板代码` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `数量` INT(11) NOT NULL,
            `宽度` VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8_general_ci',
            `高度` VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8_general_ci',
            `厚度` VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8_general_ci',
            `X面材质` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `X面颜色` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `Y面材质` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `Y面颜色` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `Z面材质` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `Z面颜色` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `V面材质` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `V面颜色` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `备注` TEXT NOT NULL COLLATE 'utf8_general_ci',
            `重量` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `胶水单编号` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `胶水单注释` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `所处工位` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `状态` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            PRIMARY KEY (`Index`) USING BTREE
        )
        COLLATE='utf8_general_ci'
        ENGINE=InnoDB
        AUTO_INCREMENT=0
        ;
        """%newOrderID
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error")
        db.rollback()
    db.close()

def CreatePackagePanelSheetForOrder(log,whichDB,newOrderID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """CREATE TABLE `%s` (
            `Index` INT(11) NOT NULL AUTO_INCREMENT,
            `订单号` INT(11) NOT NULL,
            `子订单号` VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8_general_ci',
            `甲板` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `区域` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `房间` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `图纸` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `产品类型` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `面板代码` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `宽度` VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8_general_ci',
            `高度` VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8_general_ci',
            `厚度` VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8_general_ci',
            `X面颜色` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `Y面颜色` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `Z面颜色` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `V面颜色` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `备注` TEXT NOT NULL COLLATE 'utf8_general_ci',
            `重量` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `胶水单编号` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `胶水单注释` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `状态` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `所属货盘` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
          PRIMARY KEY (`Index`) USING BTREE
        )
        COLLATE='utf8_general_ci'
        ENGINE=InnoDB
        AUTO_INCREMENT=0
        ;
        """%newOrderID
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error new4")
        db.rollback()
    db.close()

def CreatePackageSheetForOrder(log,whichDB,newOrderID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % packageDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """CREATE TABLE `%s` (
            `Index` INT(11) NOT NULL AUTO_INCREMENT,
            `货盘编号` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `货盘长` INT(10) UNSIGNED NOT NULL DEFAULT '0',
            `货盘宽` INT(10) UNSIGNED NOT NULL DEFAULT '0',
            `货盘高` INT(10) UNSIGNED NOT NULL DEFAULT '0',
            `货盘层数` INT(10) UNSIGNED NOT NULL DEFAULT '0',
            `货盘总重` VARCHAR(50) NOT NULL DEFAULT '0' COLLATE 'utf8_general_ci',
            `货盘总面板数` VARCHAR(50) NOT NULL DEFAULT '0' COLLATE 'utf8_general_ci',
            `货盘总面积` VARCHAR(50) NOT NULL DEFAULT '0' COLLATE 'utf8_general_ci',
            `货盘所属子订单` VARCHAR(50) NOT NULL DEFAULT '0' COLLATE 'utf8_general_ci',
            `货盘所属甲板` VARCHAR(50) NOT NULL DEFAULT '0' COLLATE 'utf8_general_ci',
            `货盘所属区域` VARCHAR(50) NOT NULL DEFAULT '0' COLLATE 'utf8_general_ci',
            `货盘所属房间` VARCHAR(50) NOT NULL DEFAULT '0' COLLATE 'utf8_general_ci',
	        `货盘打包方式` VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8_general_ci',
            `货盘类别` VARCHAR(50) NOT NULL DEFAULT '0' COLLATE 'utf8_general_ci',
            `货盘数据` TEXT NOT NULL COLLATE 'utf8_general_ci',
            `备注` VARCHAR(50) NOT NULL DEFAULT '0' COLLATE 'utf8_general_ci',
            PRIMARY KEY (`Index`) USING BTREE
        )
        COLLATE='utf8_general_ci'
        ENGINE=InnoDB
        AUTO_INCREMENT=0
        ;
        """%newOrderID
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error new5")
        db.rollback()
    db.close()

def GetSubOrderPanelsForPackage(log,whichDB,orderID,suborderID=None):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if suborderID == None:
        sql = """SELECT `Index`,`订单号`,`子订单号`,`甲板`,`区域`,`房间`,`图纸`,`产品类型`,`面板代码`,`数量`,`高度`,`宽度`,`厚度`,`X面颜色`,`Y面颜色`,`Z面颜色`,`V面颜色`,`胶水单编号`,`重量`,`状态` from `%s` """ % (str(orderID))
    else:
        sql = """SELECT `Index`,`订单号`,`子订单号`,`甲板`,`区域`,`房间`,`图纸`,`产品类型`,`面板代码`,`数量`,`高度`,`宽度`,`厚度`,`X面颜色`,`Y面颜色`,`Z面颜色`,`V面颜色`,`胶水单编号`,`重量`,`状态` from `%s` where `子订单号`='%s'""" %(str(orderID),str(suborderID))
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    result =[]
    for i in temp:
        if not i[6][2:5].isdigit():
            result.append(list(i))
    db.close()
    return 0, result

def InsertPackageBoxInfo(log,whichDB,orderID,suborderID,boxInfo):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % packageDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    # sql ="""UPDATE `%s` SET `货盘长`=%s, `货盘宽`=%s, `货盘高`=%s, `货盘层数`=%s ,`货盘数据`='%s', `货盘总重`='%s', `货盘总面板数`='%s', `货盘总面积`='%s'  where `Index`=%s""" \
    #       %(str(orderID),boxLength,boxWidth,boxHeight,boxLayer,json.dumps(data),str(weight),str(amount),square,index)
    for data in boxInfo:
        sql = "INSERT INTO `%s` (`货盘编号`,`货盘长`,`货盘宽`,`货盘高`,  `货盘层数`,`货盘总重`,`货盘总面板数`,  `货盘总面积`,    `货盘所属子订单`,`货盘所属甲板`,`货盘所属区域`,`货盘所属房间`,`货盘打包方式`,`货盘类别`)" \
                         "VALUES ('%s'      ,%s,       %s ,    %s,      %s ,     '%s',      '%s',           '%s',          '%s',        '%s',          '%s',      '%s',        '%s',      '%s')"\
              % ( str(orderID),  '待定中',   data[0],data[1],data[2],data[3],str(data[4]),str(data[5]),str(data[6]),str(suborderID),   data[7],        data[8],  data[9],     data[10],  data[11])
        # sql = "INSERT INTO `%s` (`货盘编号`,`货盘长`,`货盘宽`,`货盘高`,  `货盘层数`,`货盘总重`,`货盘总面板数`,  `货盘总面积`,    `货盘所属子订单`,`货盘所属甲板`,`货盘所属区域`,`货盘所属房间`,`货盘打包方式`,`货盘类别`)" \
        #                  "VALUES ('%s'    %s,       %s ,    %s,      %s ,     '%s',      '%s',           '%s',          '%s',        '%s',          '%s',      '%s',        '%s',      '%s')"\
        #       % ( str(orderID),  '待定中',data[0],  data[1],data[2],data[3],str(data[4]),str(data[5]),str(data[6]),str(suborderID),   data[7],        data[8],  data[9],     data[10],  data[11])
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            print("error Insert1")
            db.rollback()

        sql = """SELECT `Index` from `%s` where `货盘编号`='%s'""" % (str(orderID), '待定中')
        cursor.execute(sql)
        index = cursor.fetchone()[0]  # 获得索引值
        Data=data[-1]
        for i,layer in enumerate(Data):
            for j,row in enumerate(layer):
                for k,col in enumerate(row):
                    Data[i][j][k][-3]="托盘%s"%str(index)
                    Data[i][j][k][-1]=""

        sql = "UPDATE `%s` SET `货盘编号`='托盘%s', `货盘数据`='%s' where `Index`=%s " %(str(orderID),str(index),json.dumps(Data,ensure_ascii=False),index)
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            print("error1")
            db.rollback()
    db.close()

def UpdateSpecificPackageBoxInfo(log,whichDB,orderID,index,boxLength,boxWidth,boxHeight,boxLayer,data,weight=0,amount=0,square=0):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % packageDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    square="%.2f"%(square)
    sql ="""UPDATE `%s` SET `货盘长`=%s, `货盘宽`=%s, `货盘高`=%s, `货盘层数`=%s ,`货盘数据`='%s', `货盘总重`='%s', `货盘总面板数`='%s', `货盘总面积`='%s'  where `Index`=%s""" \
          %(str(orderID),boxLength,boxWidth,boxHeight,boxLayer,json.dumps(data,ensure_ascii=False),str(weight),str(amount),square,index)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error1")
        db.rollback()
    db.close()

def DeleteSuborderPackageDB(log,whichDB,orderID,suborderID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % packageDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()

    sql = """DELETE from `%s` where `货盘所属子订单`='%s' """ % (str(orderID), str(suborderID))
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error")
        db.rollback()
    db.close()


def DeleteNewPackageBoxInPackageDBWithBoxName(log,whichDB,orderID,boxName):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % packageDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """DELETE from `%s` where `货盘编号`='%s' """ % (str(orderID), boxName)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error")
        db.rollback()
    db.close()

def DeleteNewPackageBoxInPackageDB(log,whichDB,orderID,index):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % packageDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """DELETE from `%s` where `Index`=%s """ % (str(orderID), index)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error")
        db.rollback()
    db.close()


def GetSpecificPackageBoxData(log,whichDB,orderID,index):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % packageDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `货盘编号`, `货盘长`, `货盘宽`, `货盘高`, `货盘层数`, `货盘总重`, `货盘总面板数`, `货盘总面积`,  
    `货盘所属子订单`,`货盘所属甲板`, `货盘所属区域`, `货盘所属房间`, `货盘打包方式`, `货盘类别`, `货盘数据` from `%s` 
    where `Index`=%s """ \
          % (str(orderID), index)
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    temp = list(temp)
    temp[14] = json.loads(temp[14])
    db.close()
    return 0, temp

def GetSubOrderPackageNumber(log,whichDB,orderID,suborderID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % packageDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `货盘编号` from `%s` where `货盘所属子订单`='%s' """ % (str(orderID), str(suborderID))
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    result = len(temp)
    db.close()
    return 0, result

def GetSubOrderPackageData(log,whichDB,orderID,suborderID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % packageDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `货盘编号`, `货盘长`, `货盘宽`, `货盘高`, `货盘层数`, `货盘总重`, `货盘总面板数`, `货盘总面积`,  
    `货盘所属子订单`,`货盘所属甲板`, `货盘所属区域`, `货盘所属房间`, `货盘打包方式`, `货盘类别`, `货盘数据` from `%s` 
    where `货盘所属子订单`='%s' """ \
          % (str(orderID), str(suborderID))
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    result =[]
    for record in temp:
        record = list(record)
        record[-1] = json.loads(record[-1])
        result.append(list(record))
    db.close()
    return 0, result

def GetSuborderAllPackageList(log,whichDB,orderID,suborderID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % packageDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `货盘编号`, `货盘长`, `货盘宽`, `货盘高`, `货盘层数`, `货盘总重`, `货盘总面板数`, `货盘总面积`,  
    `货盘所属子订单`,`货盘所属甲板`, `货盘所属区域`, `货盘所属房间`, `货盘打包方式`, `货盘类别`, `货盘数据` from `%s` 
    where `货盘所属子订单`='%s' """ \
          % (str(orderID), str(suborderID))
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    result =[]
    for record in temp:
        record = list(record)
        record[-1] = json.loads(record[-1])
        result.append(list(record))
    db.close()
    return 0, result


def GetCurrentPackageData(log,whichDB,orderID,suborderID,deck,zone,room=None):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % packageDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if room==None:
        sql = """SELECT `货盘编号`, `货盘长`, `货盘宽`, `货盘高`, `货盘层数`, `货盘总重`, `货盘总面板数`, `货盘总面积`,  
        `货盘所属子订单`,`货盘所属甲板`, `货盘所属区域`, `货盘所属房间`, `货盘打包方式`, `货盘类别`, `货盘数据` from `%s` 
        where `货盘所属子订单`='%s' and `货盘所属甲板`='%s' and `货盘所属区域`='%s' """ \
              % (str(orderID), str(suborderID), str(deck), str(zone))
    else:
        sql = """SELECT `货盘编号`, `货盘长`, `货盘宽`, `货盘高`, `货盘层数`, `货盘总重`, `货盘总面板数`, `货盘总面积`,  
        `货盘所属子订单`,`货盘所属甲板`, `货盘所属区域`, `货盘所属房间`, `货盘打包方式`, `货盘类别`, `货盘数据` from `%s` 
        where `货盘所属子订单`='%s' and `货盘所属甲板`='%s' and `货盘所属区域`='%s' and `货盘所属房间`='%s' """ \
              % (str(orderID), str(suborderID), str(deck), str(zone), str(room))
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    result =[]
    for record in temp:
        record = list(record)
        record[-1] = json.loads(record[-1])
        result.append(list(record))
    db.close()
    return 0, result


def GetSubOrderPanelsForPackageFromPackageDB(log,whichDB,orderID,suborderID=None):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    dbName = "p%s-%03d"%(orderID,int(suborderID))
    if suborderID == None:

        sql = """SELECT `Index`,`订单号`, `子订单号`, `甲板`, `区域`, `房间`, `图纸`, `产品类型`, `面板代码`,  `高度`,`宽度`, `厚度`, `X面颜色`, `Y面颜色`, `Z面颜色`, `V面颜色`, `备注`, `重量`, `胶水单编号`, `胶水单注释`, `状态`, `所属货盘` from `%s` """ % (str(dbName))
    else:
        sql = """SELECT `Index`,`订单号`, `子订单号`, `甲板`, `区域`, `房间`, `图纸`, `产品类型`, `面板代码`,  `高度`,`宽度`, `厚度`, `X面颜色`, `Y面颜色`, `Z面颜色`, `V面颜色`, `备注`, `重量`, `胶水单编号`, `胶水单注释`, `状态`, `所属货盘` from `%s` where `子订单号`='%s'""" %(str(dbName),str(suborderID))
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    result =[]
    for i in temp:
        if not i[6][2:5].isdigit():
            x = list(i)
            x[9]=int(x[9])
            x[10]=int(x[10])
            x[11]=int(x[11])
            result.append(x)
    db.close()
    return 0, result


def InsertNewOrderRecord(log,whichDB,newOrderID,newOrderName,subOrderIDList):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    subOrderIdStr=str(int(subOrderIDList[0]))
    for i in subOrderIDList[1:]:
        subOrderIdStr += ','
        subOrderIdStr += str(int(i))
    # sql = "INSERT INTO 订单信息(`订单编号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`," \
    #       "`热压100`,`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`图纸大类`,`创建时间`,`备注`)" \
    #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
    #       % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],datetime.date.today(),data[17])
    sql = "INSERT INTO 订单信息(`订单编号`,`订单名称`,`子订单编号`) VALUES (%s,'%s','%s')" %(int(newOrderID),newOrderName,subOrderIdStr)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error")
        db.rollback()
    db.close()

def UpdateSeperatePanelBoxNumberAndState(log, whichDB, orderID,suborderID, index, state, boxNum):
    name="p%s-%03d"%(str(orderID),int(suborderID))
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE `%s` SET `状态`='%s', `所属货盘`='%s'  where `Index`=%s" %(name,state,boxNum,index)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error2")
        db.rollback()
    db.close()

def ClearSeperatePanelBoxNumberWithIndex(log, whichDB, orderID, suborderID, index):
    name="p%s-%03d"%(str(orderID),int(suborderID))
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE `%s` SET `所属货盘`=''  where `Index`=%s" %(name, index)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error2")
        db.rollback()
    db.close()

# def UpdateSeperatePanelBoxNumberAndState(log, whichDB, orderID, index, state, boxNum):
#     name="p%s"%str(orderID)
#     try:
#         db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
#                              passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
#     except:
#         wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
#         if log:
#             log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
#         return -1, []
#     cursor = db.cursor()
#     sql = "UPDATE `%s` SET `状态`='%s', `所属货盘`='%s'  where `Index`=%s" %(name,state,boxNum,index)
#     try:
#         cursor.execute(sql)
#         db.commit()  # 必须有，没有的话插入语句不会执行
#     except:
#         print("error2")
#         db.rollback()
#     db.close()
#
def UpdateSubOrderPackageState(log,whichDB,orderID,subOrderId,state):
    name="p%s-%03d"%(str(orderID),int(subOrderId))
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!"%orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE `%s` SET `状态`='%s'  where `子订单号`='%s'" %(name,state,str(subOrderId))
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("执行更新p%s-3d中子订单打包状态时未成功！"%(str(orderID),int(subOrderId)))
        db.rollback()
    db.close()

def UpdateSubOrderPackageStateAndClearPackageNumber(log,whichDB,orderID,subOrderId,state,packageNum):
    name="p%s-%03d"%(str(orderID),int(subOrderId))
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!"%orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE `%s` SET `状态`='%s',`所属货盘`='%s' where `子订单号`='%s'" %(name,state,packageNum,str(subOrderId))
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("执行更新p%s-3d中子订单打包状态时未成功！"%(str(orderID),int(subOrderId)))
        db.rollback()
    db.close()

def UpdatePanelPackageStateInPOrderDB(log,whichDB,boxName,data):
    dbName = "p%s-%3d"%str(data[1],int(data[2]))
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if len(data)>0:
        index = int(data[0])
        sql = "UPDATE `%s` SET `所属货盘`='%s' where `Index`=%s" %(dbName,str(boxName),index)
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            print("error1")
            db.rollback()
    db.close()

def UpdateOrderRecord(log,whichDB,OrderID,subOrderIdStr,subOrderStateStr):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    # sql = "INSERT INTO 订单信息(`订单编号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`," \
    #       "`热压100`,`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`图纸大类`,`创建时间`,`备注`)" \
    #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
    #       % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],datetime.date.today(),data[17])
    sql = "UPDATE 订单信息 SET `子订单编号`='%s', `子订单状态`='%s' where `订单编号`=%s" %(subOrderIdStr,subOrderStateStr,int(OrderID))
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error1")
        db.rollback()
    db.close()

def UpdatePanelGlueNoInDB(log, whichDB, orderID, index, glueNo):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE `%s` SET `胶水单编号`='%s'  where `Index`=%s" %(orderID,glueNo,int(index))
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error1")
        db.rollback()
    db.close()

def UpdatePanelWeightInDB(log, whichDB, orderID, index, weight):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE `%s` SET `重量`='%.2f'  where `Index`=%s" %(orderID,weight,int(index))
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error1")
        db.rollback()
    db.close()

def UpdatePanelGluePageInDB(log, whichDB, orderID, glueNo, gluePage):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE `%s` SET `胶水单注释`='%s'  where `胶水单编号`='%s'" %(orderID,gluePage,glueNo)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error1")
        db.rollback()
    db.close()

def UpdatePanelGlueLabelPageInDB(log, whichDB, orderID, glueNo, gluePage):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE `%s` SET `备注`='%s'  where `胶水单编号`='%s'" %(orderID,gluePage,glueNo)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error1")
        db.rollback()
    db.close()

def GetOrderDetailRecord(log, whichDB, orderDetailID,suborderNum=None):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if suborderNum == None:
        sql = """SELECT `Index`,`订单号`,`子订单号`,`甲板`,`区域`,`房间`,`图纸`,`面板代码`,`X面颜色`,`Y面颜色`,`高度`,`宽度`,`厚度`,`数量`,`Z面颜色`,`V面颜色`,`胶水单编号` from `%s` """%(str(orderDetailID))
    else:
        sql = """SELECT `Index`,`订单号`,`子订单号`,`甲板`,`区域`,`房间`,`图纸`,`面板代码`,`X面颜色`,`Y面颜色`,`高度`,`宽度`,`厚度`,`数量`,`Z面颜色`,`V面颜色`,`胶水单编号` from `%s` where `子订单号`='%s'"""%(str(orderDetailID),str(suborderNum))

    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

def GetDraftOrderDetailByID(log,whichDB, id):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql="select * from `订单信息` where `Index`=%s"%id
    cursor.execute(sql)
    result = cursor.fetchall()
    column = [index[0] for index in cursor.description]
    data_dict = [dict(zip(column,row)) for row in result]
    db.close()
    return 0, data_dict[0]


def GetDraftOrderDetail(log,whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql="select * from `订单信息` "
    cursor.execute(sql)
    result = cursor.fetchall()
    column = [index[0] for index in cursor.description]
    data_dict = [dict(zip(column,row)) for row in result]
    db.close()
    return 0, data_dict


def GetOrderPanelRecord(log, whichDB, orderDetailID,suborderNum=None):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if suborderNum == None:
        sql = """SELECT `Index`,`订单号`,`子订单号`,`甲板`,`区域`,`房间`,`图纸`,`面板代码`,`X面颜色`,`Y面颜色`,`高度`,`宽度`,`厚度`,`数量`,`Z面颜色`,`V面颜色`,`胶水单编号`,`产品类型` from `%s` """%(str(orderDetailID))
    else:
        sql = """SELECT `Index`,`订单号`,`子订单号`,`甲板`,`区域`,`房间`,`图纸`,`面板代码`,`X面颜色`,`Y面颜色`,`高度`,`宽度`,`厚度`,`数量`,`Z面颜色`,`V面颜色`,`胶水单编号`,`产品类型` from `%s` where `子订单号`='%s'"""%(str(orderDetailID),str(suborderNum))

    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    result = []
    for record in temp:
        if not record[-1].isdigit():
            result.append(record[:-1])
    return 0, result

def GetGluepageFromGlueNum(log, whichDB, orderID,glueNum):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `胶水单注释` from `%s` where `胶水单编号`= '%s' """%(str(orderID),glueNum)

    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp[0]

def GetGlueLabelpageFromGlueNum(log, whichDB, orderID,glueNum):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `备注` from `%s` where `胶水单编号`= '%s' """%(str(orderID),glueNum)

    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp[0]

def InsertOrderDetailRecord(log,whichDB,OrderID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    # sql = "INSERT INTO 订单信息(`订单编号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`," \
    #       "`热压100`,`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`图纸大类`,`创建时间`,`备注`)" \
    #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
    #       % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],datetime.date.today(),data[17])
    sql = "INSERT INTO '%s'(`订单号`) VALUES (%s)" % (OrderID,1)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
    db.close()

def InsertBatchOrderDataIntoDB(log, whichDB, orderTabelName, orderDataList):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    for data in orderDataList:
        if '.' in data[4]:
            temp = data[4].split('.')
        else:
            temp=[0]*3
            temp[0]=data[4][0]
            temp[1]=data[4][1:4]
            temp[2]=data[4][4:]
        if not temp[2].isdigit():
            string1=temp[2]
            num = ord(string1[0].upper()) - ord('A')
            num += 10
            string1 = str(num) + string1[1:]
            string1 = int(string1)
        else:
            string1=int(temp[2])
        data[4]="%s.%s.%04d"%(temp[0],temp[1],string1)
        if data[8]!=None:
            data[8]=str(data[8]).replace('-','')
            data[8]=data[8].strip().upper()
        if data[9]!=None:
            data[9]=str(data[9]).replace('-','')
            data[9]=data[9].strip().upper()
        if data[10]!=None:
            data[10]=str(data[10]).replace('-','')
            data[10]=data[10].strip().upper()
        if data[11]!=None:
            data[11]=str(data[11]).replace('-','')
            data[11]=data[11].strip().upper()

        sql="""INSERT INTO `%d`(`订单号`,`子订单号`,`甲板`,`区域`,`房间`,`图纸`,`宽度`,`高度`,`厚度`,`X面颜色`,`Y面颜色`,`Z面颜色`,`V面颜色`,`数量`,`面板代码`,`产品类型`)
        VALUES (%d,%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d,'%s','%s')"""\
            %(int(orderTabelName),int(orderTabelName),int(data[0]),data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],int(data[12]),data[13],temp[1])
        cursor.execute(sql)
        try:
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            db.rollback()
    db.close()

def CreateNewPackageBoxInBoxDB(log, whichDB,orderID,suborderID,deck,zone,room=""):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % packageDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s数据库!"% packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s数据库"% packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if room=="":
        mode = "按区域打包"
    else:
        mode = "按房间打包"
    sql="""INSERT INTO `%s`(`货盘所属子订单`,`货盘所属甲板`,`货盘所属区域`  ,`货盘所属房间`,`货盘打包方式`)
    VALUES (                 '%s',         '%s',               '%s',       '%s'     ,'%s')"""\
         %(str(orderID),str(suborderID),      deck,         zone,         room,       mode)
    cursor.execute(sql)
    try:
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
        print("erro box new")
    sql = """SELECT `Index` from `%s` where `货盘编号`= '' and `货盘所属子订单`= '%s' and `货盘所属甲板`= '%s' 
                and `货盘所属区域`= '%s' and `货盘所属房间`= '%s'"""\
          %(str(orderID),str(suborderID),deck,zone,room)
    cursor.execute(sql)
    boxNum = cursor.fetchone()
    if boxNum!=None:
        boxNum=boxNum[0]
        sql = "UPDATE `%s` SET `货盘编号`='托盘%s' where `Index`= %s "% (str(orderID),str(boxNum),boxNum)
        # sql = "INSERT INTO 图纸信息(`图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`," \
        #       "`热压100`,`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`图纸大类`,`创建时间`,`备注`)" \
        #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
        #       % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],datetime.date.today(),data[17])
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            db.rollback()
    else:
        boxNum = -1
    db.close()
    return boxNum

def InsertPanelDetailIntoPackageDB(log, whichDB, orderTabelName, orderDataList):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % orderDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % orderDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
                              # [64731,      '1',          '3', '9','Corridor','C.C72.0005', 'C72', 'H40RDA',  '400', '1280',  '50',  'RAL9010',    'G',   'None', 'None',     '',     '3.07', '64731-0102',  '',       '',      '']
    for data in orderDataList:
        sql="""INSERT INTO `%s`(`订单号`,  `子订单号`      ,`甲板`,`区域`  ,`房间`,   `图纸`    ,`产品类型`,`面板代码`  ,`高度` ,`宽度`, `厚度`,  `X面颜色`, `Y面颜色`,`Z面颜色`,  `V面颜色`, `胶水单编号`, `重量`   ,`胶水单注释`,`状态`,`所属货盘`)
        VALUES (                  %d,      '%s',          '%s', '%s',  '%s',     '%s',       '%s'  ,  '%s'    , '%s',  '%s',   '%s',   '%s',      '%s',     '%s',     '%s',       '%s',    '%s',    '%s',      '%s',    '%s')"""\
      %(orderTabelName    ,int(data[0]),int(data[1]),  data[2],data[3],data[4], data[5],   data[6] ,data[7],   data[8],data[9],data[10],data[11],data[12],data[13],  data[14], data[15],data[16] ,data[17], data[18], data[19])
        cursor.execute(sql)
        try:
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            db.rollback()
            print("erro package new")
    db.close()

def InsertNewOrder(log,whichDB,dic,operatorID):
    result = 1
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    # sql = "UPDATE 系统参数 SET `启动纵切最小板材数`='%s', `任务单每页行数`='%s', `墙角板型号列表`='%s' " %(propertyDic["启动纵切最小板材数"],propertyDic["任务单每页行数"],json.dumps(propertyDic["墙角板型号列表"]))
    sql = "INSERT INTO `订单信息` (`下单员ID`,`备注`) VALUES ('%s','%s')"%(operatorID,operatorID)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error Insert2")
        db.rollback()
    sql = """SELECT `Index` from `订单信息` where `备注`= '%s' and `订单编号`= 0"""%(operatorID)
    cursor.execute(sql)
    id = cursor.fetchone()[0]
    sql = "UPDATE `订单信息` SET `订单编号`= %s, `备注`='' where `Index`=%s " %(int(id),id)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error1")
        db.rollback()

    # sql = "INSERT INTO `订单技术图纸信息` (`订单编号`) VALUES (%s)"%(int(id))
    # try:
    #     cursor.execute(sql)
    #     db.commit()  # 必须有，没有的话插入语句不会执行
    # except:
    #     print("error Insert3")
    #     db.rollback()

    sectionNameDic={
                       "订单名称":"1.订单名称 *",
                       "草稿订单类别":"2.草稿订单类别",
                       "客户名称":"3.客户单位名称",
                       "客户公司信息":"4.客户公司信息",
                       "联系人":"5.联系人姓名 *",
                       "联系人电话":"6.联系人电话",
                       "联系人邮箱":"7.联系人email *",
                       # "投标方式":"2.投标方式",
                       # "投标格式":"3.投标格式",
                       "下单时间":"8.下单日期",
                       "投标时间":"1.投标日期"
                    }
    for i,sectionName in enumerate(sectionNameDic.keys()):
        if sectionName == "投标方式":
            value = BIDMODE[int(dic[sectionNameDic[sectionName]])]
        elif sectionName == "投标格式":
            value = BIDMETHOD[int(dic[sectionNameDic[sectionName]])]
        elif sectionName in ["下单时间","投标时间"]:
            value = dic[sectionNameDic[sectionName]].FormatISODate()
        else:
            value = dic[sectionNameDic[sectionName]]
        sql = "UPDATE `订单信息` SET `%s`='%s' where `Index`=%s " %(sectionName,value,id)
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            print("error1")
            db.rollback()

    if dic["1.产品清单或图纸文件"]!='':
        data = TransformBase64(dic["1.产品清单或图纸文件"])
    else:
        data = ""
    sql = "UPDATE `订单信息` SET `客户原始技术图纸名`= '%s' where `Index`= %s "%(json.dumps(dic["1.产品清单或图纸文件"],ensure_ascii=False), id)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("errorName")
        db.rollback()
        result=-1
    sql = "UPDATE `订单技术图纸信息` SET `技术图纸`= '%s' where `订单编号`= %s "%( data ,int(id))
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error图1")
        db.rollback()
        result=-1

    # length = len(data)
    # if length%(1024*1024)>0:
    #     times = int(length/(1024*1024))+1
    # else:
    #     times = int(length/(1024*1024))
    # if times>2:
    #     times=2
    # for i in range(times):
    #     temp=data[i*(1024*1024):(i+1)*1024*1024]
    #     sql = "UPDATE `订单信息` SET `图%s`= '%s' where `Index`= %s "%(i, temp ,id)
    #     try:
    #         cursor.execute(sql)
    #         db.commit()  # 必须有，没有的话插入语句不会执行
    #     except:
    #         print("error图")
    #         db.rollback()
    #         result=-1
    db.close()
    return result

def GetPDF(log,whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    # sql = "UPDATE 系统参数 SET `启动纵切最小板材数`='%s', `任务单每页行数`='%s', `墙角板型号列表`='%s' " %(propertyDic["启动纵切最小板材数"],propertyDic["任务单每页行数"],json.dumps(propertyDic["墙角板型号列表"]))
    # sql = "INSERT INTO `订单信息` (`订单名称`,`客户原始技术图纸名`,`客户原始技术图纸`) VALUES ('%s', '%s', %s)"%(propertyDic["1.订单名称"], json.dumps(propertyDic["1.图纸文件"],ensure_ascii=False), MySQLdb.Binary(img))
    # sql = "INSERT INTO `订单信息` (`订单名称`,`客户原始技术图纸名`,`图`) VALUES ('%s', '%s', '%s')"%(propertyDic["1.订单名称"], json.dumps(propertyDic["1.图纸文件"],ensure_ascii=False), data)
    # sql = """INSERT INTO `订单信息` (`图`) VALUES (%s)""" %(img)
    sql = "select `图`  from `订单信息` where `Index`=%s" % (70)
    cursor.execute(sql)
    record=cursor.fetchone()
    db.close()
    with open('TJDZ_1.pdf', 'wb') as file:
        image = base64.b64decode(record[0])  # 解码
        file.write(image)
        file.close()

def UpdateOrderOperatorCheckStateByID(log,whichDB,id,state,quotationDate,exchangeRateDate):
    id = int(id)
    result = 1
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    # sql = "UPDATE `订单信息` SET `订单部审核状态`= '%s',`报价参考日期`= '%s',`汇率参考日期`= '%s' where `Index`= %s " % (state,quotationDate,exchangeRateDate,id)
    sql = "UPDATE `订单信息` SET `订单部审核状态`= '%s' where `Index`= %s " % (state,id)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("修改订单部审核状态出错！")
        db.rollback()
        result = -1
    db.close()
    return result

def UpdateTechCheckStateByID(log,whichDB,id,state):
    id = int(id)
    result = 1
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE `订单信息` SET `设计审核状态`= '%s' where `Index`= %s " % (state,id)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("修改设计审核状态出错！")
        db.rollback()
        result = -1
    db.close()
    return result

def UpdatePurchchaseCheckStateByID(log,whichDB,id,state):
    id = int(id)
    result = 1
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE `订单信息` SET `采购审核状态`= '%s' where `Index`= %s " % (state,id)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("修改设计审核状态出错！")
        db.rollback()
        result = -1
    db.close()
    return result

def UpdateFinancingCheckStateByID(log,whichDB,id,state):
    id = int(id)
    result = 1
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE `订单信息` SET `财务审核状态`= '%s' where `Index`= %s " % (state,id)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("修改设计审核状态出错！")
        db.rollback()
        result = -1
    db.close()
    return result

def UpdateManagerCheckStateByID(log,whichDB,id,state,quotationDate=None,exchangeRateDate=None):
    id = int(id)
    result = 1
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE `订单信息` SET `经理审核状态`= '%s',`报价参考日期`= '%s',`汇率参考日期`= '%s' where `Index`= %s " % (state,str(quotationDate),str(exchangeRateDate),id)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("修改经理审核状态出错！")
        db.rollback()
        result = -1
    db.close()
    return result

def UpdateOrderSquareByID(log,whichDB,id,square):
    id = int(id)
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return []
    cursor = db.cursor()
    sql = "UPDATE `订单信息` SET `产品数量`= '%s' where `Index`= %s " % (square, id)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("修改设计审核状态出错！")
        db.rollback()
        result = -1
    db.close()


def UpdateDraftCheckInfoByID(log, whichDB, id, dicList):
    id = int(id)
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderCheckDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return []
    cursor = db.cursor()
    sql = "DROP TABLE IF EXISTS `%s`"%id
    cursor.execute(sql)
    sql = """CREATE TABLE `%s` (
            `Index` INT(11) NOT NULL AUTO_INCREMENT,
            `类别` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
            `产品名称` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
            `产品型号` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `产品表面材料` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
            `产品长度` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `产品宽度` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `产品厚度` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
            `单位` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
            `数量` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
            `单价` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `总价` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `潮湿` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `加强` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `实际报价` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            `产品描述` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
            PRIMARY KEY (`Index`) USING BTREE
            )
            COLLATE='utf8_unicode_ci'
            ENGINE=InnoDB
            AUTO_INCREMENT=1
            ;
        """%(id)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error new1")
        db.rollback()
    for dic in dicList:
        ls = [(k,dic[k]) for k in dic if dic[k] is not None]
        sql = 'insert `%s` (' %id + ','.join(i[0] for i in ls)+') values ('+','.join('%r' %i[1] for i in ls)+')'
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            print("更新草稿订单表单时，数据库存储出错！")
            db.rollback()
    db.close()

def SaveMeterialTodayPriceInDB(log,whichDB,dicList):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return []
    cursor = db.cursor()
    sql ="SELECT `市价更新日期` FROM `原材料单价表` ORDER BY `Index` DESC LIMIT 1"
    cursor.execute(sql)
    Date = cursor.fetchone()[0]
    if Date == str(datetime.date.today()):
        sql = """DELETE from `原材料单价表` where `市价更新日期`='%s' """ % (Date)
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            print("error new2")
            db.rollback()
    id = "原材料单价表"
    for dic in dicList:
        dic["市价更新日期"]=str(datetime.date.today())
        ls = [(k,dic[k]) for k in dic if dic[k] is not None]
        sql = 'insert `%s` (' %id + ','.join(i[0] for i in ls)+') values ('+','.join('%r' %i[1] for i in ls)+')'
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            print("error new2")
            db.rollback()
    db.close()



def GetExchagneRateInDB(log,whichDB,Date):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return None
    cursor = db.cursor()
    sql ="SELECT `汇率` FROM `美元汇率表` where `日期`='%s'"%(Date)
    # sql="select * from `原材料单价表` where `市价更新日期`='%s'"%(Date)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result != None:
        result=result[0]
    db.close()
    return result

def GetMeterialPrice(log,whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return []
    cursor = db.cursor()
    sql ="SELECT `市价更新日期` FROM `原材料单价表` ORDER BY `Index` DESC LIMIT 1"
    cursor.execute(sql)
    Date = cursor.fetchone()[0]
    sql="select * from `原材料单价表` where `市价更新日期`='%s'"%(Date)
    cursor.execute(sql)
    result = cursor.fetchall()
    column = [index[0] for index in cursor.description]
    data_dict = [dict(zip(column,row)) for row in result]
    db.close()
    return data_dict

def GetDraftComponentInfoByID(log, whichDB, id,type):
    id = int(id)
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderCheckDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return []
    cursor = db.cursor()
    sql = "select table_name from information_schema.tables where table_schema='%s'"%orderCheckDBName[whichDB]
    cursor.execute(sql)
    temp = cursor.fetchall()
    result=[]
    for i in temp:
        result.append(i[0])
    if str(id) not in result:
        sql = """CREATE TABLE `%s` (
                `Index` INT(11) NOT NULL AUTO_INCREMENT,
                `类别` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
                `产品名称` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
                `产品型号` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
                `产品表面材料` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
                `产品长度` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
                `产品宽度` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
                `产品厚度` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
                `单位` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
                `数量` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
                `单价` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
                `总价` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
                `潮湿` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
                `加强` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
                `实际报价` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
                `产品描述` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
                PRIMARY KEY (`Index`) USING BTREE
                )
                COLLATE='utf8_unicode_ci'
                ENGINE=InnoDB
                AUTO_INCREMENT=2
                ;
            """%(id)
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            print("error new3")
            db.rollback()
    sql="select * from `%s` where `类别`='%s'"%(id,type)
    cursor.execute(sql)
    result = cursor.fetchall()
    column = [index[0] for index in cursor.description]
    data_dict = [dict(zip(column,row)) for row in result]
    db.close()
    return data_dict

def GetQuotationDateAndExchangeDateFromDB(log,whichDB,id):
    id = int(id)
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "select `报价参考日期`,`汇率参考日期`  from `订单信息` where `Index`=%s" % id
    cursor.execute(sql)
    record=cursor.fetchone()
    db.close()
    return record[0],record[1]

def GetTechCheckStateByID(log,whichDB,id):
    id = int(id)
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "select `设计审核状态`  from `订单信息` where `Index`=%s" % id
    cursor.execute(sql)
    record=cursor.fetchone()
    db.close()
    return record[0]

def GetTechDrawingDataByID(log,whichDB,id):
    id = int(id)
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    # sql = "UPDATE 系统参数 SET `启动纵切最小板材数`='%s', `任务单每页行数`='%s', `墙角板型号列表`='%s' " %(propertyDic["启动纵切最小板材数"],propertyDic["任务单每页行数"],json.dumps(propertyDic["墙角板型号列表"]))
    # sql = "INSERT INTO `订单信息` (`订单名称`,`客户原始技术图纸名`,`客户原始技术图纸`) VALUES ('%s', '%s', %s)"%(propertyDic["1.订单名称"], json.dumps(propertyDic["1.图纸文件"],ensure_ascii=False), MySQLdb.Binary(img))
    # sql = "INSERT INTO `订单信息` (`订单名称`,`客户原始技术图纸名`,`图`) VALUES ('%s', '%s', '%s')"%(propertyDic["1.订单名称"], json.dumps(propertyDic["1.图纸文件"],ensure_ascii=False), data)
    # sql = """INSERT INTO `订单信息` (`图`) VALUES (%s)""" %(img)

    # sql = "select `图0`  from `订单信息` where `Index`=%s" % (id)
    # cursor.execute(sql)
    # record=cursor.fetchone()
    # image = base64.b64decode(record[0])  # 解码

    temp =""
    sql = "select `技术图纸`  from `订单技术图纸信息` where `订单编号`=%s" % (id)
    cursor.execute(sql)
    record=cursor.fetchone()
    temp=record[0]
    image = base64.b64decode(temp)  # 解码
    db.close()
    return image

def GetPriceDateListFromDB(log,whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "select `定价日期`  from `产品报价表单`"
    cursor.execute(sql)
    record = cursor.fetchall()
    temp =[]
    for i in record:
        temp.append(i[0])
    db.close()
    record = list(set(temp))
    return record

def GetPriceDicFromDB(log, whichDB, date):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % packageDBName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % packageDBName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql="select * from `产品报价表单` where `定价日期`='%s'"%(date)
    cursor.execute(sql)
    result = cursor.fetchall()
    column = [index[0] for index in cursor.description]
    data_dict = [dict(zip(column,row)) for row in result]
    db.close()
    return data_dict
