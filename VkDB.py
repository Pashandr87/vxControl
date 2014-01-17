'''
Created on 03.01.2014

@author: pavel
'''

import _sqlite3

class VkDB():
    def __init__(self):
        self.myvkdb = None
    def connectToDB(self, filename = 'devicessqlite.db'):
        try:
            self.myvkdb = _sqlite3.connect(filename)
            self.cur = self.myvkdb.cursor() 
            return True
        except _sqlite3.Error as e:
            print("Error in connectToDB: ", e.args[0])
            return False
    def closeDB(self):
        if self.myvkdb:
            self.myvkdb.close()
    def getLastId(self):
        try:
            self.cur.execute("SELECT * FROM provdev ORDER BY Dev_ID")
            data = self.cur.fetchall()
            data.reverse()
            return int(data[0][1])
        except _sqlite3.Error as e:
            print("Error in getLastId:", e.args[0])
            return None
    def addToEndDB(self, proizvod='', data='', devName='', devModel='', result='', operatorName=''):
        lastid = self.getLastId()
        if lastid == None: return False
        values = ((proizvod, str(lastid + 1), data, devName, devModel, result, operatorName),)
        try:
            self.cur = self.myvkdb.cursor()
            self.cur.executemany("INSERT INTO provdev(Firma, Dev_ID, Data_Prov, Dev_Name, Dev_Model, Result_Prov, Name_Operator) VALUES (?, ?, ?, ?, ?, ?, ?);", values)
            self.myvkdb.commit()
            return True
        except _sqlite3.Error as e:
            print("Error in addToEndDB:", e.args[0])
            return False
    def addToEndDBB(self, listZavNumbers):
        lastid = self.getLastId()
        if lastid == None: return False
        try:
            self.cur = self.myvkdb.cursor()
            for item in listZavNumbers:
                self.cur.execute("INSERT INTO zavnums(Dev_ID, Zav_Number) VALUES(?, ?);", (str(lastid), str(item)))
            self.myvkdb.commit()
            return True
        except _sqlite3.Error as e:
            print("Error in addToEndDBB:", e.args[0])
            return False
    def changeRecord(self, listRecord, listZavNum, curId = None):
        try:
            self.cur = self.myvkdb.cursor()
            self.cur.execute("UPDATE provdev SET Firma=?, Data_Prov=?, Dev_Name=?, Dev_Model=?, Result_Prov=?, Name_Operator=? WHERE Dev_ID=?",
                             (listRecord[0], listRecord[1], listRecord[2], listRecord[3], listRecord[4], listRecord[5], str(curId)))
            self.myvkdb.commit()
            self.cur.execute("DELETE FROM zavnums WHERE Dev_ID=:Dev_ID", {"Dev_ID": str(curId)})
            self.myvkdb.commit()
            for item in listZavNum:
                self.cur.execute("INSERT INTO zavnums(Dev_ID, Zav_Number) VALUES(?, ?);", (str(curId), str(item)))
            self.myvkdb.commit()
            return True
        except _sqlite3.Error as e:
            print("Error in changeRecord:", e.args[0])
            return False
    def deleteRecord(self, curId = None):
        if curId != None:
            try:
                self.cur = self.myvkdb.cursor()
                self.cur.execute('DELETE FROM provdev WHERE Dev_ID=:Dev_ID', {"Dev_ID": str(curId)})
                self.myvkdb.commit()
                self.cur.execute("DELETE FROM zavnums WHERE Dev_ID=:Dev_ID", {"Dev_ID": str(curId)})
                self.myvkdb.commit()
                return True
            except _sqlite3.Error as e:
                print("Error in deleteRecord:", e.args[0])
                return False
    def getAllList(self, tableName=None):
        rows = []
        if tableName != None:
            try:
                self.cur = self.myvkdb.cursor()
                self.cur.execute("SELECT * FROM " + str(tableName))
                rows = self.cur.fetchall()
                return rows
            except _sqlite3.Error as e:
                print("Error in getAllList:", e.args[0])
                return None
        return None     