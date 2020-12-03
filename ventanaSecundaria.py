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
        Dialog.resize(627, 335)
        Dialog.setMouseTracking(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 8, 1, 1, 1)
        self.botonSiguienteIzq = QtWidgets.QPushButton(Dialog)
        self.botonSiguienteIzq.setObjectName("botonSiguienteIzq")
        self.gridLayout.addWidget(self.botonSiguienteIzq, 8, 4, 1, 1)
        self.botonCerrarVentana2 = QtWidgets.QPushButton(Dialog)
        self.botonCerrarVentana2.setObjectName("botonCerrarVentana2")
        self.gridLayout.addWidget(self.botonCerrarVentana2, 8, 6, 1, 1)
        self.labelY = QtWidgets.QLabel(Dialog)
        self.labelY.setText("")
        self.labelY.setObjectName("labelY")
        self.gridLayout.addWidget(self.labelY, 8, 2, 1, 1)
        self.scrollAreaVentana2 = QtWidgets.QScrollArea(Dialog)
        self.scrollAreaVentana2.setMouseTracking(False)
        self.scrollAreaVentana2.setWidgetResizable(True)
        self.scrollAreaVentana2.setObjectName("scrollAreaVentana2")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 607, 284))
        self.scrollAreaWidgetContents.setMouseTracking(False)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        
        
        self.scrollAreaVentana2.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollAreaVentana2, 0, 0, 1, 7)
        self.botonSiguienteDer = QtWidgets.QPushButton(Dialog)
        self.botonSiguienteDer.setObjectName("botonSiguienteDer")
        self.gridLayout.addWidget(self.botonSiguienteDer, 8, 5, 1, 1)
        self.horizontalSlider = QtWidgets.QSlider(Dialog)
        self.horizontalSlider.setMaximum(99)
        self.horizontalSlider.setMinimum(-99)
        self.horizontalSlider.setPageStep(1)
        self.horizontalSlider.setProperty("value", 0)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")

#        self.horizontalSlider_lab = QLabel()
#        self.horizontalSlider_lab.setText(str(self.horizontalSlider_opt.value())
#        self.horizontalSlider_lab.setEnabled(False)
#        hb_da_opt.addWidget(self.horizontalSlider_lab)
#        gb_dark_opt.setLayout(hb_dark_opt)
#        
        self.gridLayout.addWidget(self.horizontalSlider, 8, 3, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Escala"))
        self.botonSiguienteIzq.setText(_translate("Dialog", "Anterior"))
        self.botonCerrarVentana2.setText(_translate("Dialog", "Cerrar"))
        self.botonSiguienteDer.setText(_translate("Dialog", "Siguiente"))
