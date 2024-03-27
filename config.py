# coding=utf-8

import sqlite3,configparser
from datetime import datetime

config_file = 'pnote.ini'

# 其他------------------------------------------------------------------------------
# 保存config
def save_config(section, key, value):
    config = configparser.ConfigParser()  # 创建ConfigParser对象
    config.read(config_file)  # 读取.ini文件
    config.set(section, key, value)  # 修改参数值
    with open(config_file, 'w') as f:  # 写入修改后的.ini文件
        config.write(f)

# 查询config
def get_config(section, key):
    config = configparser.ConfigParser()  # 创建ConfigParser对象
    config.read(config_file)  # 读取.ini文件
    current = config.get(section, key)
    return current

# 数据库查询
def selectOne(sql, info=[]):
    try:
        # 连接Sqlite数据库
        db = sqlite3.connect(get_config('db', 'pnotedb'))
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 使用execute()方法执行sql语句
        cursor.execute(sql, info)
        # 使用fetchone()方法获取所有数据
        results = cursor.fetchall()
        return results
    except Exception as err:
        return '事务处理失败'
    else:
        return "事务处理成功"
    # 关闭数据库
    finally:
        db.close()

# 数据库更新
def addUpdateDel(sql, info=[]):
    try:
        # 连接Sqlite数据库
        db = sqlite3.connect(get_config('db', 'pnotedb'))
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 使用execute()方法执行sql语句
        cursor.execute(sql, info)
    except Exception as err:
        db.rollback()
        return '事务处理失败'
    else:
        db.commit()
        return "事务处理成功"
    # 关闭数据库
    finally:
        db.close()

# 查子目录
def queryItem(pid):
	result = selectOne("SELECT id,iid,name FROM pnotes WHERE pid=?",(pid,))
	return result

# 查内容
def queryContent(id):
	result = selectOne("SELECT content FROM pnotes WHERE id=?",(id,))
	return result

# 更新内容
def updateContent(content,id):
	result = addUpdateDel("update pnotes set content=? where id=?",(content,id,))
	return result

# 插入图片
def insertImageInfo(tid, imageid, imgaddress, imgdata):
    result = addUpdateDel("INSERT INTO pimages (tid, imageid, imgaddress, imgdata, create_date) VALUES (?, ?, ?, ?, ?)",(tid, imageid, imgaddress, imgdata, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
    return result

# 查询图片
def queryImageInfo(tid):
    result = selectOne("select imageid, imgaddress, imgdata from pimages where tid=?",(tid,))
    return result

# 删除旧图片信息
def deleteImageInfo(tid):
    result = addUpdateDel("delete from pimages where tid=?",(tid,))
    return result

# 最大iid
def queryMaxIid():
    result = selectOne("select max(iid) from pnotes")
    return result

# 添加子项
def addItem(pid, iid, name):
    result = addUpdateDel("INSERT INTO pnotes (pid, iid, name, create_date) VALUES (?, ?, ?, ?)",(pid, iid, name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
    return result

# 删除当前项
def deleteItem(id):
    result1 = addUpdateDel("delete from pnotes where id=?",(id,))
    result2 = addUpdateDel("delete from pimages where tid=?",(id,))
    if '事务处理失败' in (result1,result2):
        result = '事务处理失败'
    else:
        result = "事务处理成功"
    return result

# 重命名当前项
def renameItem(name,id):
    result = addUpdateDel("update pnotes set name=? where id=?",(name,id,))
    return result

# 总条目
def queryItems():
    result = selectOne("select count(1) from pnotes")[0][0]
    return result

# 新建数据库
def createNewDb():
    create_pnotes = '''CREATE TABLE "pnotes" (
        "id" INTEGER NOT NULL,
        "pid" INTEGER NOT NULL,
        "iid" INTEGER NOT NULL,
        "name" VARCHAR(50) NOT NULL,
        "content" TEXT NULL,
        "create_date" VARCHAR(50) NOT NULL,
        PRIMARY KEY ("id")
    );
    '''
    create_pimages = '''CREATE TABLE "pimages" (
        "id" INTEGER NOT NULL,
        "tid" INTEGER NOT NULL,
        "imageid" VARCHAR(50) NULL,
        "imgaddress" VARCHAR(50) NULL,
        "imgdata" BLOB NULL,
        "create_date" VARCHAR(50) NOT NULL,
        PRIMARY KEY ("id")
    );
    '''
    result1 = addUpdateDel(create_pnotes)
    result2 = addUpdateDel(create_pimages)
    if '事务处理失败' in (result1,result2):
        result = '事务处理失败'
    else:
        result = "事务处理成功"
    return result
    return result