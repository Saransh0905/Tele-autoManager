import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from DragDrop import ListBox,ListItem,ListBox2
from GetAPI import GetAPIInfo
import json
from sys import stderr, stdout
from MainApp import startMain,disconnect
import traceback
from HelperUi import DialogBox
from Activate import userpassGetter
class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
class APIThread(QRunnable):
    def __init__(self):
        super(APIThread, self).__init__()
        self.signals = WorkerSignals()
    @pyqtSlot()
    def run(self):
        try:
            api_id, api_hash = GetAPIInfo()
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(api_id+" "+api_hash)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
def showdialog():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Email: <a href='xxx@gmail.com'>xxx@gmail.com</a> <br> Link:<a href='http://google.com/'>Google</a> <br> Contact: +11111111111")
    msg.setInformativeText("Telegram API Bot")

    msg.setWindowTitle("Contact Details")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
def LinkingA():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Go To: <a href='www.installA.com'>www.installA.com</a> <br>")
    msg.setWindowTitle("Install A")  #Title of Message box
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
def LinkingB():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Go To: <a href='www.installB.com'>www.installB.com</a> <br>")
    msg.setWindowTitle("Install B")  # Title of Message box
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
def mainMessage(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle("Information")  # Title of Message box
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()


class Port(object):
    def __init__(self, view):
        self.view = view
    def flush(self):
        pass
    def write(self, *args):
        if args[0]!="\n":
            # self.view.append(str([*args])) # This line will highlight next line character in console "\n"
            self.view.append(*args)
class InOutWidget(QWidget):
    def __init__(self, parent,heading,limit):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.label = QLabel(heading)
        self.label.setAlignment(Qt.AlignCenter)
        self.lineEdit = QLineEdit(limit)
        self.lineEdit.setMaximumWidth(50)
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
class MainWindow(QMainWindow):
    def __init__(self,parent = None):
        super(QMainWindow, self).__init__(parent)
        # self.showMaximized()
        self.showFullScreen()
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.apiId = ''
        self.apiHash = ''
        f = open('data.json')
        data = json.load(f)
        if data['API ID']!='':
            self.apiId = data['API ID']
            self.apiHash = data['API Hash']
        self.channelsList = data["Channels"]
        self.getChannelProcess = None
        self.activated = False
        self.SetupUI()
        for i in range(12):
            count = 0
            if i%2==0:
                st = 'Input'
            else:
                st = 'Output'
            for k in data[st+str(i//2 +1)]:
                listItem = ListItem(self.listArr[i],k)
                self.listArr[i].setItemWidget(listItem,listItem.widget)
                count+=1
            self.headArr[i].lineEdit.setText(str(count))
            self.changedLimit(self.listArr[i],self.headArr[i].lineEdit)
            self.listArr[i].currSize =  int(self.headArr[i].lineEdit.text())
            
        self.styleSheet = ""
        with open("style.qss") as qss:
            self.styleSheet = qss.read()
        self.setStyleSheet(self.styleSheet)
        self.setWindowTitle("Window Title") #Set window title here.

    def SetupUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.centralLayout)
        self.menuBar = QMenuBar()
        self.menuMenu = self.menuBar.addMenu("Menu")
        self.helpMenu = self.menuBar.addMenu("Help")
        activateAct = QAction('&System Check',self)
        activateAct.triggered.connect(self.ActivateFunc)
        self.menuMenu.addAction(activateAct)

        installAAct = QAction('Install A',self)
        installAAct.triggered.connect(self.InstallAFunc)
        self.menuMenu.addAction(installAAct)
        
        installBAct = QAction('Install B',self)
        installBAct.triggered.connect(self.InstallBFunc)
        self.menuMenu.addAction(installBAct)

        exitAct = QAction('&Exit', self)
        exitAct.triggered.connect(qApp.quit)
        self.menuMenu.addAction(exitAct)

        contactAct = QAction('Contact',self)
        contactAct.triggered.connect(self.ContactFunc)
        self.helpMenu.addAction(contactAct)

        self.horiLayout = QHBoxLayout()
        self.VLayout1 = QVBoxLayout()
        self.VLayout2 = QVBoxLayout()
        self.VLayout3 = QVBoxLayout()
        self.VLayout2Main = QVBoxLayout()
        #Creating 1st Vertical layout
        self.getAPIButton = QPushButton("GET API ID/HASH",self)
        self.getAPIButton.clicked.connect(lambda: self.getAPIFunc())
        self.horiPairLayout = QHBoxLayout()
        self.horiPairLayout.addWidget(self.getAPIButton)
        self.apiIDLabel = QLabel(self.apiId)
        self.apiIDLabel.setAlignment(Qt.AlignCenter)
        self.apiHashLabel = QLabel(self.apiHash)
        self.apiHashLabel.setAlignment(Qt.AlignCenter)
        self.getChannelButton = QPushButton("GET CHANNELS/GROUPS")
        self.getChannelButton.clicked.connect(lambda: self.getChannelFunc())
        self.tempHoriLayout = QHBoxLayout()
        self.numLineEdit = QLineEdit(self)
        self.numSendButton = QPushButton("SEND",self)
        self.numSendButton.clicked.connect(lambda: self.sendFunc(self.numLineEdit))
        self.codeLineEdit = QLineEdit(self)
        self.codeSendButton = QPushButton("Send",self)
        self.codeSendButton.clicked.connect(lambda:self.sendFunc(self.codeLineEdit))
        self.tempHoriLayout.addWidget(self.numLineEdit)
        self.tempHoriLayout.addWidget(self.numSendButton)
        self.tempHoriLayout.addWidget(self.codeLineEdit)
        self.tempHoriLayout.addWidget(self.codeSendButton)
        self.allChannelList = ListBox2(self)
        self.allChannelList.addItems(self.channelsList)
        self.VLayout1.addLayout(self.horiPairLayout)
        self.VLayout1.addWidget(self.apiIDLabel)
        self.VLayout1.addWidget(self.apiHashLabel)
        self.VLayout1.addWidget(self.getChannelButton)
        self.VLayout1.addLayout(self.tempHoriLayout)
        self.VLayout1.addWidget(self.allChannelList)
        #Creating 2nd Vertical layout
        self.inputHeadArr = []
        self.listArr = []
        self.inputListHead1 = InOutWidget(self,"FOR CHANNEL INPUT 1",'1')
        self.inputList1 = ListBox(self)
        self.inputListHead1.lineEdit.textChanged.connect(lambda : self.changedLimit(self.inputList1,self.inputListHead1.lineEdit))
        self.outputListHead1 = InOutWidget(self,"FOR CHANNEL OUTPUT 1",'1')
        self.outputList1 = ListBox(self)
        self.outputListHead1.lineEdit.textChanged.connect(lambda : self.changedLimit(self.outputList1,self.outputListHead1.lineEdit))

        self.inputListHead2 = InOutWidget(self,"FOR CHANNEL INPUT 2",'1')
        self.inputList2 = ListBox(self)
        self.inputListHead2.lineEdit.textChanged.connect(lambda : self.changedLimit(self.inputList2,self.inputListHead2.lineEdit))
        self.outputListHead2 = InOutWidget(self,"FOR CHANNEL OUTPUT 2",'1')
        self.outputList2 = ListBox(self)
        self.outputListHead2.lineEdit.textChanged.connect(lambda : self.changedLimit(self.outputList2,self.outputListHead2.lineEdit))

        self.inputListHead3 = InOutWidget(self,"FOR CHANNEL INPUT 3",'1')
        self.inputList3 = ListBox(self)
        self.inputListHead3.lineEdit.textChanged.connect(lambda : self.changedLimit(self.inputList3,self.inputListHead3.lineEdit))
        self.outputListHead3 = InOutWidget(self,"FOR CHANNEL OUTPUT 3",'1')
        self.outputList3 = ListBox(self)
        self.outputListHead3.lineEdit.textChanged.connect(lambda : self.changedLimit(self.outputList3,self.outputListHead3.lineEdit))

        
        self.inputListHead4 = InOutWidget(self,"FOR CHANNEL INPUT 4",'1')
        self.inputList4 = ListBox(self)
        self.inputListHead4.lineEdit.textChanged.connect(lambda : self.changedLimit(self.inputList4,self.inputListHead4.lineEdit))
        self.outputListHead4 = InOutWidget(self,"FOR CHANNEL OUTPUT 4",'1')
        self.outputList4 = ListBox(self)
        self.outputListHead4.lineEdit.textChanged.connect(lambda : self.changedLimit(self.outputList4,self.outputListHead4.lineEdit))

        self.inputListHead5 = InOutWidget(self,"FOR CHANNEL INPUT 5",'1')
        self.inputList5 = ListBox(self)
        self.inputListHead5.lineEdit.textChanged.connect(lambda : self.changedLimit(self.inputList5,self.inputListHead5.lineEdit))
        self.outputListHead5 = InOutWidget(self,"FOR CHANNEL OUTPUT 5",'1')
        self.outputList5 = ListBox(self)
        self.outputListHead5.lineEdit.textChanged.connect(lambda : self.changedLimit(self.outputList5,self.outputListHead5.lineEdit))


        self.inputListHead6 = InOutWidget(self,"FOR CHANNEL INPUT 6",'1')
        self.inputList6 = ListBox(self)
        self.inputListHead6.lineEdit.textChanged.connect(lambda : self.changedLimit(self.inputList6,self.inputListHead6.lineEdit))
        self.outputListHead6 = InOutWidget(self,"FOR CHANNEL OUTPUT 6",'1')
        self.outputList6 = ListBox(self)
        self.outputListHead6.lineEdit.textChanged.connect(lambda : self.changedLimit(self.outputList6,self.outputListHead6.lineEdit))
        self.listArr = [self.inputList1,self.outputList1,self.inputList2,self.outputList2,self.inputList3,self.outputList3,self.inputList4,self.outputList4,self.inputList5,self.outputList5,self.inputList6,self.outputList6]
        self.headArr = [self.inputListHead1,self.outputListHead1,self.inputListHead2,self.outputListHead2,self.inputListHead3,self.outputListHead3,self.inputListHead4,self.outputListHead4,self.inputListHead5,self.outputListHead5,self.inputListHead6,self.outputListHead6]
        self.VLayout2.addWidget(self.inputListHead1)
        self.VLayout2.addWidget(self.inputList1)
        self.VLayout2.addWidget(self.outputListHead1)
        self.VLayout2.addWidget(self.outputList1)
        self.VLayout2.addWidget(self.inputListHead2)
        self.VLayout2.addWidget(self.inputList2)
        self.VLayout2.addWidget(self.outputListHead2)
        self.VLayout2.addWidget(self.outputList2)
        self.VLayout2.addWidget(self.inputListHead3)
        self.VLayout2.addWidget(self.inputList3)
        self.VLayout2.addWidget(self.outputListHead3)
        self.VLayout2.addWidget(self.outputList3)
        self.VLayout2.addWidget(self.inputListHead4)
        self.VLayout2.addWidget(self.inputList4)
        self.VLayout2.addWidget(self.outputListHead4)
        self.VLayout2.addWidget(self.outputList4)
        self.VLayout2.addWidget(self.inputListHead5)
        self.VLayout2.addWidget(self.inputList5)
        self.VLayout2.addWidget(self.outputListHead5)
        self.VLayout2.addWidget(self.outputList5)
        self.VLayout2.addWidget(self.inputListHead6)
        self.VLayout2.addWidget(self.inputList6)
        self.VLayout2.addWidget(self.outputListHead6)
        self.VLayout2.addWidget(self.outputList6)
        self.scrollWid = QWidget()
        self.scrollWid.setLayout(self.VLayout2)
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scrollWid)
        self.VLayout2Main.addWidget(self.scroll)
        #Creating 3rd Vertical box
        self.mainTextBox = QTextBrowser(self)
        self.mainTextBox.setText("GET CHANNEL and START MAIN output will be shown here!")    
        self.applyButton = QPushButton("Apply",self)
        self.applyButton.clicked.connect(lambda: self.applyFunc(1))
        self.startMainButton = QPushButton("Activate",self)
        self.startMainButton.setStyleSheet("background-color:red")
        self.startMainButton.clicked.connect(lambda: self.startM())
        self.stopButton = QPushButton("STOP",self)
        self.stopButton.clicked.connect(disconnect)
        self.showHereButton = QPushButton("Show Here",self)
        self.showHereButton.clicked.connect(lambda: self.showHereFunc())

        self.horiPairLayout2 = QHBoxLayout()
        self.horiPairLayout2.addWidget(self.applyButton)
        self.horiPairLayout2.addWidget(self.startMainButton)
        self.horiPairLayout2.addWidget(self.stopButton)
        self.mainTextBox.setReadOnly(True)
        self.VLayout3.addLayout(self.horiPairLayout2)
        self.VLayout3.addWidget(self.showHereButton)
        self.VLayout3.addWidget(self.mainTextBox)
        self.centralLayout.addWidget(self.menuBar)
        self.centralLayout.addLayout(self.horiLayout)
        self.horiLayout.addLayout(self.VLayout1)
        self.horiLayout.addLayout(self.VLayout2Main)
        self.horiLayout.addLayout(self.VLayout3)
    def ActivateFunc(self):
        print("Activate option clicked")
        dia = DialogBox(self)
        dia.show()
    def InstallAFunc(self):
        print("Install A option clicked")
        LinkingA()
    def InstallBFunc(self):
        print("Install B option clicked")
        LinkingB()
    def ContactFunc(self):
        showdialog()
        print("Contact option clicked")
    def DisplayAPI(self,s):
        api_id,api_hash = s.split(" ")
        self.apiIDLabel.setText(api_id)
        self.apiHashLabel.setText(api_hash)
        self.applyFunc(0)

    def getAPIFunc(self):
        print("GET API Pressed")
        apiThread = APIThread()
        apiThread.signals.result.connect(self.DisplayAPI)
        self.threadpool.start(apiThread)    
    def getChannelFunc(self):
        api_id = self.apiIDLabel.text()
        api_hash = self.apiHashLabel.text()
        self.getChannelProcess = QProcess()
        self.getChannelProcess.readyReadStandardOutput.connect(self.handle_stdout)
        self.getChannelProcess.readyReadStandardError.connect(self.handle_stderr)
        self.getChannelProcess.finished.connect(self.updateChannelList)
        self.getChannelProcess.start("python",['GetChannels.py'])
    
    def startM(self):
        print(self.apiIDLabel.text())
        if self.apiIDLabel.text()=='':
            mainMessage("API ID and API Hash are not available")
        else:
            flag,key = userpassGetter()
            print(flag)
            if flag==True:
                self.startMainButton.setText("Start Main")
                self.startMainButton.setStyleSheet(self.styleSheet)
                self.startMainButton.clicked.connect(startMain)
                self.mainTextBox.setPlainText("Activated\nClick Start Main\n""After entring phone and code on Console press SHOW HERE!")
            else:
                mainMessage("Your key is: "+key+"\nGive this key to the Provider ")

    def handle_stderr(self):
        data = self.getChannelProcess.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.mainTextBox.append(stderr)

    def handle_stdout(self):
        data = self.getChannelProcess.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        print(stdout)
        self.mainTextBox.append(stdout)
    def sendFunc(self,edit):
        text = edit.text() + "\n"
        self.getChannelProcess.write(text.encode())
        self.mainTextBox.append(text)
    def showHereFunc(self):
        self.mainTextBox.setText("")
        sys.stdout = Port(self.mainTextBox)
        print("Logged in..")
    def updateChannelList(self):
        with open("data.json","r") as f:
            data = json.load(f)
            self.allChannelList.clear()
            self.allChannelList.addItems(data["Channels"])
        print("UI Updated!")

    def changedLimit(self,listW,textW):
        if textW.text()!='':
            listW.itemLimit = int(textW.text())
    
    def getItems(self,listWidget):
        items = []
        for index in range(listWidget.count()):
            items.append(listWidget.item(index).textLabel.text())
        return items
    def applyFunc(self,flag):
        f = open("data.json")
        data = json.load(f)
        f.close()
        if flag==0:
            data['API ID'] = self.apiIDLabel.text()
            data['API Hash'] = self.apiHashLabel.text()
            print("API ID ,Hash SAVED")
        else:
            data['Input1'] = self.getItems(self.inputList1)
            data['Input2'] = self.getItems(self.inputList2)
            data['Input3'] = self.getItems(self.inputList3)
            data['Input4'] = self.getItems(self.inputList4)
            data['Input5'] = self.getItems(self.inputList5)
            data['Input6'] = self.getItems(self.inputList6)
            data['Output1'] = self.getItems(self.outputList1)
            data['Output2'] = self.getItems(self.outputList2)
            data['Output3'] = self.getItems(self.outputList3)
            data['Output4'] = self.getItems(self.outputList4)
            data['Output5'] = self.getItems(self.outputList5)
            data['Output6'] = self.getItems(self.outputList6)
            print("INPUT/OUTPUT SAVED")
           
        with open("data.json", "w") as outfile: 
            json.dump(data, outfile)

if __name__=="__main__":
    app = QApplication(sys.argv)
    pyqtRemoveInputHook()
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
