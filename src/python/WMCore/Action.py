"""
A basic action is a thing that will run a SQL statement

A more complex one would be something that ran multiple SQL 
objects to produce a single output.
"""
from WMCore.Database.Dialects import MySQLDialect
from WMCore.Database.Dialects import SQLiteDialect
from WMCore.Database.Dialects import OracleDialect

class BaseAction(object):
    name = "BaseAction"
    def __init__(self, package='WMCore', logger=None):
        self.package = package
        self.logger = logger
        self.logger.debug("Instantiating %s Action object" % self.name)
        self.dialects = {"Oracle" : OracleDialect,
                    "MySQL" : MySQLDialect,
                    "SQLite" : SQLiteDialect}
    
    def loadDialect(self, classname, dbinterface):
        """
        Somewhat fugly method to load generic SQL classes...
        """
        
        dia = dbinterface.engine.dialect
        #TODO: Make good
        dialect = None
        for i in self.dialects.keys():
            if isinstance(dia, self.dialects[i]): 
                dialect = i
        if not dialect: 
            raise TypeError, "unknown connection type: %s" % dia
        
        module = "%s.%s.%sSQL" % (self.package, dialect, classname)
        self.logger.debug("importing %s, %s" % (module, classname))
        module = __import__(module, globals(), locals(), [classname], -1)
        instance = getattr(module, classname.split('.')[-1])
        return instance

    
    def execute(self, dbinterface = None):
        myclass = self.loadDialect(self.name, dbinterface)
        action = myclass(self.logger, dbinterface)
        try:
            return action.execute()
        except Exception, e:
            self.logger.exception(e)
            return False

class BoundAction(BaseAction):
    """
    Subclass of BaseAction that takes kwargs to the execute method
    """
    
    def execute(self, **kwargs):
        if not 'dbinterface' in kwargs.keys():
            raise ValueError, "You must pass a dbinterface to a BoundAction's execute method"
        myclass = self.loadDialect(self.name, dbinterface)
        action = myclass(self.logger, dbinterface)
        try:
            return action.execute(kwargs)
        except Exception, e:
            self.logger.exception(e)
            return False