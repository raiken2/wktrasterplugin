from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.core import *

#from .db_plugins import supportedDbTypes, createDbPlugin
#from .db_plugins.plugin import InvalidDataException, ConnectionError, Table, DbError
from postgis_utils import *

class SingletonConn(object):
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(SingletonConn, cls).__new__(cls)
        return cls._instance
    def __init__(self):
        #self.dbplugin = createDbPlugin('postgis')
        pass
    
    def listDatabases(self):
        actionsDb = {}
        settings = QSettings()
        settings.beginGroup("/PostgreSQL/connections")
        keys = settings.childGroups()
    
        for key in keys:
            actionsDb[unicode(key)] = key
        settings.endGroup()
        return actionsDb
    

#GeoDB=SingletonConn()

def listDatabases():
    actionsDb = {}
    settings = QSettings()
    settings.beginGroup("/PostgreSQL/connections")
    keys = settings.childGroups()

    for key in keys:
        actionsDb[unicode(key)] = key
    settings.endGroup()
    return actionsDb


    
def getConnString(parent,selected):
    settings = QSettings()
    # get connection details from QSettings
    settings.beginGroup(u"/PostgreSQL/connections/" + selected)
    if not settings.contains("database"): # non-existent entry?
        QMessageBox.critical(parent, "Error", "Unable to connect: there is no defined database connection \"%s\"." % selected)
        return

    get_value_str = lambda x: unicode(settings.value(x).toString())
    host, database, username, password = map(get_value_str, ["host", "database", "username", "password"])
    port = settings.value("port").toInt()[0]
    
    #searching for saved username qgis 1.5 >
    if not ( settings.value("saveUsername").toBool()):
        (username, ok) = QInputDialog.getText(parent, "Enter user name", "Enter user name for connection \"%s\":" % selected, QLineEdit.Normal)
        if not ok: return
    
    
    # qgis1.5 use 'savePassword' instead of 'save' setting
    if not (settings.value("save").toBool() or settings.value("savePassword").toBool()):
        (password, ok) = QInputDialog.getText(parent, "Enter password", "Enter password for connection \"%s\":" % selected, QLineEdit.Password)
        if not ok: return
    settings.endGroup()
    return ('PG: dbname=%s host=%s user=%s password=%s port=%s') % (database, host, username, password, port)

def listTables(parent,connstring):
    """This method connects to the database using a python Postgres connection and reads the raster_columns table"""
    attrMap={1:0,0:1,11:2,8:6,9:7,10:4,7:3} #this a map of the raster_columns column order with the displayed order
    parmlist=connstring.split(" ")
    try:
        db = GeoDB(host=parmlist[2].split("=")[1],dbname=parmlist[1].split("=")[1],user=parmlist[3].split("=")[1],passwd=parmlist[4].split("=")[1],port=int(parmlist[5].split("=")[1]))
        rows=db.list_rastertables()
    except DbError, e:
        QMessageBox.warning(None,"Error",str(e))#"Connection failed to "+connstring)
        return []
         
         
    tables=[]
    for row in rows:
        table=[]
        for i,key in enumerate(attrMap.keys()):
            cel=QTableWidgetItem(str(row[key])) #tname
            table.append((attrMap[key],cel))
        tables.append(table)
    return tables
    
"""def runSQL(parent,connstring,sql):
    db = QSqlDatabase.addDatabase("QPSQL")
    if db==None:
        QMessageBox.warning(parent,"Error", "Could not load PyQt's PostgreSQL driver")
        return None
    parmlist=connstring.split(" ")
    db.setDatabaseName(parmlist[1].split("=")[1])
    db.setHostName(parmlist[2].split("=")[1])
    db.setUserName(parmlist[3].split("=")[1])
    db.setPassword(parmlist[4].split("=")[1])
    db.setPort(int(parmlist[5].split("=")[1]))
    ok = db.open()
    if not ok:
        QMessageBox.warning(parent,"Error","Connection failed to "+conn)
        return None
    query=db.exec_(sql)"""

def listRIDs(parent, connstring, table):
    """This method connects to the database using a python Postgres connection and reads the rids available in a raster table"""
    parmlist=connstring.split(" ")
    try:
        db = GeoDB(host=parmlist[2].split("=")[1],dbname=parmlist[1].split("=")[1],user=parmlist[3].split("=")[1],passwd=parmlist[4].split("=")[1],port=int(parmlist[5].split("=")[1]))
        cursor = db.con.cursor()   
        result=db._exec_sql(cursor,"select rid from "+str(table))
        rows=cursor.fetchall()        
    except DbError, e:
        QMessageBox.warning(None,"Error",str(e))#"Connection failed to "+connstring)
        return []
         
    rids=[]
    for row in rows:
        rids.append(str(row[0]))
    return rids
