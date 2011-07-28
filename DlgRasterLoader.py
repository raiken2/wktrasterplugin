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
import gdal
import re 

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
        del self.db


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
        self.widget.setVisible(False)

    def checkPostgisRasterExtension(self,connstring):
        pass
    def getCurrentConnection(self):
        return self.comboBox.currentText()
        
    def browseRaster(self):
        fileName = str(QtGui.QFileDialog.getOpenFileName(self,"Open Image", os.getcwd(), "Image Files (*.tif)"));
        self.lineEdit.setText(fileName)
        self.getMetadata(fileName)
        
    def loadRaster(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        
        connstring = str(conn.getConnString(self,self.getCurrentConnection()))
        self.checkPostgisRasterExtension(connstring)
        self.plainTextEdit.appendPlainText("Checking parameters...")
        #running gdal2postgis.py
        fileName=str(self.lineEdit.text())
        tablename=str(self.lineEdit_3.text())#(os.path.split(fileName)[-1])[:-4]
        epsg=str(self.lineEdit_2.text())
        blocksizex=str(self.spinBox_2.value())
        blocksizey=str(self.spinBox_3.value())
        nover=self.spinBox.value()
        for i in range(1,nover+1):
            cmd=['qgis','-r',fileName,"-t",tablename,"-l",str(i),"-s",epsg,"-I","-M"] #"-o",output,
            if (self.checkBox.isChecked()): cmd+=["-k",blocksizex+"x"+blocksizey]
            if (self.checkBox_2.isChecked()): cmd.append("-R")
            sys.argv=cmd
            import raster2pgsql
            #the sql buffer is going to run the commands as they are being sent to the buffer
            self.plainTextEdit.appendPlainText("Connecting to database...")
            sqlBuffer=buffer(connstring)
            sys.stdout=sqlBuffer
            #start the translation
            self.plainTextEdit.appendPlainText("Storing overview "+str(i)+"on database...")
            raster2pgsql.main()    
            sqlBuffer.commit()
            self.plainTextEdit.appendPlainText("Done.")
            del raster2pgsql
            del sqlBuffer
        
        QApplication.restoreOverrideCursor()
        
    def getMetadata(self,filename):
        #filename='/home/mauricio/Cartografia_Sistematica/Rio/landsat7_2005/L71217076_07620050617_B10.TIF'
        ds=gdal.Open(filename)
        #pattern that searches for EPSG values
        pattern=re.compile(r'\[?EPSG[^\]]*\]') 
        #captures the every EPSG in the projection description (contains elipsoid, units, etc)
        epsglist=pattern.findall(ds.GetProjection())
        if (len(epsglist)>0):
            epsg=epsglist[-1]
            pattern=re.compile(r'[\'"]\d*[\'"]')
            epsg=pattern.search(epsg)
            if (epsg==None):
                self.lineEdit_2.setText('-1')
            else:
                self.lineEdit_2.setText(epsg.group().strip('\"\'') )
        #self.spinBox_2.setValue(ds.RasterXSize)
        #self.spinBox_3.setValue(ds.RasterYSize)
        
        
        
        del ds
