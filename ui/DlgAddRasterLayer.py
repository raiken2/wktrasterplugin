# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/DlgAddRasterLayer.ui'
#
# Created: Mon Aug  1 17:41:10 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DlgAddRasterLayer(object):
    def setupUi(self, DlgAddRasterLayer):
        DlgAddRasterLayer.setObjectName(_fromUtf8("DlgAddRasterLayer"))
        DlgAddRasterLayer.resize(524, 339)
        self.formLayout = QtGui.QFormLayout(DlgAddRasterLayer)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(DlgAddRasterLayer)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.comboBox = QtGui.QComboBox(DlgAddRasterLayer)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.label_3 = QtGui.QLabel(DlgAddRasterLayer)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.modeComboBox = QtGui.QComboBox(DlgAddRasterLayer)
        self.modeComboBox.setEnabled(True)
        self.modeComboBox.setObjectName(_fromUtf8("modeComboBox"))
        self.modeComboBox.addItem(_fromUtf8(""))
        self.modeComboBox.addItem(_fromUtf8(""))
        self.modeComboBox.addItem(_fromUtf8(""))
        self.modeComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.modeComboBox)
        self.tableWidget = QtGui.QTableWidget(DlgAddRasterLayer)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.tableWidget)
        self.label_2 = QtGui.QLabel(DlgAddRasterLayer)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEdit = QtGui.QLineEdit(DlgAddRasterLayer)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit)
        self.label_4 = QtGui.QLabel(DlgAddRasterLayer)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.ridComboBox = QtGui.QComboBox(DlgAddRasterLayer)
        self.ridComboBox.setObjectName(_fromUtf8("ridComboBox"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.ridComboBox)
        self.buttonBox = QtGui.QDialogButtonBox(DlgAddRasterLayer)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.SpanningRole, self.buttonBox)

        self.retranslateUi(DlgAddRasterLayer)
        self.modeComboBox.setCurrentIndex(2)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DlgAddRasterLayer.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DlgAddRasterLayer.reject)
        QtCore.QMetaObject.connectSlotsByName(DlgAddRasterLayer)

    def retranslateUi(self, DlgAddRasterLayer):
        DlgAddRasterLayer.setWindowTitle(QtGui.QApplication.translate("DlgAddRasterLayer", "Load Postgis Raster layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DlgAddRasterLayer", "Postgis\' connection:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DlgAddRasterLayer", "Reading mode:", None, QtGui.QApplication.UnicodeUTF8))
        self.modeComboBox.setItemText(0, QtGui.QApplication.translate("DlgAddRasterLayer", "Read table\'s vector representation", None, QtGui.QApplication.UnicodeUTF8))
        self.modeComboBox.setItemText(1, QtGui.QApplication.translate("DlgAddRasterLayer", "Read one row as a raster", None, QtGui.QApplication.UnicodeUTF8))
        self.modeComboBox.setItemText(2, QtGui.QApplication.translate("DlgAddRasterLayer", "Read one table as a raster", None, QtGui.QApplication.UnicodeUTF8))
        self.modeComboBox.setItemText(3, QtGui.QApplication.translate("DlgAddRasterLayer", "Read the dataset as a raster", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("DlgAddRasterLayer", "Schema", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("DlgAddRasterLayer", "Table", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("DlgAddRasterLayer", "SRID", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("DlgAddRasterLayer", "Pixel Type", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("DlgAddRasterLayer", "Is external file", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("DlgAddRasterLayer", "Is regular block", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(6).setText(QtGui.QApplication.translate("DlgAddRasterLayer", "Pixel size x ", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(7).setText(QtGui.QApplication.translate("DlgAddRasterLayer", "Pixel size y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DlgAddRasterLayer", "Table name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("DlgAddRasterLayer", "Row identifier:", None, QtGui.QApplication.UnicodeUTF8))
