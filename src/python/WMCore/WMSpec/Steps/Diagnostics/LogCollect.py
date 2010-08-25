#!/usr/bin/env python
"""
_LogCollect_

Diagnostic implementation for a job's LogCollect step


"""

__revision__ = "$Id: LogCollect.py,v 1.1 2010/05/05 21:06:07 mnorman Exp $"
__version__ = "$Revision: 1.1 $"

import os
from WMCore.WMSpec.Steps.Diagnostic import Diagnostic, DiagnosticHandler


class LCExceptionHandler(DiagnosticHandler):
    """
    _LCExceptionHandler_

    Generic handler for the LogCollect step

    I have no idea what this should do

    """
    def __call__(self, errCode, executor, **args):
        """
        _operator()_

        Twiddle thumbs, contemplate navel, toss coin

        """
        jobRepXml = os.path.join(executor.step.builder.workingDir,
                                 executor.step.output.jobReport)

        if not os.path.exists(jobRepXml):
            # no report => Error
            msg = "No Job Report Found: %s" % jobRepXml
            executor.report.addError(50115, "MissingJobReport", msg)
            return
        
        # job report XML exists, load the exception information from it
        executor.report.parse(jobRepXml)
        
        
        # make sure the report has the error in it
        errSection = getattr(executor.report.report, "errors", None)
        if errSection == None:
            msg = "Job Report contains no error report, but StageOutManager exited non-zero: %s" % errCode
            executor.report.addError(50116, "MissingErrorReport", msg)
            return

        else:
            #check exit code in report is non zero
            if executor.report.report.status == 0:
                msg = "Job Report contains no error report, but StageOutManager exited non-zero: %s" % errCode
                executor.report.addError(50116, "MissingErrorReport", msg)
        return

class LogCollect(Diagnostic):

    def __init__(self):
        Diagnostic.__init__(self)


        catchAll = LCExceptionHandler()
        [ self.handlers.__setitem__(x, catchAll) for x in range(0, 255) if not self.handlers.has_key(x) ]
