# -*- encoding: utf-8 -*-
import base64
import pymysql as MySQLdb
# import MySQLdb
#impo
def TransformBase64(fileName):
    """
    image -> base64
    :param fileName:
    :return:
    """
    # img_path = "./%s.png" % img_name
    # img_path = "%s" % fileName
    try:
        with open(fileName, 'rb') as file:
            fileData = file.read()
            base64_data = base64.b64encode(fileData)  # 'bytes'型数据
            str_base64_data = base64_data.decode()#str型数据
            return str_base64_data
    except:
        return "erro"

def UpdateInfoImage(kinfe_name):
    data=TransformBase64(kinfe_name)
    if data != "erro":
        # DB = MySQLdb.connect(host="%s" % host_name, user='%s' % user_name, passwd='%s' % passwd_name, db='%s' %DATABASE_NAME[6],charset='utf8')
        DB = MySQLdb.connect(host='127.0.0.1',user="root", passwd="12345678", db="dingzhikeji", charset='utf8')
        cursor = DB.cursor()
        cursor.execute(
            "UPDATE `info_tools` set `info_image`='%s' WHERE `kinfe_name`='%s'" % (data,"TJDZ_1"))
        DB.commit()
        print("success")
    else:
        print("erro2")

def ReadInfoImage(kinfe_name):
    DB = MySQLdb.connect(host='127.0.0.1', user='root', passwd='12345678', db="dingzhikeji", charset='utf8')
    cursor = DB.cursor()
    cursor.execute("select `info_image`  from `info_tools` where `kinfe_name`='%s'" %(kinfe_name))
    record=cursor.fetchone()
    return record

def InsertInfoIntoDB(filename):
    data = TransformBase64(filename)
    if data != 'erro':
        try:
            db = MySQLdb.connect(host='192.168.1.108', user="slyb", passwd="Freescalejm60", db="test", charset='utf8')
        except:
            print("db_error!")
        cursor = db.cursor()
        sql = "INSERT INTO `测试表` (`图纸1`) VALUES ('%s')" %(data)
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            print("error Insert")
            db.rollback()
        db.close()


def ShowImage(kinfe_name):
    """
    base64 -> image
    :return:
    """
    kinfe_name=ReadInfoImage(kinfe_name)
    with open('TJDZ_1.jpg', 'wb') as file:
        image = base64.b64decode(kinfe_name[0])  # 解码
        file.write(image)

if __name__ == '__main__':
    InsertInfoIntoDB("QMS-for-XA-2019-报价模板.pdf")
    # info=ShowImage("TJDZ_1")
    # info=UpdateInfoImage("TJDZ_1")