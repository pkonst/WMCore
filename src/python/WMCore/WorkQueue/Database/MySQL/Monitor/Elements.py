"""
WMCore/WorkQueue/Database/MySQL/Monitor/Elements.py

DAO object for WorkQueue

WorkQueue database structure:
WMCore/WorkQueue/Database/CreateWorkQueueBase.py

hints on usage:
T0/DAS/Services/Tier0TomService.py
T0/DAS/Database/Oracle/RunsByStates.py

"""

__all__ = []
__revision__ = "$Id: Elements.py,v 1.2 2010/02/06 01:20:38 maxa Exp $"
__version__ = "$Revision: 1.2 $"


from WMCore.Database.DBFormatter import DBFormatter



class Elements(DBFormatter):
    sql = """SELECT id, wmtask_id, input_id, parent_queue_id, child_queue, num_jobs,
            priority, parent_flag, status, subscription_id, insert_time, update_time
            FROM wq_element"""

    def execute(self, conn = None, transaction = False):
        results = self.dbi.processData(self.sql, conn = conn,
                                       transaction = transaction)
        
        formResults = self.formatDict(results)
        return formResults