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
        self.DB_NAME = 'Vaidhyanathan_IPL'
        self.mydb = self.handshake()
        self.cursor = self.mydb.cursor(buffered=True,dictionary=True) 
        self.create_from_create_database()
        self.TABLES,self.QUERIES = Query()
        self.update_tables()
        self.cursor.execute('SHOW TABLES')
        self.loaddata('ipl_venue.csv','venue')
        self.loaddata('ipl_matches.csv','matches')
        self.loaddata('ipl_ball_by_ball.csv','ball')
    def get_tables(self,tables):
        self.TABLES =tables
    def create_database(self):
            try:
                self.cursor.execute(
                    "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.DB_NAME))
            except mysql.connector.Error as err:
                print("Failed creating database: {}".format(err))
    def create_from_create_database(self):
        print("Trying to create DB ",self.DB_NAME)
        try:
            self.cursor.execute("USE {}".format(self.DB_NAME))
            print('Using ',self.DB_NAME, ' Database')
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(self.DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database()
                print("Database {} created successfully.".format(self.DB_NAME))
                self.mydb.database = self.DB_NAME
            else:
                print(err)
    def handshake(self):
        user = input('Enter your user name for your MySQL-server:  ')
        pwd = input('Enter your password for your MySQL-server:  ')
        mydb = mysql.connector.connect(host='localhost',user=user,password=pwd,client_flags=[ClientFlag.LOCAL_FILES],allow_local_infile = True)
        return mydb
    def update_tables(self):
        for table_name in self.TABLES:
            table_description = self.TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                self.cursor.execute(table_description)
                print('Table {} created'.format(table_name))
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print(table_name, " already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
        self.cursor.execute('SHOW TABLES')
        print('Verify all tables are created below')
        print(self.cursor.fetchall())
        self.cursor.reset()
    def loaddata(self,csvfile,tablename):
        sqlLoadData = """load data local infile '{}' into table {}
                         FIELDS TERMINATED BY ','
                         ENCLOSED BY '"' LINES 
                         TERMINATED BY '\n' 
                         IGNORE 1 LINES;""".format(csvfile,tablename)
        self.cursor.execute('SET GLOBAL local_infile=1;')
        self.cursor.execute(sqlLoadData)
        self.mydb.commit()
    def query1(self):
        self.cursor.execute(self.QUERIES['Query1'])
        pp = pprint.PrettyPrinter(indent=3)
        pp.pprint(self.cursor.fetchall())
    def query2(self):
        self.cursor.execute(self.QUERIES['Query2'])
        t= self.cursor.fetchall()
        pp = pprint.PrettyPrinter(indent=3)
        pp.pprint(t)
d = database()