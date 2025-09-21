from ast import Pow
from math import floor
from random import randint
import sys # Только для доступа к аргументам командной строки
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QBoxLayout, QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QMainWindow, QPushButton, QLabel
from PyQt6.QtCore import QSize, Qt
import os

#define OLED 96x16
#define OLED 64x32
#define OLED 64x48
#define OLED 128x64
#define OLED 64x128
#define tft_ 128x128
#define tft_ 80x160
#define tft_ 128x160
#define tft_ 160x128
#define tft_ 240x240
#define tft_round 240x240
#define tft_ 240x280
#define tft_ 240x320
#define tft2 320x240
#define tft2 480x320
#define tft_ 800x480
#define tft_ 1024x600
#define tft_ 1280 x 800

# расчитать в дюймах размеры (пикселей) для размера экрана в дюймах, в зависимости от диагонали монитора. Чтобы на мониторе отображался реальный размер tft (oled) экрана

# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):

  def __init__(self):
        super().__init__()
        self.setWindowTitle("TFT 160x128 emulator")
        self.setFixedSize(QSize(1280, 1000))
        self.initTftComboBox()
        self.initTestDrawComboBox()
        self.initDrawWidget()
        self.initButton()
        self.initControlLayout()
        self.initMainLayout()

        # Устанавливаем центральный виджет Window.
        widgetShow = QWidget()
        widgetShow.setLayout(self.layout)
        self.setLayout(self.layout)
        self.setCentralWidget(widgetShow)
        self.iteration = 300
        self.tftResolution= self.tft.currentData
        
        self.tft.currentIndexChanged.connect(self.ChangeResolutionTFT)
        
  def initDrawWidget(self):
     self.widget = QLabel()
     #self.image = QImage(0,0,QImage.Format.Format_RGB32)
     self.setResolutionTFT()
     self.widget.setPixmap(QPixmap(self.image))
     self.widget.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
     return
  def initMainLayout(self):
     self.layout = QHBoxLayout()
     self.layout.addWidget(self.widget,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
     self.layoutControls.addWidget(self.tft,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
     self.layoutControls.addWidget(self.tftDraw,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
     self.layoutControls.addWidget(self.button,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
     self.layout.addLayout(self.layoutControls)
     return
  def initControlLayout(self):
     self.layoutControls=QVBoxLayout()
     return 
  
  def initButton(self):
   self.button = QPushButton("Draw")
   self.button.setFixedSize(100, 60)
   self.button.clicked.connect(self.update)
   return  
  
  def initTftComboBox(self): # Выбор размера tft в пикселях
     self.tft = QComboBox()
     self.tft.setFixedSize(200, 60)
     self.tft.showEvent(self.initComboBoxTft())
     return 

  def initComboBoxTft(self): # список tft разрешений
        self.tft.addItem("OLED 96x16",[96,16])
        self.tft.addItem("OLED 64x32",[64,32])
        self.tft.addItem("OLED 64x48",[64,48])
        self.tft.addItem("OLED 128x64",[128,64])
        self.tft.addItem("OLED 64x128",[64,128])  
        self.tft.addItem("OLED 128x128",[128,128])  
        self.tft.addItem("TFT 80x160",[80,160])  
        self.tft.addItem("TFT 128x160",[128,160])  
        self.tft.addItem("TFT 160x128",[160,128])  
        self.tft.addItem("TFT 64x128",[64,128])  
        self.tft.addItem("TFT 240x240",[240,240])  
        self.tft.addItem("Round 240x240",[240,240])  
        self.tft.addItem("TFT 240x280",[240,280])  
        self.tft.addItem("TFT 240x320",[240,320]) 
        self.tft.addItem("TFT 320x240",[320,240])  
        self.tft.addItem("TFT 480x320",[480,320])  
        self.tft.addItem("TFT 800x480",[800,480])  
        self.tft.addItem("TFT 1024x600",[1024,600])  
        self.tft.addItem("TFT 1280x800",[1280,800])  
        self.setResolutionTFT()

  def initTestDrawComboBox(self): # выбор draw test
     self.tftDraw = QComboBox()
     self.tftDraw.setFixedSize(200, 60)
     self.tftDraw.showEvent(self.initTestDrawBox())
     return 
  def initTestDrawBox(self):     # список draw test
     self.tftDraw.addItem("Sierpinski triangle")
     self.setResolutionTFT()
        
  def setResolutionTFT(self):
        self.setWindowTitle(self.tft.currentText()+" emulator")  
        xy= self.tft.itemData(self.tft.currentIndex()) 
        self.image = QImage(xy[0],xy[1],QImage.Format.Format_RGB32)
        self.image.fill(0x00000000)
        
  def ChangeResolutionTFT(self):
        self.setWindowTitle(self.tft.currentText()+" emulator")  
        xy= self.tft.itemData(self.tft.currentIndex()) 
        self.image = QImage(xy[0],xy[1],QImage.Format.Format_RGB32)
        self.image.fill(0x00000000)
        self.widget.setPixmap(QPixmap(self.image))


  def drawImage(self):
    self.widget.setPixmap(QPixmap(self.image))
    return
  
  def update(self):
   for i in range(1,1000):
    self.serpinsky()
   self.drawImage()
   return 
 
 
 
 #X = (X-случайной вершины + X-предыдущей точки) / 2
 #Y = (Y-случайной вершины + Y-предыдущей точки) / 2
 
  def RecursionDrawing(self,previousDotCords,iteration):
    if iteration>self.iteration:
      return
    randomCorner = randint(0,2)
    x=int((self.cornerCords[randomCorner][0]+previousDotCords[0])/2)
    y=int((self.cornerCords[randomCorner][1]+previousDotCords[1])/2)
    self.image.setPixel(x,y,0xffffffff)
    self.RecursionDrawing([int((self.cornerCords[randomCorner][0]+previousDotCords[0])/2),int((self.cornerCords[randomCorner][1]+previousDotCords[1])/2)],iteration+1)
    

  def serpinsky(self):        
   self.cornerCords =  [[int(self.image.width()/2), 0],[0, int(self.image.height())],[int(self.image.width()),int(self.image.height())]] 
   self.RecursionDrawing(self.cornerCords[0],0)
   return

  def Change3Dcoordinates():
   return
      
# Приложению нужен один (и только один) экземпляр QApplication.
# Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
# Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
app = QApplication(sys.argv)

# Создаём виджет Qt — окно.
window = MainWindow()
window.show()  # Важно: окно по умолчанию скрыто.

# Запускаем цикл событий.
app.exec()


# Приложение не доберётся сюда, пока вы не выйдете и цикл
# событий не остановится.