'''
Created on 29.12.2013

@author: pavel
'''
import os
import datetime
import webbrowser
import time

def howlong(f):
    def tmp():
        t = time.time()
        ret = f()
        print("%f" % (time.time() - t))
        return ret
    return tmp

class printVKForm():
    def __init__(self):
        self.dayToday = datetime.date.today().strftime("%d.%m.%Y")
    def printvkf(self, nameI, model, firma, zavNumberList, rezultat, operator):
        self.globStr = b''
        self.allZavNumbers = ''
        try:
            etalonFile = os.open('template.html', os.O_RDONLY)
        except:
            print("Error: Can`t open file \'template.html\'!")
            return
        try:
            if os.path.exists('tmp.html'):
                os.remove('tmp.html')
        except:
            pass
        try:
            targetFile = os.open('tmp.html', os.O_CREAT | os.O_RDWR)
        except:
            print("Error: Can`t create template file!")
            return
        str1 = os.read(etalonFile, 1024)
        while str1:
            self.globStr += str1
            str1 = os.read(etalonFile, 1024)
        self.globStr = self.globStr.decode('utf-8')
        self.globStr = self.globStr.replace("[TDate]", str(self.dayToday))
        self.globStr = self.globStr.replace('[TNameI]', nameI)
        self.globStr = self.globStr.replace('[TModel]', model)
        self.globStr = self.globStr.replace('[TFirma]', firma)
        if len(zavNumberList) < 20:
            self.allZavNumbers = ''
            for item in zavNumberList:
                self.allZavNumbers += (item + '<br>')
            self.globStr = self.globStr.replace('[TZNamber1]', self.allZavNumbers)
            self.globStr = self.globStr.replace('[TZNamber2]', '')
        elif len(zavNumberList) < 40:
            self.allZavNumbers = ''
            for item in zavNumberList[:21]:
                self.allZavNumbers += (item + '<br>')
            self.globStr = self.globStr.replace('[TZNamber1]', self.allZavNumbers)
            self.allZavNumbers = ''
            for item in zavNumberList[21:]:
                self.allZavNumbers += (item + '<br>')
            self.globStr = self.globStr.replace('[TZNamber2]', self.allZavNumbers)
        else:
            print("(printvkf): To many items in list")
            return
        self.globStr = self.globStr.replace('[TRezultat]', rezultat)
        self.globStr = self.globStr.replace('[TOperator]', operator)
        os.write(targetFile, self.globStr.encode())
        os.close(etalonFile)
        os.close(targetFile)
        webbrowser.open_new('tmp.html')
        return