from qfluentwidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import backend
import sys
import os

resizeAnimPath = ""
previewImgPath = "./assets/appicon.png"
filePath = str(os.path.dirname(__file__))

class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setWindowTitle("BootResize")
        self.setWindowIcon(QIcon('./assets/appicon.png'))
        self.setFixedSize(506, 320)
        self.navigationInterface.setExpandWidth(160)
        self.titleBar.maxBtn.hide()
        # Create and add sub interfaces
        self.addSubInterface(ResizeWidget(), QIcon("./assets/resize.png"), 'Resize')

class ResizeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setObjectName("ResizePage")

    def initUI(self):
        global fileLabel
        global widthBase
        global heightBase
        global widthInput
        global heightInput
        global startButton
        global previewImg
        global mainProgress

        # open button
        openbtn = PrimaryPushButton(QIcon("./assets/folder.png"), "Open...", self)
        openbtn.move(8, 8)
        openbtn.resize(128,32)
        openbtn.clicked.connect(self.openbtnEvent)

        # boot animation name 
        fileLabel = StrongBodyLabel("", self)
        fileLabel.move(144, 8)
        fileLabel.resize(256, 32)

        # animation preview
        previewCard = CardWidget(self)
        previewCard.move(8,48)
        previewCard.setFixedSize(128,216)
        previewImg = ImageLabel(previewImgPath, previewCard)
        previewImg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        previewImg.setBorderRadius(6, 6, 6, 6)
        previewImg.scaledToWidth(124)
        previewImg.move(2, 106 - round(previewImg.height()/2))

        # target WxH label
        targetLabel = StrongBodyLabel("Target resolution:", self)
        targetLabel.resize(192, 32)
        targetLabel.move(144, 48)
        # width input
        widthInput = LineEdit(self)
        widthInput.setPlaceholderText("Width")
        widthInput.move(144, 84)
        widthInput.resize(140, 48)
        widthInput.setDisabled(True)
        # the X(!!!!!)
        theX = StrongBodyLabel("x", self)
        theX.move(292, 91)
        theX.resize(8, 16)
        # height input
        heightInput = LineEdit(self)
        heightInput.setPlaceholderText("Height")
        heightInput.move(308, 84)
        heightInput.resize(140, 48)
        heightInput.setDisabled(True)

        # base resolution label
        baseLabel = StrongBodyLabel("Base resolution:", self)
        baseLabel.resize(192, 32)
        baseLabel.move(144, 118)
        # width base
        widthBase = LineEdit(self)
        widthBase.setPlaceholderText("e.g. 1080")
        widthBase.move(144, 154)
        widthBase.resize(140, 48)
        widthBase.setDisabled(True)
        # the X(again)(!!!!!)
        theX2 = StrongBodyLabel("x", self)
        theX2.move(292, 161)
        theX2.resize(8, 16)
        # height base
        heightBase = LineEdit(self)
        heightBase.setPlaceholderText("e.g. 1920")
        heightBase.move(308, 154)
        heightBase.resize(140, 48)
        heightBase.setDisabled(True)

        # progress bar
        mainProgress = ProgressBar(self)
        mainProgress.setRange(0, 100)
        mainProgress.setValue(0)
        mainProgress.resize(296, 16)
        mainProgress.move(148, 248)

        # start button
        startButton = PushButton("Start", self)
        startButton.resize(296, 32)
        startButton.move(148, 200)
        startButton.setDisabled(True)
        startButton.clicked.connect(self.startResize)

    def openbtnEvent(self):
        global baseHeight
        global baseWidth
        resizeAnimPath = backend.openBootAnim(self)
        mainProgress.setValue(0)
        if resizeAnimPath == "notazip":
            notazipw = MessageBox("Error!", "The file you opened is NOT a boot animation. At least, not a zip archive. Please make sure you picked the right file and try again.", self)
            notazipw.show()
            resizeAnimPath = ""
        if resizeAnimPath == "nodesc":
            nodescw = MessageBox("Error!", "The file you opened is NOT a boot animation. It doesn't have desc.txt! Please make sure you picked the right file and try again.", self)
            nodescw.show()
            resizeAnimPath = ""
        if resizeAnimPath == "":
            return
        if resizeAnimPath.rfind("\\") == -1: 
            fileLabel.setText(resizeAnimPath[resizeAnimPath.rfind("/")+1:])
        else:
            fileLabel.setText(resizeAnimPath[resizeAnimPath.rfind("\\")+1:])
        with open(filePath + "/temp/desc.txt") as f:
            descline = f.readline()
            desclist = descline.split(" ")
            baseWidth = desclist[0]
            baseHeight = desclist[1]
            widthBase.setText(str(baseWidth))
            heightBase.setText(str(baseHeight))
        widthInput.setDisabled(False)
        heightInput.setDisabled(False)
        startButton.setDisabled(False)
        previewImg.setImage(filePath + "/temp/part0/" + str(os.listdir(filePath + "/temp/part0")[0]))
        previewImg.scaledToWidth(124)
        
    def startResize(self):
        invalidInputw = MessageBox("Error!", "Invalid width and/or height! Please check your input numbers.", self)

        # if input data is not a number
        try:
            int(widthInput.text()) - int(heightInput.text())
        except:
            invalidInputw.show()
            return
        if widthInput.text().strip() == "" or heightInput.text().strip() == "":
            invalidInputw.show()
            return
        else:
            backend.resizeAnimation(int(baseHeight), int(baseWidth), int(heightInput.text()), int(widthInput.text()), mainProgress)
            mainProgress.setValue(99999)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())