'''
Created on 07.01.2014

@author: pavel
'''
from PySide import QtCore, QtGui

class Ui_zavNumForm(object):
    def setupUi(self, zavNumForm):
        zavNumForm.setObjectName("zavNumForm")
        zavNumForm.resize(300, 300)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(zavNumForm.sizePolicy().hasHeightForWidth())
        zavNumForm.setSizePolicy(sizePolicy)
        zavNumForm.setMinimumSize(QtCore.QSize(300, 300))
        zavNumForm.setMaximumSize(QtCore.QSize(300, 300))
        self.plainTextEdit = QtGui.QPlainTextEdit(zavNumForm)
        self.plainTextEdit.setGeometry(QtCore.QRect(1, 1, 298, 250))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        self.plainTextEdit.setMinimumSize(QtCore.QSize(298, 250))
        self.plainTextEdit.setStyleSheet("background-color: rgb(246, 244, 242);")
        self.plainTextEdit.setFrameShape(QtGui.QFrame.Box)
        self.plainTextEdit.setFrameShadow(QtGui.QFrame.Plain)
        self.plainTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.buttonBox = QtGui.QDialogButtonBox(zavNumForm)
        self.buttonBox.setGeometry(QtCore.QRect(105, 265, 90, 30))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(zavNumForm)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("clicked(QAbstractButton*)"), zavNumForm.close)
        QtCore.QMetaObject.connectSlotsByName(zavNumForm)

    def retranslateUi(self, zavNumForm):
        zavNumForm.setWindowTitle(QtGui.QApplication.translate("zavNumForm", "Список заводских номеров", None, QtGui.QApplication.UnicodeUTF8))