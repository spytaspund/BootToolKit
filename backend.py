import crossfiledialog
import zipfile
import shutil
import os
from qfluentwidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QHBoxLayout

filePath = str(os.path.dirname(__file__))

def zip_directory(path, zip_file_handle):
    for root, _dirs, files in os.walk(path):
        for file in files:
            zip_file_handle.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))
    print(f'Directory {path} zipped successfully')

def countFilesInDir(directory_path):
    files = [
        f
        for f in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, f))
    ]
    return len(files)

def getAllLinesNumber(path):
    number = 0
    numparts = len(next(os.walk(path))[1])
    for i in range(0, numparts):
        number = number + countFilesInDir(path + "/part" + str(i))
    return number

def openBootAnim(parent):
    fileName = crossfiledialog.open_file()
    if str(fileName).endswith(".zip") != True:
        fileName = "notazip"
        return fileName
    # do not forget to return filename
    with zipfile.ZipFile(fileName) as zipf:
        shutil.rmtree(filePath + "/temp")
        zipf.extractall(filePath + "/temp")
    try:
        desc = open(filePath + "/temp/desc.txt", "r") # in case zip is not a boot anim
    except FileNotFoundError:
        fileName = "nodesc"
    return fileName

def resizeLine(line, baseHeight, baseWidth, targetHeight, targetWidth):
    if line != "":
        a = line.split("x")[0]
        b = line.split("x")[1].split("+")[0]
        c = int(line.split("x")[1].split("+")[1])
        d = int(line.split("x")[1].split("+")[2])
        # c = w:2 - a:2
        # d = h:2 - b:2
        # h = d*2 + b
        # w = c*2 + b
        # offset = base - 2c - b
        # offset = (base - a)/2 - c 
        offsetc = round((baseWidth-int(a))/ 2) - c
        offsetd = round((baseHeight-int(b))/ 2) - d
        cnew = round((targetWidth - int(a))/2) + offsetc
        dnew = round((targetHeight - int(b))/2) + offsetd
        outstr = a + "x" + b + "+" + str(cnew) + "+" + str(dnew)
        return outstr
    else:
        return ""

def resizeAnimation(baseHeight, baseWidth, targetHeight, targetWidth, pbar):
    savePath = crossfiledialog.save_file(title="Select folder to save resized bootanimation.zip")
    numparts = len(next(os.walk(filePath + "/temp"))[1])
    totalLineSum = getAllLinesNumber(filePath + "/temp")
    pbar.setRange(0, totalLineSum + numparts*25)

    # get desc lines
    with open(filePath + "/temp/desc.txt", "r") as desc:
        desclines = desc.read().split('\n')
    # edit first line
    with open(filePath + "/temp/desc.txt", "w") as desc:
        framerate = desclines[0].split(" ")[2]
        desclines[0] = str(targetWidth) + " " + str(targetHeight) + " " + framerate
        for line in desclines:
            desc.write(line + '\n')
    
    # edit all trim.txt's
    for part in range(0, numparts):
        # get all lines
        with open(filePath + "/temp/part" + str(part) + "/trim.txt", "r+") as trim:
            trimlines = trim.read().split("\n")
        # resize every line
        with open(filePath + "/temp/part" + str(part) + "/trim.txt", "w") as trim:
            for line in trimlines:
                if line.strip() != "":
                    resizedLine = resizeLine(line, baseHeight, baseWidth, targetHeight, targetWidth)
                    trim.write(resizedLine + '\n')
                    pbar.setValue(pbar.value() + 1)
    # zip it up
    with zipfile.ZipFile(savePath, "w", zipfile.ZIP_STORED) as zipf:
        for part in range(0, numparts):
            zip_directory(filePath + "/temp/part" + str(part), zipf)
            pbar.setValue(pbar.value() + 25)
        zipf.write(filePath + "/temp/desc.txt", "desc.txt")