# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ventana_inicio.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_AvatarsVSRooks(object):
    def setupUi(self, AvatarsVSRooks):
        if not AvatarsVSRooks.objectName():
            AvatarsVSRooks.setObjectName(u"AvatarsVSRooks")
        AvatarsVSRooks.setEnabled(True)
        AvatarsVSRooks.resize(804, 600)
        AvatarsVSRooks.setAcceptDrops(True)
        self.centralwidget = QWidget(AvatarsVSRooks)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(290, 360, 251, 132))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.Informacin = QLabel(self.verticalLayoutWidget)
        self.Informacin.setObjectName(u"Informacin")
        self.Informacin.setEnabled(True)
        self.Informacin.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.Informacin.setMouseTracking(False)
        self.Informacin.setStyleSheet(u"background-color: #FFFFFF;     /* gris oscuro */\n"
"color: black;                  /* color del texto */\n"
"border-radius: 8px; ")
        self.Informacin.setScaledContents(False)

        self.verticalLayout.addWidget(self.Informacin)

        self.txtUsuario = QLineEdit(self.verticalLayoutWidget)
        self.txtUsuario.setObjectName(u"txtUsuario")
        self.txtUsuario.setAutoFillBackground(False)
        self.txtUsuario.setDragEnabled(False)

        self.verticalLayout.addWidget(self.txtUsuario)

        self.txtPassword = QLineEdit(self.verticalLayoutWidget)
        self.txtPassword.setObjectName(u"txtPassword")
        self.txtPassword.setFrame(True)
        self.txtPassword.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayout.addWidget(self.txtPassword)

        self.btnEntrar = QPushButton(self.verticalLayoutWidget)
        self.btnEntrar.setObjectName(u"btnEntrar")

        self.verticalLayout.addWidget(self.btnEntrar)

        self.btn_registrarse = QPushButton(self.verticalLayoutWidget)
        self.btn_registrarse.setObjectName(u"btn_registrarse")

        self.verticalLayout.addWidget(self.btn_registrarse)

        self.fondo = QLabel(self.centralwidget)
        self.fondo.setObjectName(u"fondo")
        self.fondo.setGeometry(QRect(-2, -5, 811, 610))
        self.fondo.setPixmap(QPixmap(u"../images/fondo.jpg"))
        self.fondo.setScaledContents(True)
        AvatarsVSRooks.setCentralWidget(self.centralwidget)
        self.fondo.raise_()
        self.verticalLayoutWidget.raise_()
        self.statusbar = QStatusBar(AvatarsVSRooks)
        self.statusbar.setObjectName(u"statusbar")
        AvatarsVSRooks.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(AvatarsVSRooks)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 804, 33))
        AvatarsVSRooks.setMenuBar(self.menubar)

        self.retranslateUi(AvatarsVSRooks)

        QMetaObject.connectSlotsByName(AvatarsVSRooks)
    # setupUi

    def retranslateUi(self, AvatarsVSRooks):
        AvatarsVSRooks.setWindowTitle(QCoreApplication.translate("AvatarsVSRooks", u"MainWindow", None))
        self.Informacin.setText(QCoreApplication.translate("AvatarsVSRooks", u"  Ingrese su nombre de usuario y Contrase\u00f1a ", None))
        self.txtUsuario.setInputMask("")
        self.txtUsuario.setText("")
        self.txtUsuario.setPlaceholderText(QCoreApplication.translate("AvatarsVSRooks", u"Usuario", None))
        self.txtPassword.setText("")
        self.txtPassword.setPlaceholderText(QCoreApplication.translate("AvatarsVSRooks", u"Contrase\u00f1a", None))
        self.btnEntrar.setText(QCoreApplication.translate("AvatarsVSRooks", u"Entrar", None))
        self.btn_registrarse.setText(QCoreApplication.translate("AvatarsVSRooks", u"Registrarse", None))
        self.fondo.setText("")
    # retranslateUi

