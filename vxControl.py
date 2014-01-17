# -*- coding: utf-8 -*-
'''
Created on 29.12.2013

@author: pavel
'''
import sys
import os
import re
from PySide import QtGui, QtCore
from vkForm import Ui_vkForm
from zavNumForm import Ui_zavNumForm
from printVKForm import printVKForm
import configparser
from VkDB import *

class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return len(self.mylist[0])
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None
    def sort(self, col, order):
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        if order == QtCore.Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))

class ComboDelegate(QtGui.QItemDelegate):
    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)
    def createEditor(self, parent, option, index):
        editor = QtGui.QDateTimeEdit(parent)
        editor.setDisplayFormat('dd.MM.yyyy')
        editor.setCalendarPopup(True)
        editor.setDate(QtCore.QDate.currentDate())
        return editor
    '''    combo = QtGui.QComboBox(parent)
        li = []
        li.append("Zero")
        li.append("One")
        li.append("Two")
        li.append("Three")
        li.append("Four")
        li.append("Five")
        combo.addItems(li)
        self.connect(combo, QtCore.SIGNAL("currentIndexChanged(int)"), self, QtCore.SLOT("currentIndexChanged()"))
        return combo
    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setCurrentIndex(int(index.model().data(index)))
        editor.blockSignals(False)
    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentIndex())
    @QtCore.Slot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())'''

class MyDelegate(QtGui.QItemDelegate):
    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)
        self.parent = parent
    def paint(self, painter, option, index):
        painter.save()
        painter.setPen(QtCore.Qt.NoPen)
        if option.state & QtGui.QStyle.State_Selected:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.gray))
        else:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
        painter.drawRect(option.rect)
        if str(index.data()) == 'ИСПРАВЕН' or str(index.data()) == 'ИСПРАВНЫ' or str(index.data()) == 'ИСПРАВНО':
            painter.setPen(QtGui.QPen(QtCore.Qt.green))
        elif str(index.data()) == 'НЕИСПРАВЕН' or str(index.data()) == 'НЕИСПРАВНЫ' or str(index.data()) == 'НЕИСПРАВНО':
            painter.setPen(QtGui.QPen(QtCore.Qt.red))
        else:
            painter.setPen(QtGui.QPen(QtCore.Qt.black))
        painter.drawText(option.rect, QtCore.Qt.AlignCenter, str(index.data()))
        painter.restore()

class MyZavNumForm(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MyZavNumForm, self).__init__(parent)
        self.ui = Ui_zavNumForm()
        self.ui.setupUi(self)
    def setZavNums(self, texts):
        for txt in texts:
            self.ui.plainTextEdit.appendPlainText(str(txt))        

class MyvkForm(QtGui.QWidget):
    def makeHTMLPrint(self, toPrint = False):
        QtGui.QApplication.processEvents()
        myprt = printVKForm()
        myprt.printvkf(str(self.ui.naimIzdel_cB.currentText()), 
                       str(self.ui.model_cB.currentText()), 
                       str(self.ui.firma_cB.currentText()), 
                       self.strs, 
                       str(self.ui.rezult_cB.currentText()), 
                       str(self.ui.operator_cB.currentText()))
    def deleteItemSelected(self):
        if len(self.strs) == 0:
            self.haveZN = False
            self.ui.clear_pB.setEnabled(False)
        else:
            self.strs.pop(self.ui.zavNumber_lV.currentIndex().row())
            self.model1.setStringList(self.strs)
            self.ui.zavNumber_lV.setModel(self.model1)
    def on_zavNumber_lE_returnPressed(self):
        if len(self.ui.zavNumber_lE.text()) > 0:
            self.ui.print_pB.setEnabled(True)
            self.ui.clear_pB.setEnabled(True)
            self.haveZN = True
            if len(self.strs) < 40:
                self.strs.append(self.ui.zavNumber_lE.text())
                self.model1.setStringList(self.strs)
                self.ui.zavNumber_lV.setModel(self.model1)
                self.ui.zavNumber_lE.clear()
                self.ui.zavNumber_lV.scrollToBottom()
            else:
                QtGui.QMessageBox.warning(self, "Предупреждение", "Исчерпан лимит вместимости номеров", QtGui.QMessageBox.Ok)
                self.ui.zavNumber_lE.clear()
    def on_print_pB_clicked(self):
        if self.haveZN:
            self.ui.print_pB.setEnabled(False)
            if self.mydbs.connectToDB():
                if self.changeRecordFlag:
                    curlstRecord = []
                    curlstRecord.append(str(self.ui.firma_cB.currentText()))
                    curlstRecord.append(str(self.ui.dateEdit.text()))
                    curlstRecord.append(str(self.ui.naimIzdel_cB.currentText()))
                    curlstRecord.append(str(self.ui.model_cB.currentText()))
                    curlstRecord.append(str(self.ui.rezult_cB.currentText()))
                    curlstRecord.append(str(self.ui.operator_cB.currentText()))
                    if self.mydbs.changeRecord(curlstRecord, self.strs, self.numOfRecord):
                        self.ui.print_pB.setText('Печать формы')
                        self.changeRecordFlag = False
                    else:
                        print("Error")
                else:
                    if self.mydbs.addToEndDB(str(self.ui.firma_cB.currentText()), 
                                             str(self.ui.dateEdit.text()), 
                                             str(self.ui.naimIzdel_cB.currentText()), 
                                             str(self.ui.model_cB.currentText()), 
                                             str(self.ui.rezult_cB.currentText()), 
                                             str(self.ui.operator_cB.currentText())):
                        if self.mydbs.addToEndDBB(self.strs):
                            self.makeHTMLPrint(True)
                        self.ui.repeate_pB.setEnabled(True)
                self.ui.print_pB.setEnabled(True)
                self.mydbs.closeDB()
                self.loadTable()
        else:
            QtGui.QMessageBox.critical(self, 'Ошибка', 'Список заводских номеров пуст')
    def on_repeate_pB_clicked(self):
        self.ui.repeate_pB.setEnabled(False)
        self.makeHTMLPrint(True)
        self.ui.repeate_pB.setEnabled(True)
    def on_clear_pB_clicked(self):
        self.ui.zavNumber_lE.clear()
        self.strs.clear()
        self.model1.setStringList(self.strs)
        self.ui.zavNumber_lV.setModel(self.model1)
        self.ui.clear_pB.setEnabled(False)
        self.ui.print_pB.setEnabled(False)
    def bd_tV_clicked(self, index):
        self.rowIDs.clear()
        self.rowIDs.append(index.row())
        self.rowIDs.append((self.ui.bd_tV.model().index(index.row(), 1).data()))
    def loadTable(self):
        if self.mydbs.connectToDB():
            self.curdataList.clear()
            self.curdataList = self.mydbs.getAllList('provdev')
            self.mydbs.closeDB()
            if self.curdataList != None:
                self.mymodel = MyTableModel(self, self.curdataList, self.curheader)
                self.ui.bd_tV.setModel(self.mymodel)
                self.ui.bd_tV.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
                self.ui.bd_tV.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
                self.ui.bd_tV.resizeColumnsToContents()
                self.ui.bd_tV.resizeRowsToContents()
    def on_filter_cB_currentIndexChanged(self, index):
        if index == 0:
            self.loadTable()
            self.filterList.clear()
            self.ui.lineEdit.clear()
            self.ui.lineEdit.setEnabled(False)
            return
        elif index > 0 and index < (self.ui.filter_cB.model().rowCount() - 1):
            self.ui.lineEdit.setEnabled(True)
            self.filterList.clear()
            self.ui.lineEdit.setFocus()
            for row in range(0, self.ui.bd_tV.model().rowCount(self.ui.bd_tV.rootIndex())):
                if self.filterList.count(str(self.ui.bd_tV.model().index(row, index-1).data())) == 0:
                    self.filterList.append(str(self.ui.bd_tV.model().index(row, index-1).data()))
            return
    def on_lineEdit_textEdited(self, text):
        self.regexpfilterList.clear()
        if len(self.ui.lineEdit.text()) > 0:
            for item in self.filterList:
                curpar = re.findall("([\\w\\.]*" + text + "+[\\w\\.]*)", 
                                    item, 
                                    re.UNICODE | re.IGNORECASE)
                if len(curpar) > 0:
                    self.regexpfilterList.append(item)
            if len(self.regexpfilterList) > 0:
                self.model1.setStringList(self.regexpfilterList)
                self.ui.filter_lV.setVisible(True)
            else:
                self.ui.filter_lV.setVisible(False)
    def  keyPressEvent(self, event):
        cursel = -1
        if self.ui.lineEdit.isActiveWindow() and self.ui.filter_lV.model().rowCount() > 0:
            if event.key() == QtCore.Qt.Key_Down:
                for i in range(0, self.ui.filter_lV.model().rowCount()):
                    if self.ui.filter_lV.selectionModel().isSelected(self.ui.filter_lV.model().index(i,0)):
                        cursel = i
                if cursel >= 0 and cursel < (self.ui.filter_lV.model().rowCount() - 1):
                    self.ui.filter_lV.selectionModel().select(self.ui.filter_lV.model().index(cursel+1,0), 
                                                              QtGui.QItemSelectionModel.SelectCurrent)
                else:
                    self.ui.filter_lV.selectionModel().select(self.ui.filter_lV.model().index(0,0),
                                                              QtGui.QItemSelectionModel.SelectCurrent)
            if event.key() == QtCore.Qt.Key_Up:
                for i in range(0, self.ui.filter_lV.model().rowCount()):
                    if self.ui.filter_lV.selectionModel().isSelected(self.ui.filter_lV.model().index(i,0)):
                        cursel = i
                if cursel > 0:
                    self.ui.filter_lV.selectionModel().select(self.ui.filter_lV.model().index(cursel-1,0), 
                                                              QtGui.QItemSelectionModel.SelectCurrent)
                else:
                    self.ui.filter_lV.selectionModel().select(self.ui.filter_lV.model().index((self.ui.filter_lV.model().rowCount() - 1),0),
                                                              QtGui.QItemSelectionModel.SelectCurrent)
            if event.key() == QtCore.Qt.Key_Return and len(self.ui.lineEdit.text()) > 0:
                self.ui.filter_lV.setVisible(False)
                for i in range(0, self.ui.filter_lV.model().rowCount()):
                    if self.ui.filter_lV.selectionModel().isSelected(self.ui.filter_lV.model().index(i,0)):
                        cursel = i
                if cursel > -1:
                    self.ui.lineEdit.setText(str(self.ui.filter_lV.model().index(cursel, 0).data()))
                self.search_trowfilter(self.ui.lineEdit.text())
                self.ui.lineEdit.clear()
            if event.key() == QtCore.Qt.Key_Escape:
                self.ui.filter_lV.setVisible(False)
                self.ui.lineEdit.clear()
        return QtGui.QWidget.keyPressEvent(self, event)
    def search_trowfilter(self, text):
        self.proxyModel = QtGui.QSortFilterProxyModel(self)
        self.proxyModel.setSourceModel(self.mymodel)
        if self.ui.filter_cB.currentIndex() > 0 and self.ui.filter_cB.currentIndex() < (self.ui.filter_cB.model().rowCount() - 1):
            self.proxyModel.setFilterKeyColumn(self.ui.filter_cB.currentIndex() - 1)
        self.proxyModel.setFilterFixedString(text)
        self.ui.bd_tV.setModel(self.proxyModel)
    def on_search_pB_clicked(self):
        if len(self.ui.lineEdit.text()) > 0:
            self.search_trowfilter(self.ui.lineEdit.text())
        else:
            QtGui.QMessageBox.critical(self, 'Ошибка', 'Пустой запрос!')
    def on_filter_lV_doubleclicked(self, index):
        self.ui.lineEdit.setText(str(index.data()))
        self.ui.filter_lV.setVisible(False)
    def changeRecord(self):
        self.ui.firma_cB.setCurrentIndex(self.ui.firma_cB.findText(self.ui.bd_tV.model().index(self.rowIDs[0],0).data()))
        self.ui.naimIzdel_cB.setCurrentIndex(self.ui.naimIzdel_cB.findText(self.ui.bd_tV.model().index(self.rowIDs[0],3).data()))
        self.ui.model_cB.setCurrentIndex(self.ui.model_cB.findText(self.ui.bd_tV.model().index(self.rowIDs[0],4).data()))
        self.ui.rezult_cB.setCurrentIndex(self.ui.rezult_cB.findText(self.ui.bd_tV.model().index(self.rowIDs[0],5).data()))
        self.ui.operator_cB.setCurrentIndex(self.ui.operator_cB.findText(self.ui.bd_tV.model().index(self.rowIDs[0],6).data()))
        self.ui.dateEdit.setDate(QtCore.QDate().fromString(self.ui.bd_tV.model().index(self.rowIDs[0],2).data(), "dd.MM.yy"))
        if self.mydbs.connectToDB():
            self.strs.clear()
            zavNumLst = self.mydbs.getAllList('zavnums')
            for item in zavNumLst:
                if item[0] == self.rowIDs[1]:
                    self.strs.append(str(item[1]))
            self.model1.setStringList(self.strs)
            self.ui.zavNumber_lV.setModel(self.model1)
            self.mydbs.closeDB()
            self.haveZN = True
            self.ui.print_pB.setEnabled(True)
            self.ui.clear_pB.setEnabled(True)
            self.ui.zavNumber_lV.scrollToTop()
            self.ui.print_pB.setText('Правка записи')
            self.changeRecordFlag = True
            self.numOfRecord = self.rowIDs[1]
    def printRecord(self):
        QtGui.QApplication.processEvents()
        lst1 = []
        if self.mydbs.connectToDB():
            zavNumLst = self.mydbs.getAllList('zavnums')
            for item in zavNumLst:
                if item[0] == self.rowIDs[1]:
                    lst1.append(str(item[1]))
            self.mydbs.closeDB()
        myprt = printVKForm()
        myprt.printvkf(str(self.ui.bd_tV.model().index(self.rowIDs[0], 3).data()), 
                       str(self.ui.bd_tV.model().index(self.rowIDs[0], 4).data()), 
                       str(self.ui.bd_tV.model().index(self.rowIDs[0], 0).data()), 
                       lst1, 
                       str(self.ui.bd_tV.model().index(self.rowIDs[0], 5).data()), 
                       str(self.ui.bd_tV.model().index(self.rowIDs[0], 6).data()))
    def deleteRecord(self):
        if QtGui.QMessageBox.question(self, 'Входной контроль', 
                                   'Вы уверены, что хотите удалить данную запись?', 
                                   QtGui.QMessageBox.Yes, 
                                   QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
            if self.mydbs.connectToDB():
                self.mydbs.deleteRecord(self.rowIDs[1])
                self.mydbs.closeDB()
                self.loadTable()
    def viewRecord(self):
        self.myZavNumF = MyZavNumForm()
        zavNumFiltres = []
        if self.mydbs.connectToDB():
            zavNumLst = self.mydbs.getAllList('zavnums')
            for item in zavNumLst:
                if item[0] == self.rowIDs[1]:
                    zavNumFiltres.append(str(item[1]))
            self.myZavNumF.ui.plainTextEdit.clear()
            self.myZavNumF.setZavNums(zavNumFiltres)
            self.mydbs.closeDB()
        self.myZavNumF.setWindowModality(QtCore.Qt.ApplicationModal)
        self.myZavNumF.show()
    def __init__(self, parent=None):
        super(MyvkForm, self).__init__(parent)
        self.changeRecordFlag = False
        self.haveZN = False
        self.flagprint = False
        self.numOfRow = -1
        self.numOfRecord = -1
        self.curdataList = []
        self.strs = []
        self.rowIDs = []
        self.filterList = []
        self.delTableActions = []
        self.regexpfilterList = []
        self.lVmodel = QtGui.QStringListModel()
        self.curheader = ['Производитель', 'ID номер', 'Дата проверки', 'Наименование', 'Модель', 'Рез. проверки', 'ФИО оператора']
        self.mydbs = VkDB()
        self.mydel = MyDelegate(self)
        self.model1 = QtGui.QStringListModel()
        self.ui = Ui_vkForm()
        self.ui.setupUi(self)
        self.setWindowTitle("Входной контроль")
        self.delAction = QtGui.QAction('Удалить', self.ui.zavNumber_lV)
        self.ui.zavNumber_lV.addAction(self.delAction)
        self.ui.zavNumber_lV.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ui.zavNumber_lV.connect(self.delAction, QtCore.SIGNAL('triggered()'), self, QtCore.SLOT('deleteItemSelected()'))
        self.connect(self.ui.zavNumber_lE, QtCore.SIGNAL('returnPressed ()'), self, QtCore.SLOT('on_zavNumber_lE_returnPressed()'))
        self.connect(self.ui.clear_pB, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('on_clear_pB_clicked()'))
        self.connect(self.ui.print_pB, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('on_print_pB_clicked()'))
        self.connect(self.ui.repeate_pB, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('on_repeate_pB_clicked()'))
        self.ui.search_pB.clicked.connect(self.on_search_pB_clicked)
        self.ui.filter_cB.currentIndexChanged.connect(self.on_filter_cB_currentIndexChanged)
        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
        self.ui.bd_tV.horizontalHeader().setClickable(False)
        self.ui.bd_tV.verticalHeader().setClickable(False)
        self.ui.bd_tV.verticalHeader().hide()
        self.ui.bd_tV.viewport().setMouseTracking(True)
        self.setMouseTracking(True)
        self.ui.bd_tV.viewport().installEventFilter(self)
        self.ui.bd_tV.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.bd_tV.pressed.connect(self.bd_tV_clicked)
        self.ui.bd_tV.setItemDelegate(self.mydel)
        self.delTableActions.append(QtGui.QAction('Правка записи', self.ui.bd_tV))
        self.delTableActions.append(QtGui.QAction('Печать записи', self.ui.bd_tV))
        self.delTableActions.append(QtGui.QAction('Список Зав. номеров', self.ui.bd_tV))
        self.delTableActions.append(QtGui.QAction('Удалить', self.ui.bd_tV))
        self.ui.bd_tV.addActions(self.delTableActions)
        self.ui.bd_tV.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ui.bd_tV.connect(self.delTableActions[0], QtCore.SIGNAL('triggered()'), self, QtCore.SLOT('changeRecord()'))
        self.ui.bd_tV.connect(self.delTableActions[1], QtCore.SIGNAL('triggered()'), self, QtCore.SLOT('printRecord()'))
        self.ui.bd_tV.connect(self.delTableActions[2], QtCore.SIGNAL('triggered()'), self, QtCore.SLOT('viewRecord()'))
        self.ui.bd_tV.connect(self.delTableActions[3], QtCore.SIGNAL('triggered()'), self, QtCore.SLOT('deleteRecord()'))
        self.ui.filter_lV.setGeometry(QtCore.QRect(405, 260, 238, 50))
        self.ui.filter_lV.setVisible(False)
        self.ui.filter_lV.setModel(self.model1)
        self.itemsel = QtGui.QItemSelectionModel(self.ui.filter_lV.model())
        self.ui.filter_lV.doubleClicked.connect(self.on_filter_lV_doubleclicked)
        self.ui.lineEdit.textEdited.connect(self.on_lineEdit_textEdited)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        '''self.ui.bd_tV.setItemDelegateForColumn(1, ComboDelegate(self))
        for row in range(0, self.ui.bd_tV.model().rowCount(self)):
            self.ui.bd_tV.openPersistentEditor(self.ui.bd_tV.model().index(row, 1))'''
        if os.path.exists('res.ini'):
            myres = configparser.ConfigParser()
            myres.read('res.ini')
            for key in myres['Name']:
                self.ui.naimIzdel_cB.addItem(str(myres['Name'][key])) 
            for key in myres['Model']:
                self.ui.model_cB.addItem(str(myres['Model'][key]))
            for key in myres['Firma']:
                self.ui.firma_cB.addItem(str(myres['Firma'][key]))
            for key in myres['Operator']:
                self.ui.operator_cB.addItem(str(myres['Operator'][key]))
            self.ui.naimIzdel_cB.setCurrentIndex(-1)
            self.ui.model_cB.setCurrentIndex(-1)
            self.ui.firma_cB.setCurrentIndex(-1)
            self.ui.rezult_cB.setCurrentIndex(-1)
            self.ui.operator_cB.setCurrentIndex(-1)
            if os.path.exists('devicessqlite.db'):
                self.loadTable()
            else:
                QtGui.QMessageBox.critical(self, 
                                           'Ошибка', 
                                           'Не найден файл \'devicessqlite.db\'\nПереустановите приложение или восстановите\nданный файл из резервных источников')
                self.close()
        else:
            QtGui.QMessageBox.critical(self, 
                                       'Ошибка', 
                                       'Не найден файл \'res.ini\'\nПереустановите приложение или восстановите\nданный файл из резервных источников')
            self.close()        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myvkF = MyvkForm()
    myvkF.show()
    sys.exit(app.exec_())