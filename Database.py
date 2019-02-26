#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sqlite3

class Database():

    db_path = "./purogconfig.db"
    def __init__(self):
        self.setupConn()

    def setupConn(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except():
            print("数据库连接创建异常！")

    def closeConn(self):
        try:
            self.cursor.close()
            self.conn.close()
        except():
            print("数据库连接关闭异常！")

    # 从SQLite文件中读取数据
    def readDB(self, sql):
        try:
            self.conn.row_factory = sqlite3.Row
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except():
            print("数据库读取异常！")
            return None

    # 写数据库
    def executeDB(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except():
            print("数据库执行错误！")

