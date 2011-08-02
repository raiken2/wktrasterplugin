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
import conn, os, sys
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
        #del self.db
        
class rasterLoaderProcess(QtCore.QThread):
    def __init__(self,connstring,fileName,tablename,epsg,blocksizex,blocksizey,nover,isexternal):
        QtCore.QThread.__init__(self)
        #setting main parameters
        self.cmd=['qgis','-r',fileName,"-t",tablename,"-s",epsg,"-I","-M"]
        self.cmd+=["-k",blocksizex+"x"+blocksizey]
        if (isexternal): self.cmd.append("-R")
        self.connstring=connstring
        self.nover=nover
        
    def write(self,text):
        self.emit(QtCore.SIGNAL("writeText(PyQt_PyObject)"),text)
        
    def run(self):
        #starting the overview loop
        self.write("Connecting to database...")
        #the sql buffer is going to run the commands as they are being sent to the buffer
        self.sqlBuffer=buffer(self.connstring)
        sys.stdout=self.sqlBuffer
        
        for i in range(1,self.nover+1):
            #"-o",output,
            self.write("Storing overview "+str(i)+" on database...")
            cmdi=self.cmd[:]
            if (i>1): cmdi+=["-l",str(i)]
            
            sys.argv=cmdi
            import raster2pgsql
            #start the translation
            raster2pgsql.main()
            self.sqlBuffer.commit()
            self.write("Finished storing overview "+str(i)+".")
            del raster2pgsql
        del self.sqlBuffer
        

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
        fileName = QtGui.QFileDialog.getOpenFileName(self,"Open Image", os.getcwd(), "GDAL Supported Files (*)");
        if (fileName):
            self.lineEdit.setText(str(fileName))
            self.getMetadata(str(fileName))
        
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
        isexternal=self.checkBox_2.isChecked()
        self.process=rasterLoaderProcess(connstring, fileName, tablename, epsg, blocksizex, blocksizey, nover, isexternal)
        QtCore.QObject.connect(self.process,QtCore.SIGNAL('writeText(PyQt_PyObject)'),self.plainTextEdit.appendPlainText)
        QtCore.QObject.connect(self.process,QtCore.SIGNAL('finished()'),self.finishLoadRaster)
        self.process.run()
        #self.process.start()
        

    def finishLoadRaster(self):
        self.plainTextEdit.appendPlainText("Finished.")
        QtGui.QApplication.restoreOverrideCursor()
        
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

if __name__=="__main__":
    settings = QtCore.QSettings()
    key = "/PostgreSQL/connections/wktraster"
    settings.setValue(key + "/host", QtCore.QVariant("localhost"))
    settings.setValue(key + "/port", QtCore.QVariant(5432))
    settings.setValue(key + "/database", QtCore.QVariant("wktraster"))
    settings.setValue(key + "/username", QtCore.QVariant("postgres"))
    settings.setValue(key + "/password", QtCore.QVariant("teste"))
    
    
    settings.setValue("/PostgreSQL/connections/selected", QtCore.QVariant("wktraster"))
    
    app = QtGui.QApplication(sys.argv)
    
    dlg = DlgRasterLoader()
    dlg.show()
    
    retval = app.exec_()
    
    sys.exit(retval)
