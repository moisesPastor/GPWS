#################################################################################
# Copyright 2020, Carlos Peralta Garcia & Moisés Pastor Gadea                   #
#                                                                               #
#   Licensed under the Apache License, Version 2.0                              #
#   you may not use this file except in compliance with the License.            #
#   You may obtain a copy of the License at                                     #
#                                                                               #
#       http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                               #
#   Unless required by applicable law or agreed to in writing, software         #
#   distributed under the License is distributed on an "AS IS" BASIS,           #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    #
#   See the License for the specific language governing permissions and         #
#   limitations under the License.                                              #
#                                                                               #
#   Created on: 06/08/2020                                                      #
#       Authors: Carlos Peralta Garcia & Moisés Pastor Gadea                    #       
#       Contact: cpega7391@gmail.com  mpastorg@prhlt.upv.es                     #   
#                                                                               #
#################################################################################



from PyQt5 import QtCore,  QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ventanaPrincipal import Ui_MainWindow
from ventanaSecundaria import Ui_Dialog
from functools import partial
from PIL import Image
from argparse import ArgumentParser
import sys


POS_PROB = 0
POS_F_NAME = 0

dicProb = {}
listMaxProbPage = []
localizaciones = {}
palabraUsr = ""
prob = -1
escala = 1
size = -1

class SecondWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        #self.setWindowFlags(Qt.FramelessWindowHint);
        self.setWindowFlags(Qt.WindowMaximizeButtonHint|Qt.WindowCloseButtonHint)       
        self.ui.setupUi(self)


class MyWindow(QMainWindow):
    def __init__(self):
        global dicProb
        
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.barBuscando.setVisible(False)
        self.myDialog = SecondWindow()
        self.ui.inputPalabra.setFocus()
        
        parser = ArgumentParser(description='%(prog)s is an word search for page images tool')       
        parser.add_argument('pageList', help='file containing the page list to search')
        parser.add_argument('pathToImgs', help='path to pageImages\'s')
        parser.add_argument('pathToIdx', help='path to index\'s')         
        args = parser.parse_args()       
        
        pageList = open(args.pageList)
        pages = pageList.read().split("\n")
        
        nombreImagenes = []
        nombreIndices = []
        for i in range(len(pages)):
            nombreImagenes.append(pages[i].split("/")[-1]+".jpg")           
            nombreIndices.append(pages[i].split("/")[-1]+".idx")

        for i in range(len(nombreImagenes)-1):
            try:
                file = open(args.pathToIdx + '/' +nombreIndices[i])            
                
                line_idx = file.readline().split(" ")
                      
            
                while len(line_idx) > 1:
                    line_idx[0]=line_idx[0].upper()
                    try:
                        dicProb[line_idx[0]].append([nombreImagenes[i], line_idx[1:8]])
                    except Exception:
                        dicProb[line_idx[0]] = list()
                        dicProb[line_idx[0]].append([nombreImagenes[i], line_idx[1:8]])
                                              
                    line_idx = file.readline().split(" ")
            
            except FileNotFoundError:
                print("ATENCION: los indices para la la pagina "+ nombreImagenes[i] + " no existe")


        def mostrarBuscadas():
            global listMaxProbPage

            numImagenesEncontradas = len(listMaxProbPage)
            if numImagenesEncontradas == 0:
                return
            
            #sort listMaxProbPage i localizaciones
            from operator import itemgetter

            if self.ui.tipoOrdenacion.currentIndex() == 0:
                listMaxProbPage.sort(reverse=True,key=itemgetter(1))
            else:
                if self.ui.tipoOrdenacion.currentIndex() == 1:
                    listMaxProbPage.sort(key=itemgetter(1))
                else:
                    listMaxProbPage.sort(key=itemgetter(0))
                    
            restauraGrid(self)
            contador = 0
            
            self.ui.barBuscando.setVisible(True)
            self.ui.barBuscando.setMaximum(100)
            self.ui.barBuscando.setFormat("%d " % contador)
            self.ui.barBuscando.setValue(contador)
            self.ui.barBuscando.setAlignment(Qt.AlignCenter)
                
                                                     
            incrementBarra = 100.0/numImagenesEncontradas
                    
            x = 0
            y = 0
            for i in range(numImagenesEncontradas):
                image = QImage(args.pathToImgs + "/" + listMaxProbPage[i][0])
                                                
                label_imageDisplay = QLabel()    
                label_imageDisplay.setPixmap(QPixmap.fromImage(image).scaled(350, 230)) 
                self.ui.gridImg.addWidget(label_imageDisplay, x, y)

                n = 1000000

                prob = float(listMaxProbPage[i][1])
                if prob > 1: prob = 1
                value = prob * 100
                prob = format(prob, '.12g')
                probImg = QtWidgets.QProgressBar()
                probImg.setStyleSheet(" QProgressBar { border: 1px solid black; border-radius: 0px; text-align: center; } QProgressBar::chunk {background-color: #3add36; width: 1px;}")
                                    
                probImg.setMaximum(100 * n)
                probImg.setProperty("value", -1)
                probImg.setObjectName("%s" % listMaxProbPage[i][1])
                                
                probImg.setValue(int(value * n))
                value = format(float(prob), '.2f')
                probImg.setFormat("%s " % value)
                botonMostrarImg1 = QtWidgets.QPushButton("%s" % listMaxProbPage[i][0])
                botonMostrarImg1.setObjectName("%s" % listMaxProbPage[i][0])
                botonMostrarImg1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                cbk = partial(ventanaImg, i)
                botonMostrarImg1.clicked.connect(cbk)
                self.ui.gridImg.addWidget(probImg, x+1, y)
                self.ui.gridImg.addWidget(botonMostrarImg1, x+2, y)

                if y < 2:
                    y += 1
                else:
                    x += 3
                    y = 0                                            
                
                self.ui.barBuscando.setFormat("%d " % int((i+1)*incrementBarra))
                self.ui.barBuscando.setValue(int((i+1)*incrementBarra))

                
                               
            self.ui.labelInfo.setText("%d páginas encontradas" % numImagenesEncontradas)
            self.ui.labelInfo.setStyleSheet("Color: blue")
            self.ui.barBuscando.setVisible(False)   

        
        def buscar():
            import re
            global numImagenesEncontradas, textoImg, dicProb, listMaxProbPage, palabraUsr, localizaciones, prob

            if prob == float(self.ui.inputProb.value()) and palabraUsr == self.ui.inputPalabra.text().upper().strip() :
                return
            
            listMaxProbPage = []
            localizaciones = {}            
            textoImg = []
            l = []

            var=""
            palabraUsr = self.ui.inputPalabra.text().upper().strip()            
            search_word_no_special_chars = re.sub('[^a-zA-Z ]', '', palabraUsr)
            queryFormatError = False;
            
            if len(palabraUsr) == 0:
                var = "(*) Debe introducir una palabra."                
                queryFormatError = True
            else:
                if len(search_word_no_special_chars) != len(palabraUsr):                 
                    var = "(*) ATENCIÓN!, la palabra no debe contener caracteres especiales.\n"                    
                    queryFormatError = True
                if len(palabraUsr.split(" ")) != 1:
                    var += "(*) ATENCIÓN!, debe introducir una sola palabra."
                    queryFormatError = True

            if(queryFormatError):
                self.ui.labelInfo.setText(var)
                self.ui.labelInfo.setStyleSheet("Color: red")
            else:
                self.ui.labelInfo.clear()
                prob = float(self.ui.inputProb.value())    
                try:
                    l = dicProb[palabraUsr]

                    for i in range(len(l)):
                        if float(l[i][1][POS_PROB]) >= prob:
                            if l[i][POS_F_NAME] in textoImg:
                                for j in range(len(listMaxProbPage)):                                      
                                    if listMaxProbPage[j][0] == l[i][POS_F_NAME] and float(l[i][1][POS_PROB]) > float(listMaxProbPage[j][1]):
                                        listMaxProbPage[j] = (l[i][POS_F_NAME],float(l[i][1][POS_PROB]))                                   
                                        break
                                localizaciones[l[i][POS_F_NAME]].append((l[i][1][1], l[i][1][2], l[i][1][3], l[i][1][4]))
                            else:
                                textoImg.append(l[i][POS_F_NAME])
                                listMaxProbPage.append((l[i][POS_F_NAME],float(l[i][1][POS_PROB])))
                                localizaciones[l[i][POS_F_NAME]] = list()
                                localizaciones[l[i][POS_F_NAME]].append((l[i][1][1], l[i][1][2], l[i][1][3], l[i][1][4]))

                    if (len(listMaxProbPage) == 0):
                        var = "%d coincidencias para \"%s\", \nninguna con probabilidad igual o superior a %.6g." % (len(l), self.ui.inputPalabra.text(), prob)
                        self.ui.labelInfo.setStyleSheet("Color: red")
                        self.ui.labelInfo.setText(var)
                        restauraGrid(self)
                    else:
                        mostrarBuscadas()
                except KeyError:
                    restauraGrid(self)
                    var = "No se han encontrado coincidencias de la palabra \"%s\" \nen ningún documento." % (self.ui.inputPalabra.text())
                    self.ui.labelInfo.setStyleSheet("Color: red")
                    self.ui.labelInfo.setText(var)
                                           
        
        def ventanaImg(indice):
            global listMaxProbPage, num, palabraUsr, image_orig, escala, size #, localizaciones           

            #self.myDialog.ui.horizontalSlider.setProperty("value", 0)
         
            num=indice
            pagina = listMaxProbPage[indice][0]
            image_orig = QPixmap(args.pathToImgs + "/" + pagina)                         
           
            #-------------------------------------------------------
            n = 1000000
            prob = float(listMaxProbPage[indice][1])
            if prob > 1: prob = 1
            value = prob * 100
            prob = format(prob, '.12g')
            value = format(float(prob), '.2f')
            self.myDialog.setWindowTitle("Imagen: %s\t\t Prob: %s" % (listMaxProbPage[indice][0], value))

            # pintar localizaciones            
            for i in range(len(localizaciones[pagina])):
                x1 = int(localizaciones[pagina][i][0])
                y1 = int(localizaciones[pagina][i][1])
                x2 = int(localizaciones[pagina][i][2])
                y2 = int(localizaciones[pagina][i][3])

                painterInstance = QPainter(image_orig)
                penRectangle = QtGui.QPen(QtCore.Qt.green)
                penRectangle.setWidth(5)
                painterInstance.setPen(penRectangle)
                #painterInstance.drawLine(x, y+int(yLen/2), x+xLen, y+int(yLen/2))
                painterInstance.drawLine(x1, y1, x2, y2)
                painterInstance.end()


            if size == -1:
                 h = image_orig.size().height()
                 w = image_orig.size().width()
                 size = image_orig.size() * escala
                 self.myDialog.resize(w, h)
                 
            #if escala != 1:                
            image = image_orig.scaled(size)
                       

            label_imageDisplay = QLabel()
            label_imageDisplay.setPixmap(image)
            self.myDialog.ui.scrollAreaVentana2.widget()
            label_imageDisplay.setAlignment(Qt.AlignCenter)
            self.myDialog.ui.scrollAreaVentana2.setWidget(label_imageDisplay)          
                
            self.myDialog.show()


        def siguienteImgDer():
            global num, textoImg, acumuladoGlobal
            if num < len(textoImg) - 1:
                num += 1
                ventanaImg(num)
                
        def siguienteImgIzq():
            global num, textoImg, acumuladoGlobal
            if num > 0:
                num -= 1
                ventanaImg(num)

        def muestraCreditos():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setWindowTitle("Créditos")
            msg.setText("Autores:\n\tCarlos Peralta Garcia\n\tMoises Pastor Gadea\nContacto:\n\tcpega7391@gmail.com\n\tmpastorg@prhlt.upv.es")
            #msg.setText("Autores:\n\tCarlos Peralta Garcia\nContacto:\n\tcpega7391@gmail.com")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()


        def restauraGrid(self):
            for i in reversed(range(self.ui.gridImg.count())): 
                self.ui.gridImg.itemAt(i).widget().deleteLater()

        def escalar():
            global image_orig, escala, size

 #           h = image.size().height()
 #           w = image.size().width()                
            
            escala = self.myDialog.ui.horizontalSlider.value() / 100 + 1            
            size = image_orig.size() * escala          
            img_escalada = image_orig.scaled(size)

            label_imageDisplay = QLabel()
            label_imageDisplay.setPixmap(img_escalada)

            label_imageDisplay.setAlignment(Qt.AlignCenter)
            self.myDialog.ui.scrollAreaVentana2.setWidget(label_imageDisplay)
            self.myDialog.show()
            
        self.myDialog.ui.botonCerrarVentana2.clicked.connect(self.myDialog.close)
        self.myDialog.ui.botonSiguienteDer.clicked.connect(siguienteImgDer)
        self.myDialog.ui.botonSiguienteIzq.clicked.connect(siguienteImgIzq)
        self.ui.botonBuscar.clicked.connect(buscar)
        self.ui.botonCreditos.clicked.connect(muestraCreditos)
        self.ui.inputPalabra.returnPressed.connect(buscar)
        self.ui.tipoOrdenacion.currentIndexChanged.connect(mostrarBuscadas)
        self.ui.inputProb.editingFinished.connect(buscar)
        self.myDialog.ui.horizontalSlider.valueChanged.connect(escalar)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())
