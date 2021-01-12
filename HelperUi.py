import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json
import traceback

class DialogBox(QDialog):
    def __init__(self,parent = None):
        super(DialogBox, self).__init__(parent)
        self.ui = Dialog_UI()
        self.ui.setupUi(self)
class Dialog_UI(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.Dialog = Dialog
        with open("data.json") as f:
            data = json.load(f)
            self.st = data["Path"]
        import os
        stream = os.popen('wmic os get OSArchitecture')
        output = stream.readlines()
        self.systemDet = output[2][:7]
        self.layout = QVBoxLayout(Dialog)
        self.label = QLabel("Your System is "+self.systemDet+"\nInstall "+self.systemDet+" version of the software\nChange the path if system install is in different Path\n\nPATH:")
        self.lineEdit = QLineEdit(self.st,Dialog)
        self.editButton = QPushButton("Edit",parent=Dialog)
        self.lineEdit.setReadOnly(True)
        self.editButton.clicked.connect(self.changeEdit)
        self.saveButton = QPushButton("Save",Dialog)
        self.saveButton.clicked.connect(self.saveFunc)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.editButton)
        self.layout.addWidget(self.saveButton)

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "System Details"))
        Dialog.show()
    def changeEdit(self):
        self.lineEdit.setReadOnly(False)
    def saveFunc(self):
        path = self.lineEdit.text()
        with open("data.json","r") as f:
            data = json.load(f)
            data["Path"] = path
        
        with open("data.json", "w") as outfile: 
            json.dump(data, outfile)
        self.Dialog.close()

if __name__ == '__main__':
    print("Yes!!")