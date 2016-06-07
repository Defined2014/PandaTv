import pymysql

def createcon():
    conn=pymysql.connect(host='localhost',user='root',passwd='FWwdKE4ZuKMvmcZG',db='danmu',port=3306,charset='utf8')
    return conn

def closecon(conn):
    conn.close()

def insertdanmu(conn,context):
    cur=conn.cursor()#获取一个游标
    sql='insert into test (IdName,context,time,level,room,plat) VALUES (\''+context["data"]["from"]["nickName"]+'\',\''+context["data"]["content"]+'\',\''+str(context["time"])+'\',\''+str(context["data"]["from"]["level"])+'\',\''+str(context["data"]["to"]["toroom"])+'\',\''+context["data"]["from"]["__plat"]+'\')'
    #print(sql)
    cur.execute(sql)
    cur.close()#关闭游标