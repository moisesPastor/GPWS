# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ventanaSecundaria.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(627, 310)
        Dialog.setMouseTracking(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.labelNombreImg = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelNombreImg.setFont(font)
        self.labelNombreImg.setText("")
        self.labelNombreImg.setObjectName("labelNombreImg")
        self.gridLayout.addWidget(self.labelNombreImg, 0, 0, 1, 4)
        self.scrollAreaVentana2 = QtWidgets.QScrollArea(Dialog)
        self.scrollAreaVentana2.setMouseTracking(False)
        self.scrollAreaVentana2.setWidgetResizable(True)
        self.scrollAreaVentana2.setObjectName("scrollAreaVentana2")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 607, 215))
        self.scrollAreaWidgetContents.setMouseTracking(False)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaVentana2.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollAreaVentana2, 1, 0, 1, 7)
        self.botonZoomMenos = QtWidgets.QPushButton(Dialog)
        self.botonZoomMenos.setObjectName("botonZoomMenos")
        self.gridLayout.addWidget(self.botonZoomMenos, 2, 0, 1, 1)
        self.botonZoomMas = QtWidgets.QPushButton(Dialog)
        self.botonZoomMas.setObjectName("botonZoomMas")
        self.gridLayout.addWidget(self.botonZoomMas, 2, 1, 1, 1)
        self.barProb = QtWidgets.QProgressBar(Dialog)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.barProb.setFont(font)
        self.barProb.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.barProb.setMaximum(1)
        self.barProb.setProperty("value", 0)
        self.barProb.setObjectName("barProb")
        self.gridLayout.addWidget(self.barProb, 2, 2, 1, 2)
        self.botonSiguienteIzq = QtWidgets.QPushButton(Dialog)
        self.botonSiguienteIzq.setObjectName("botonSiguienteIzq")
        self.gridLayout.addWidget(self.botonSiguienteIzq, 2, 4, 1, 1)
        self.botonSiguienteDer = QtWidgets.QPushButton(Dialog)
        self.botonSiguienteDer.setObjectName("botonSiguienteDer")
        self.gridLayout.addWidget(self.botonSiguienteDer, 2, 5, 1, 1)
        self.botonCerrarVentana2 = QtWidgets.QPushButton(Dialog)
        self.botonCerrarVentana2.setObjectName("botonCerrarVentana2")
        self.gridLayout.addWidget(self.botonCerrarVentana2, 2, 6, 1, 1)
        self.labelX = QtWidgets.QLabel(Dialog)
        self.labelX.setText("")
        self.labelX.setObjectName("labelX")
        self.gridLayout.addWidget(self.labelX, 3, 2, 1, 1)
        self.labelY = QtWidgets.QLabel(Dialog)
        self.labelY.setText("")
        self.labelY.setObjectName("labelY")
        self.gridLayout.addWidget(self.labelY, 3, 3, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.botonZoomMenos.setText(_translate("Dialog", "Reducir"))
        self.botonZoomMas.setText(_translate("Dialog", "Ampliar"))
        self.botonSiguienteIzq.setText(_translate("Dialog", "Anterior"))
        self.botonSiguienteDer.setText(_translate("Dialog", "Siguiente"))
        self.botonCerrarVentana2.setText(_translate("Dialog", "Cerrar"))
