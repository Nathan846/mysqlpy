# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import mysql.connector
from mysql.connector import errorcode
from queries import Query
from mysql.connector.constants import ClientFlag
import pprint
class database:
    def __init__(self):
        self.mydb = self.handshake()
        self.cursor = self.mydb.cursor(buffered=True,dictionary=True)
        self.cursor.execute('USE employees;')
    def handshake(self):
        user = input('Enter your user name for your MySQL-server:  ')
        pwd = input('Enter your password for your MySQL-server:  ')
        mydb = mysql.connector.connect(host='localhost',user=user,password=pwd,client_flags=[ClientFlag.LOCAL_FILES],allow_local_infile = True)
        return mydb
    def query1(self,q1):
        self.cursor.execute(q1)
        pp = pprint.PrettyPrinter(indent=3)
        pp.pprint(self.cursor.fetchall())
    def query2(self,q2):
        self.cursor.execute(q2)
        t= self.cursor.fetchall()
        pp = pprint.PrettyPrinter(indent=3)
        pp.pprint(t)
d = database()
d.query1(Query['Query1'])
d.query2(Query['Query2'])
