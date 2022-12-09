import assets_rc_rc
from PyQt5 import QtCore, QtGui, QtWidgets


class GUIComponents(object):

    pageNames = ("Welcome", "MachineSetup", "MachineSetup2", "SampleSetup", "Compression", "Compression2", "Compression3", "Settings")

    def __init__(self, mainWindow: QtWidgets.QMainWindow):
        self.mainWindow = mainWindow
        self.pages = {name: QtWidgets.QWidget() for name in self.pageNames}
        self.setupUI(self.mainWindow, self.pages)

    def setupUI(self, MainWindow: QtWidgets.QMainWindow, pages: dict[str, QtWidgets.QWidget]):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setStyleSheet("background-color: white;")
        self.stackedWidget.setObjectName("stackedWidget")
        
        self.welcome_page = pages["Welcome"]
        self.welcome_page.setObjectName("welcome_page")
        self.welcomePage_img = QtWidgets.QLabel(self.welcome_page)
        self.welcomePage_img.setGeometry(QtCore.QRect(300, 70, 200, 200))
        self.welcomePage_img.setStyleSheet("border-image: url(:/newPrefix/image_1.png);")
        self.welcomePage_img.setText("")
        self.welcomePage_img.setObjectName("welcomePage_img")
        self.deviceName = QtWidgets.QLabel(self.welcome_page)
        self.deviceName.setGeometry(QtCore.QRect(300, 280, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.deviceName.setFont(font)
        self.deviceName.setStyleSheet("color: black;\n"
"border-image:none;")
        self.deviceName.setAlignment(QtCore.Qt.AlignCenter)
        self.deviceName.setObjectName("deviceName")
        self.software_version = QtWidgets.QLabel(self.welcome_page)
        self.software_version.setGeometry(QtCore.QRect(300, 320, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.software_version.setFont(font)
        self.software_version.setStyleSheet("color: black;\n"
"border-image:none;")
        self.software_version.setAlignment(QtCore.Qt.AlignCenter)
        self.software_version.setObjectName("software_version")
        self.stackedWidget.addWidget(self.welcome_page)

        self.Home_page = pages["SampleSetup"]
        self.Home_page.setObjectName("Home_page")
        self.frame = QtWidgets.QFrame(self.Home_page)
        self.frame.setGeometry(QtCore.QRect(390, 50, 370, 370))
        self.frame.setMinimumSize(QtCore.QSize(370, 370))
        self.frame.setMaximumSize(QtCore.QSize(370, 370))
        self.frame.setStyleSheet("border-image:none;")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(30)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.img_1_frame = QtWidgets.QFrame(self.frame)
        self.img_1_frame.setStyleSheet("border-radius: 10px;\n"
"background-color: red;")
        self.img_1_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.img_1_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.img_1_frame.setLineWidth(0)
        self.img_1_frame.setObjectName("img_1_frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.img_1_frame)
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.img_1 = QtWidgets.QLabel(self.img_1_frame)
        self.img_1.setStyleSheet("border-image: url(:/newPrefix/image_2.png);\n"
"border-radius: 10px;")
        self.img_1.setText("")
        self.img_1.setObjectName("img_1")
        self.gridLayout_3.addWidget(self.img_1, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.img_1_frame, 0, 0, 1, 1)
        self.img_2_frame = QtWidgets.QFrame(self.frame)
        self.img_2_frame.setStyleSheet("border-radius: 10px;\n"
"background-color: red;")
        self.img_2_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.img_2_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.img_2_frame.setLineWidth(0)
        self.img_2_frame.setObjectName("img_2_frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.img_2_frame)
        self.gridLayout_4.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.img_2 = QtWidgets.QLabel(self.img_2_frame)
        self.img_2.setMinimumSize(QtCore.QSize(148, 148))
        self.img_2.setStyleSheet("border-image: url(:/newPrefix/image_3.png);\n"
"border-radius: 10px;")
        self.img_2.setText("")
        self.img_2.setObjectName("img_2")
        self.gridLayout_4.addWidget(self.img_2, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.img_2_frame, 0, 1, 1, 1)
        self.img_3_frame = QtWidgets.QFrame(self.frame)
        self.img_3_frame.setStyleSheet("border-radius: 10px;\n"
"background-color: red;")
        self.img_3_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.img_3_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.img_3_frame.setLineWidth(0)
        self.img_3_frame.setObjectName("img_3_frame")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.img_3_frame)
        self.gridLayout_6.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.img_3 = QtWidgets.QLabel(self.img_3_frame)
        self.img_3.setMinimumSize(QtCore.QSize(148, 148))
        self.img_3.setStyleSheet("border-image: url(:/newPrefix/image_5.png);\n"
"border-radius: 10px;")
        self.img_3.setText("")
        self.img_3.setObjectName("img_3")
        self.gridLayout_6.addWidget(self.img_3, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.img_3_frame, 1, 0, 1, 1)
        self.img_4_frame = QtWidgets.QFrame(self.frame)
        self.img_4_frame.setStyleSheet("border-radius: 10px;\n"
"background-color: red;")
        self.img_4_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.img_4_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.img_4_frame.setLineWidth(0)
        self.img_4_frame.setObjectName("img_4_frame")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.img_4_frame)
        self.gridLayout_5.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.img_4 = QtWidgets.QLabel(self.img_4_frame)
        self.img_4.setMinimumSize(QtCore.QSize(148, 148))
        self.img_4.setStyleSheet("border-image: url(:/newPrefix/image_4.png);\n"
"border-radius: 10px;")
        self.img_4.setText("")
        self.img_4.setObjectName("img_4")
        self.gridLayout_5.addWidget(self.img_4, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.img_4_frame, 1, 1, 1, 1)
        self.setupComplete_txt = QtWidgets.QLabel(self.Home_page)
        self.setupComplete_txt.setEnabled(True)
        self.setupComplete_txt.setGeometry(QtCore.QRect(10, 60, 381, 161))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.setupComplete_txt.setFont(font)
        self.setupComplete_txt.setStyleSheet("color: #00937A;\n"
"border-image:none;")
        self.setupComplete_txt.setAlignment(QtCore.Qt.AlignCenter)
        self.setupComplete_txt.setObjectName("setupComplete_txt")
        self.homepage_msg = QtWidgets.QLabel(self.Home_page)
        self.homepage_msg.setEnabled(True)
        self.homepage_msg.setGeometry(QtCore.QRect(10, 240, 381, 161))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.homepage_msg.setFont(font)
        self.homepage_msg.setStyleSheet("color: black;\n"
"border-image:none;")
        self.homepage_msg.setAlignment(QtCore.Qt.AlignCenter)
        self.homepage_msg.setObjectName("homepage_msg")
        self.waiting_text = QtWidgets.QLabel(self.Home_page)
        self.waiting_text.setEnabled(True)
        self.waiting_text.setGeometry(QtCore.QRect(0, 50, 381, 361))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.waiting_text.setFont(font)
        self.waiting_text.setStyleSheet("color: #E64D49;\n"
"border-image:none;")
        self.waiting_text.setAlignment(QtCore.Qt.AlignCenter)
        self.waiting_text.setObjectName("waiting_text")
        self.homepage_msg.raise_()
        self.frame.raise_()
        self.setupComplete_txt.raise_()
        self.waiting_text.raise_()
        self.stackedWidget.addWidget(self.Home_page)
        
        self.Settings_page = pages["Settings"]
        self.Settings_page.setObjectName("Settings_page")
        self.option_1_txt = QtWidgets.QLabel(self.Settings_page)
        self.option_1_txt.setEnabled(True)
        self.option_1_txt.setGeometry(QtCore.QRect(0, 170, 801, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.option_1_txt.setFont(font)
        self.option_1_txt.setStyleSheet("color: black;\n"
"border-image:none;")
        self.option_1_txt.setAlignment(QtCore.Qt.AlignCenter)
        self.option_1_txt.setObjectName("option_1_txt")
        self.Settings_heading_txt = QtWidgets.QLabel(self.Settings_page)
        self.Settings_heading_txt.setEnabled(True)
        self.Settings_heading_txt.setGeometry(QtCore.QRect(50, 0, 241, 91))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.Settings_heading_txt.setFont(font)
        self.Settings_heading_txt.setStyleSheet("color: black;\n"
"border-image:none;")
        self.Settings_heading_txt.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Settings_heading_txt.setObjectName("Settings_heading_txt")
        self.option_2_txt = QtWidgets.QLabel(self.Settings_page)
        self.option_2_txt.setEnabled(True)
        self.option_2_txt.setGeometry(QtCore.QRect(0, 220, 801, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.option_2_txt.setFont(font)
        self.option_2_txt.setStyleSheet("color: black;\n"
"border-image:none;")
        self.option_2_txt.setAlignment(QtCore.Qt.AlignCenter)
        self.option_2_txt.setObjectName("option_2_txt")
        self.stackedWidget.addWidget(self.Settings_page)
        
        self.option_1Page = QtWidgets.QWidget()
        self.option_1Page.setObjectName("option_1Page")
        self.label_13 = QtWidgets.QLabel(self.option_1Page)
        self.label_13.setEnabled(True)
        self.label_13.setGeometry(QtCore.QRect(50, 0, 441, 91))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("color: black;\n"
"border-image:none;")
        self.label_13.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.option_1_value = QtWidgets.QLabel(self.option_1Page)
        self.option_1_value.setEnabled(True)
        self.option_1_value.setGeometry(QtCore.QRect(0, 120, 801, 221))
        font = QtGui.QFont()
        font.setPointSize(70)
        font.setBold(True)
        font.setWeight(75)
        self.option_1_value.setFont(font)
        self.option_1_value.setStyleSheet("color: black;\n"
"border-image:none;")
        self.option_1_value.setAlignment(QtCore.Qt.AlignCenter)
        self.option_1_value.setObjectName("option_1_value")
        self.stackedWidget.addWidget(self.option_1Page)

        self.option_2Page = QtWidgets.QWidget()
        self.option_2Page.setObjectName("option_2Page")
        self.option_2_value = QtWidgets.QLabel(self.option_2Page)
        self.option_2_value.setEnabled(True)
        self.option_2_value.setGeometry(QtCore.QRect(0, 120, 801, 221))
        font = QtGui.QFont()
        font.setPointSize(70)
        font.setBold(True)
        font.setWeight(75)
        self.option_2_value.setFont(font)
        self.option_2_value.setStyleSheet("color: black;\n"
"border-image:none;")
        self.option_2_value.setAlignment(QtCore.Qt.AlignCenter)
        self.option_2_value.setObjectName("option_2_value")
        self.label_14 = QtWidgets.QLabel(self.option_2Page)
        self.label_14.setEnabled(True)
        self.label_14.setGeometry(QtCore.QRect(50, 0, 441, 91))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("color: black;\n"
"border-image:none;")
        self.label_14.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.stackedWidget.addWidget(self.option_2Page)
        
        self.compression_loadingPage = pages["Compression2"]
        self.compression_loadingPage.setStyleSheet("background-color:")
        self.compression_loadingPage.setObjectName("compression_loadingPage")
        self.ext_val_frame = QtWidgets.QFrame(self.compression_loadingPage)
        self.ext_val_frame.setGeometry(QtCore.QRect(260, 60, 300, 307))
        self.ext_val_frame.setMinimumSize(QtCore.QSize(240, 240))
        self.ext_val_frame.setStyleSheet("background-color: none;\n"
"border-image: none;")
        self.ext_val_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ext_val_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ext_val_frame.setObjectName("ext_val_frame")
        self.guage_value = QtWidgets.QFrame(self.ext_val_frame)
        self.guage_value.setGeometry(QtCore.QRect(10, 10, 280, 280))
        self.guage_value.setStyleSheet("QFrame{\n"
"    border-radius: 140px;    \n"
"    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:0.400 rgba(85, 170, 255, 255), stop:0.395 rgba(255, 255, 255, 0));\n"
"}")
        self.guage_value.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.guage_value.setFrameShadow(QtWidgets.QFrame.Raised)
        self.guage_value.setObjectName("guage_value")
        self.circularBg_5 = QtWidgets.QFrame(self.ext_val_frame)
        self.circularBg_5.setGeometry(QtCore.QRect(10, 10, 280, 280))
        self.circularBg_5.setStyleSheet("QFrame{\n"
"    border-radius: 140px;    \n"
"    background-color: rgba(85, 85, 127, 100);\n"
"}")
        self.circularBg_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.circularBg_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.circularBg_5.setObjectName("circularBg_5")
        self.circularContainer_5 = QtWidgets.QFrame(self.ext_val_frame)
        self.circularContainer_5.setGeometry(QtCore.QRect(25, 25, 250, 250))
        self.circularContainer_5.setBaseSize(QtCore.QSize(0, 0))
        self.circularContainer_5.setStyleSheet("QFrame{\n"
"    border-radius: 125px;    \n"
"    background-color: white;\n"
"}")
        self.circularContainer_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.circularContainer_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.circularContainer_5.setObjectName("circularContainer_5")
        self.layoutWidget_5 = QtWidgets.QWidget(self.circularContainer_5)
        self.layoutWidget_5.setGeometry(QtCore.QRect(10, 20, 231, 211))
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.infoLayout_5 = QtWidgets.QGridLayout(self.layoutWidget_5)
        self.infoLayout_5.setContentsMargins(0, 0, 0, 0)
        self.infoLayout_5.setObjectName("infoLayout_5")
        self.numeric_value = QtWidgets.QLabel(self.layoutWidget_5)
        self.numeric_value.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Roboto Thin")
        font.setPointSize(70)
        self.numeric_value.setFont(font)
        self.numeric_value.setStyleSheet("color: rgb(115, 185, 255); padding: 0px; background-color: none;")
        self.numeric_value.setAlignment(QtCore.Qt.AlignCenter)
        self.numeric_value.setIndent(-1)
        self.numeric_value.setObjectName("numeric_value")
        self.infoLayout_5.addWidget(self.numeric_value, 0, 0, 1, 1)
        self.circularBg_5.raise_()
        self.guage_value.raise_()
        self.circularContainer_5.raise_()
        self.compressing_label = QtWidgets.QLabel(self.compression_loadingPage)
        self.compressing_label.setEnabled(True)
        self.compressing_label.setGeometry(QtCore.QRect(0, 340, 801, 91))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.compressing_label.setFont(font)
        self.compressing_label.setStyleSheet("color: black;\n"
"border-image:none;")
        self.compressing_label.setAlignment(QtCore.Qt.AlignCenter)
        self.compressing_label.setObjectName("compressing_label")
        self.compressing_label.raise_()
        self.ext_val_frame.raise_()
        self.stackedWidget.addWidget(self.compression_loadingPage)
        
        self.pressGo_page = self.pages["Compression"]
        self.pressGo_page.setObjectName("pressGo_page")
        self.pressGo_txt = QtWidgets.QLabel(self.pressGo_page)
        self.pressGo_txt.setEnabled(True)
        self.pressGo_txt.setGeometry(QtCore.QRect(0, 190, 801, 91))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.pressGo_txt.setFont(font)
        self.pressGo_txt.setStyleSheet("color: black;\n"
"border-image:none;")
        self.pressGo_txt.setAlignment(QtCore.Qt.AlignCenter)
        self.pressGo_txt.setObjectName("pressGo_txt")
        self.stackedWidget.addWidget(self.pressGo_page)

        self.pressGoMachineSetup = self.pages["MachineSetup"]
        self.pressGoMachineSetup.setObjectName("pressGoMachineSetup")
        self.pressGoMachineSetup_txt = QtWidgets.QLabel(self.pressGoMachineSetup)
        self.pressGoMachineSetup_txt.setEnabled(True)
        self.pressGoMachineSetup_txt.setGeometry(QtCore.QRect(0, 190, 801, 91))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.pressGoMachineSetup_txt.setFont(font)
        self.pressGoMachineSetup_txt.setStyleSheet("color: black;\n"
"border-image:none;")
        self.pressGoMachineSetup_txt.setAlignment(QtCore.Qt.AlignCenter)
        self.pressGoMachineSetup_txt.setObjectName("pressGoMachineSetup_txt")
        self.stackedWidget.addWidget(self.pressGoMachineSetup)

        self.success_page = self.pages["Compression3"]
        self.success_page.setObjectName("success_page")
        self.success_txt = QtWidgets.QLabel(self.success_page)
        self.success_txt.setEnabled(True)
        self.success_txt.setGeometry(QtCore.QRect(40, 190, 761, 91))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.success_txt.setFont(font)
        self.success_txt.setStyleSheet("color: #007A00;\n"
"border-image:none;")
        self.success_txt.setAlignment(QtCore.Qt.AlignCenter)
        self.success_txt.setObjectName("success_txt")
        self.success_icon = QtWidgets.QLabel(self.success_page)
        self.success_icon.setGeometry(QtCore.QRect(180, 200, 61, 61))
        self.success_icon.setStyleSheet("border-image: url(:/newPrefix/check.png);")
        self.success_icon.setText("")
        self.success_icon.setObjectName("success_icon")
        self.stackedWidget.addWidget(self.success_page)

        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentWidget(self.pages["Welcome"])
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.deviceName.setText(_translate("MainWindow", "Device"))
        self.software_version.setText(_translate("MainWindow", "Software Version 1.2.1"))
        self.setupComplete_txt.setText(_translate("MainWindow", "Setup\n"
" Complete"))
        self.homepage_msg.setText(_translate("MainWindow", "Press Dial\n"
"for Settings\n"
"or Wait for\n"
"Compression"))
        self.waiting_text.setText(_translate("MainWindow", "Waiting for\n"
"setup\n"
"Completion"))
        self.option_1_txt.setText(_translate("MainWindow", "> Option 1"))
        self.Settings_heading_txt.setText(_translate("MainWindow", "Settings"))
        self.option_2_txt.setText(_translate("MainWindow", "Option 2"))
        self.label_13.setText(_translate("MainWindow", "Settings: Option 1"))
        self.option_1_value.setText(_translate("MainWindow", "10"))
        self.option_2_value.setText(_translate("MainWindow", "25"))
        self.label_14.setText(_translate("MainWindow", "Settings: Option 2"))
        self.numeric_value.setText(_translate("MainWindow", "0"))
        self.compressing_label.setText(_translate("MainWindow", "Compressing"))
        self.pressGo_txt.setText(_translate("MainWindow", "Press Go for Compression"))
        self.pressGoMachineSetup_txt.setText(_translate("MainWindow", "Press Go to Home Device"))
        self.success_txt.setText(_translate("MainWindow", "Compression Done"))


class GUITransitions(object):

    def __init__(self, mainWindow: QtWidgets.QMainWindow, guiComponents: GUIComponents):
        self.mainWindow = mainWindow
        self.guiComponents = guiComponents

    def swapPages(self, newPage: str, currPage: str=None):
        if ((currPage and currPage not in self.guiComponents.pages.keys()) or newPage not in self.guiComponents.pages.keys()):
            if (currPage):
                raise Exception(f"Either new page name '{newPage}' or current page name '{currPage}' not found in list of defined pages...")
            else:
                raise Exception(f"New page name '{newPage}' not found in list of defined pages...")

        newPage = self.guiComponents.pages[newPage]
        if (currPage):
            oldPage = self.guiComponents.pages[currPage]
            self.slidePageUpOut(oldPage)
            self.fade(oldPage)
        self.slidePageUpIn(newPage)
        self.guiComponents.stackedWidget.setCurrentWidget(newPage)

    def slidePageUpIn(self, widget: QtWidgets.QWidget):
        self.unfade(widget)
        self.animIn = QtCore.QPropertyAnimation(widget, b"geometry")
        self.animIn.setDuration(500)
        self.animIn.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        self.animIn.setStartValue(QtCore.QRect(0, 100, 800, 480))
        self.animIn.setEndValue(QtCore.QRect(0, 0, 800, 480))
        self.animIn.start()

    def slidePageUpOut(self, widget: QtWidgets.QWidget):
        self.unfade(widget)
        self.animOut = QtCore.QPropertyAnimation(widget, b"geometry")
        self.animOut.setDuration(500)
        self.animOut.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        self.animOut.setStartValue(QtCore.QRect(0, 0, 800, 480))
        self.animOut.setEndValue(QtCore.QRect(0, -100, 800, 480))
        self.animOut.start()

    def fade(self, widget: QtWidgets.QWidget):
        self.effect = QtWidgets.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animFade = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animFade.setDuration(500)
        self.animFade.setStartValue(1)
        self.animFade.setEndValue(0)
        self.animFade.start()

    def unfade(self, widget: QtWidgets.QWidget):
        self.effect = QtWidgets.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animUnfade = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animUnfade.setDuration(500)
        self.animUnfade.setStartValue(0)
        self.animUnfade.setEndValue(1)
        self.animUnfade.start()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    gui = GUIComponents(win)
    transitions = GUITransitions(win, gui)
    win.show()
    sys.exit(app.exec_())
