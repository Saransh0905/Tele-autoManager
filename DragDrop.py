from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ListBox2(QListWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setDragEnabled(True)
    
    def startDrag(self, event):
        item = self.currentItem()
        itemText = item.text()
        mimeData = QMimeData()
        mimeData.setText(itemText)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.exec_(Qt.MoveAction)
    
class ListBox(QListWidget):
    def __init__(self, parent,limit =1):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.itemLimit = limit
        self.currSize = 0
        self.setMinimumHeight(100)
    def mimeTypes(self):
        mimeTypes = super().mimeTypes()
        mimeTypes.append('text/plain')
        return mimeTypes
 
    def dropMimeData(self, index, data, action):
        if data.hasText():
            listItem = ListItem(self,data.text())
            if self.currSize<self.itemLimit:
                self.setItemWidget(listItem,listItem.widget)
                self.currSize+=1
                
            else:
                self.takeItem(self.currSize)
                print("List is Full")
            return True
        else:
            return super().dropMimeData(index, data, action)
 
class ListItem(QListWidgetItem):
    def __init__(self,parent,text):
        super().__init__(parent)
        self.parent = parent
        self.widget = QWidget()
        self.textLabel = QLabel(text)
        self.textLabel.setStyleSheet("background-color: #6b6b6b;color:#ffffff")  #backgroud color and text color for items in list
        delButton = QPushButton('X')
        delButton.setStyleSheet("color:#ba1a1a")
        delButton.setMaximumWidth(50)
        delButton.clicked.connect(lambda: self.onClick())
        self.setSizeHint(QSize(10,50))
        layout = QHBoxLayout()
        layout.addWidget(self.textLabel)
        layout.addWidget(delButton)
        # layout.addStretch()
        layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.widget.setLayout(layout)
    def onClick(self):
        ListBox.takeItem(self.parent,self.parent.currentRow())
        self.parent.currSize-=1
