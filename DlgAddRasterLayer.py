"""
/***************************************************************************
wktRasterDialog
A QGIS plugin
Allows connecting to database and choose wktraster tables.
                             -------------------
begin                : 2010-10-20 
copyright            : (C) 2010 by Mauricio de Paulo
email                : mauricio.dev@gmail.com 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui 
from ui.DlgAddRasterLayer import Ui_DlgAddRasterLayer
import conn
from qgis.core import *

# create the dialog for zoom to point
class DlgAddRasterLayer(QtGui.QDialog,Ui_DlgAddRasterLayer):
    def __init__(self): 
        QtGui.QDialog.__init__(self) 
        # Set up the user interface from Designer. 
        self.setupUi(self) 
        dblist = conn.listDatabases()
        self.comboBox.addItems(dblist.keys())
        if len(dblist.keys()) > 0:
            self.listTables(0)
        QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.listTables)
        QtCore.QObject.connect(self.tableWidget, QtCore.SIGNAL("cellClicked(int,int)"), self.copyTableName)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.run)
    
    def getCurrentConnection(self):
        return self.comboBox.currentText() 
    
    def getTable(self):
        return self.lineEdit.text()
    
    def listTables(self,i):
        """This method connects to the database using a python Postgres connection and reads the raster_columns table"""
        connstring=conn.getConnString(self,self.getCurrentConnection())
        tables=conn.listTables(self,connstring) #returns a list of pairs (index, value)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        for table in tables:
            self.tableWidget.insertRow(0)
            for pair in table:
                self.tableWidget.setItem(0,pair[0],pair[1])
            

    
    def copyTableName(self,i,j):
        #test if the table is external. GDAL doesn't suport external yet.
        if (self.tableWidget.item(i,4).text()=="True"):
            self.lineEdit.setText("GDAL does not support external tables yet.")
        else:
            self.lineEdit.setText(self.tableWidget.item(i,0).text()+"."+self.tableWidget.item(i,1).text())

    # run method that performs all the real work
    def run(self): 
        table=self.getTable().split(".") #splits table name from schema
        if (table[0]=="GDAL does not support external tables yet"):
            QtGui.QMessageBox.warning(self,"Error", "GDAL does not support external tables yet")
            return False
        connstring = str(conn.getConnString(self,self.getCurrentConnection()))
        mode=self.comboBox_2.currentIndex()+1
        name=""
        
        #setting table name and mode
        if (mode!=3): #if not, then read entire database
            if len(table)>1:
                name+=table[0]
                connstring+=" schema="+table[0]
            connstring+=' table='+table[-1]+' mode='+str(mode)
            name+="."+table[-1]
        try:
            rlayer = QgsRasterLayer(connstring, name)
        except :
            QtGui.QMessageBox.warning(None,"Error","Could not load raster layer.")        
        #workaround for the nodata problem sets properties to fix the bug
        rlayer.setNoDataValue(-32768)
        rlayer.rasterTransparency().initializeTransparentPixelList(-32768)
        
        #try to add layer to qgis. 
        if rlayer.isValid():
            status=QgsMapLayerRegistry.instance().addMapLayer(rlayer)
        else:
            QtGui.QMessageBox.warning(self,"Error", "Could not load "+connstring)

