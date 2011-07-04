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
from ui.DlgRasterLoader import Ui_DlgRasterLoader
import conn, os, sys, platform
import postgis_utils

class buffer:
    def __init__(self,connstring):
        parmlist=connstring.split(" ")
        self.db = postgis_utils.GeoDB(host=parmlist[2].split("=")[1],dbname=parmlist[1].split("=")[1],user=parmlist[3].split("=")[1],passwd=parmlist[4].split("=")[1],port=int(parmlist[5].split("=")[1]))
        if self.db==None:
            QtGui.QMessageBox.warning(None,"Error","Connection failed to "+connstring)
            return
        self.cursor = self.db.con.cursor()        
    def write(self,string):
        self.db._exec_sql(self.cursor, string)
    def commit(self):
        self.db.con.commit()


# create the dialog for zoom to point
class DlgRasterLoader(QtGui.QDialog,Ui_DlgRasterLoader):
    def __init__(self): 
        QtGui.QDialog.__init__(self) 
        # Set up the user interface from Designer. 
        self.setupUi(self) 
        #connections listing
        dblist = conn.listDatabases()
        self.comboBox.addItems(dblist.keys())
        
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.loadRaster)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.browseRaster)
        

    def checkPostgisRasterExtension(self,connstring):
        pass
    def getCurrentConnection(self):
        return self.comboBox.currentText()
        
    def browseRaster(self):
        fileName = str(QtGui.QFileDialog.getOpenFileName(self,"Open Image", os.getcwd(), "Image Files (*.tif)"));
        self.lineEdit.setText(fileName)
        
    def loadRaster(self):
        connstring = str(conn.getConnString(self,self.getCurrentConnection()))
        self.checkPostgisRasterExtension(connstring)
        self.plainTextEdit.appendPlainText("Checking parameters...")
        #running gdal2postgis.py
        fileName=str(self.lineEdit.text())
        tablename=str(self.lineEdit_3.text())#(os.path.split(fileName)[-1])[:-4]
        output=fileName[:-4]+'.sql'
        epsg=str(self.lineEdit_2.text())
        blocksize=str(self.lineEdit_4.text())
        cmd=['qgis','-r',fileName,"-t",tablename,"-l","1","-k",blocksize,"-s",epsg,"-I","-M"] #"-o",output,
        sys.argv=cmd
        import raster2pgsql
        #the sql buffer is going to run the commands as they are being sent to the buffer
        self.plainTextEdit.appendPlainText("Connecting to database...")
        sqlBuffer=buffer(connstring)
        sys.stdout=sqlBuffer
        #start the translation
        self.plainTextEdit.appendPlainText("Storing on database...")
        raster2pgsql.main()    
        sqlBuffer.commit()
        self.plainTextEdit.appendPlainText("Done.")
        
        
