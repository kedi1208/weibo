#!/usr/bin/env python
#coding:utf-8

import sqlite3
import time

dbType = ''
g_timestamp = ''

def get_conn(db_name, dbtype):
    global dbType
    dbType = dbtype
    if dbType=='sqlite':
        conn = sqlite3.connect(db_name)
        set_timestamp()
        return conn
    else:
        return None

def dao_commit(conn):
    global dbType
    if dbType=='sqlite':
        conn.commit()
    else:
        pass

def dao_close(conn):
    global dbType
    if dbType=='sqlite':
        conn.close()
    else:
        pass

def get_timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def set_timestamp():
    global g_timestamp
    g_timestamp = get_timestamp()

def hot_insert(conn, hotdata):
    global g_timestamp
    cur = conn.cursor()
    cur.execute('INSERT INTO WEIBOHOT (topic,rank,hot,timestamp,hottype) VALUES \
        ("{0}", {1}, {2}, "{3}", "{4}" )'.format(hotdata["topic"], int(hotdata["rank"]), int(hotdata["hot"]), g_timestamp, hotdata["hottype"]))



if __name__ == "__main__":
    conn = get_conn('weibohot.db', 'sqlite')
    hotdata = {"topic": "py测试3", "rank": 11, "hot": 333, "hottype": "新"}
    hot_insert(conn, hotdata)
    dao_commit(conn)
    dao_close(conn)