from qfluentwidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import backend
import sys
import os

filePath = str(os.path.dirname(__file__))

def isValidPath(animPath, widget):
    if animPath == "notazip":
        notazipw = MessageBox("Error!", "The file you opened is NOT a boot animation. At least, not a zip archive. Please make sure you picked the right file and try again.", widget)
        notazipw.show()
        return ""
    if animPath == "nodesc":
        nodescw = MessageBox("Error!", "The file you opened is NOT a boot animation. It doesn't have desc.txt! Please make sure you picked the right file and try again.", widget)
        nodescw.show()
        return ""
    if animPath == "":
        wtfw = MessageBox("Error!", "dafug", widget)
        wtfw.show()
        return ""
    if animPath.rfind("\\") == -1: 
        return animPath[animPath.rfind("/")+1:] # i use arch btw
    else:
        return animPath[animPath.rfind("\\")+1:]

class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setWindowTitle("BootToolKit")
        self.setWindowIcon(QIcon('./assets/appicon.png'))
        self.setFixedSize(506, 320)
        self.navigationInterface.setExpandWidth(160)
        self.titleBar.maxBtn.hide()
        # Create and add sub interfaces
        self.addSubInterface(ResizeWidget(), QIcon("./assets/resize.png"), 'Resize')
        self.addSubInterface(MagiskWidget(), QIcon("./assets/magiskmodule.png"), 'Magisk')

class ResizeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setObjectName("ResizePage")

    def initUI(self):
        # open button
        self.openbtn = PrimaryPushButton(QIcon("./assets/folder.png"), "Open...", self)
        self.openbtn.move(8, 8)
        self.openbtn.resize(128,32)
        self.openbtn.clicked.connect(self.openEvent)

        # boot animation name 
        self.fileLabel = StrongBodyLabel("", self)
        self.fileLabel.move(144, 8)
        self.fileLabel.resize(256, 32)

        # animation preview
        self.previewCard = CardWidget(self)
        self.previewCard.move(8,48)
        self.previewCard.setFixedSize(128,216)
        self.previewImg = ImageLabel(filePath + "/assets/appicon.png", self.previewCard)
        self.previewImg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.previewImg.setBorderRadius(6, 6, 6, 6)
        self.previewImg.scaledToWidth(124)
        self.previewImg.move(2, 106 - round(self.previewImg.height()/2))

        # target WxH label
        self.targetLabel = StrongBodyLabel("Target resolution:", self)
        self.targetLabel.resize(192, 32)
        self.targetLabel.move(144, 48)
        # width input
        self.widthInput = LineEdit(self)
        self.widthInput.setPlaceholderText("Width")
        self.widthInput.move(144, 84)
        self.widthInput.resize(140, 48)
        self.widthInput.setDisabled(True)
        # the X(!!!!!)
        self.theX = StrongBodyLabel("x", self)
        self.theX.move(292, 91)
        self.theX.resize(8, 16)
        # height input
        self.heightInput = LineEdit(self)
        self.heightInput.setPlaceholderText("Height")
        self.heightInput.move(308, 84)
        self.heightInput.resize(140, 48)
        self.heightInput.setDisabled(True)

        # base resolution label
        self.baseLabel = StrongBodyLabel("Base resolution:", self)
        self.baseLabel.resize(192, 32)
        self.baseLabel.move(144, 118)
        # width base
        self.widthBase = LineEdit(self)
        self.widthBase.setPlaceholderText("e.g. 1080")
        self.widthBase.move(144, 154)
        self.widthBase.resize(140, 48)
        self.widthBase.setDisabled(True)
        # the X(again)(!!!!!)
        self.theX2 = StrongBodyLabel("x", self)
        self.theX2.move(292, 161)
        self.theX2.resize(8, 16)
        # height base
        self.heightBase = LineEdit(self)
        self.heightBase.setPlaceholderText("e.g. 1920")
        self.heightBase.move(308, 154)
        self.heightBase.resize(140, 48)
        self.heightBase.setDisabled(True)

        # progress bar
        self.mainProgress = ProgressBar(self)
        self.mainProgress.setRange(0, 100)
        self.mainProgress.setValue(0)
        self.mainProgress.resize(296, 16)
        self.mainProgress.move(148, 248)

        # start button
        self.startButton = PushButton("Start", self)
        self.startButton.resize(296, 32)
        self.startButton.move(148, 200)
        self.startButton.setDisabled(True)
        self.startButton.clicked.connect(self.startEvent)

    def openEvent(self):
        resizeAnimPath = isValidPath(backend.openBootAnim(), self)
        if resizeAnimPath == "":
            return
        self.mainProgress.setValue(0)
        self.fileLabel.setText(resizeAnimPath)
        with open(filePath + "/temp/desc.txt") as f:
            descline = f.readline()
            desclist = descline.split(" ")
            self.baseWidth = desclist[0]
            self.baseHeight = desclist[1]
            self.widthBase.setText(str(self.baseWidth))
            self.heightBase.setText(str(self.baseHeight))
        self.widthInput.setDisabled(False)
        self.heightInput.setDisabled(False)
        self.startButton.setDisabled(False)
        self.previewImg.setImage(filePath + "/temp/part0/" + str(os.listdir(filePath + "/temp/part0")[0]))
        self.previewImg.scaledToWidth(124)
        
    def startEvent(self):
        invalidInputw = MessageBox("Error!", "Invalid width and/or height! Please check your input numbers.", self)

        # if input data is not a number
        try:
            int(self.widthInput.text()) - int(self.heightInput.text())
        except:
            invalidInputw.show()
            return
        if self.widthInput.text().strip() == "" or self.heightInput.text().strip() == "":
            invalidInputw.show()
            return
        else:
            backend.resizeAnimation(int(self.baseHeight), int(self.baseWidth), int(self.heightInput.text()), int(self.widthInput.text()), self.mainProgress)
            self.mainProgress.setValue(99999)

class MagiskWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setObjectName("MagiskPage")
    def initUI(self):
        # open button
        self.openbtn = PrimaryPushButton(QIcon(filePath + "/assets/folder.png"), "Open...", self)
        self.openbtn.move(8, 8)
        self.openbtn.resize(200, 32)
        # arrow
        self.arrow = ImageLabel(filePath + "/assets/arrow-left.png", self)
        self.arrow.scaledToWidth(16)
        self.arrow.move(220, 17)
        # start button
        self.startbtn = PushButton(QIcon(filePath + "/assets/magiskmodule.png"), "Create module", self)
        self.startbtn.move(248, 8)
        self.startbtn.resize(200, 32)
        # name label
        self.nameLabel = StrongBodyLabel("Name/ID:", self)
        self.nameLabel.resize(128, 32)
        self.nameLabel.move(8, 48)
        # name input
        self.nameInput = LineEdit(self)
        self.nameInput.setPlaceholderText("Name")
        self.nameInput.resize(128, 32)
        self.nameInput.move(8, 84)
        # id input
        self.idInput = LineEdit(self)
        self.idInput.setPlaceholderText("Module ID")
        self.idInput.resize(128, 32)
        self.idInput.move(8, 124)
        # version label
        self.versionLabel = StrongBodyLabel("Version/Code:", self)
        self.versionLabel.resize(128, 32)
        self.versionLabel.move(144, 48)
        # version input
        self.versionInput = LineEdit(self)
        self.versionInput.setPlaceholderText("Version")
        self.versionInput.resize(128, 32)
        self.versionInput.move(144, 84)
        # version code input
        self.vcodeInput = LineEdit(self)
        self.vcodeInput.setPlaceholderText("Version Code")
        self.vcodeInput.resize(128, 32)
        self.vcodeInput.move(144, 124)
        # author label
        self.authorLabel = StrongBodyLabel("Author:", self)
        self.authorLabel.resize(128, 32)
        self.authorLabel.move(280, 48)
        # author input
        self.authorInput = LineEdit(self)
        self.authorInput.setPlaceholderText("Author")
        self.authorInput.resize(128, 32)
        self.authorInput.move(280, 84)
        # description label
        self.descLabel = StrongBodyLabel("Description:", self)
        self.descLabel.resize(128, 32)
        self.descLabel.move(8, 160)
        # description input
        self.descInput = LineEdit(self)
        self.descInput.setPlaceholderText("Description...")
        self.descInput.resize(440, 32)
        self.descInput.move(8, 196)
        # progress bar
        self.mainProgress = ProgressBar(self)
        self.mainProgress.setRange(0, 100)
        self.mainProgress.setValue(0)
        self.mainProgress.resize(428, 16)
        self.mainProgress.move(14, 248)
    def openEvent(self):
        moduleAnimPath = isValidPath(backend.openBootAnim(), self)
        if moduleAnimPath == "":
            return
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())