#!/usr/bin/env python
#pylint: disable-msg=W0613
"""
_LumiBased_

Lumi based splitting algorithm that will chop a fileset into
a set of jobs based on lumi sections
"""

__revision__ = "$Id: LumiBased.py,v 1.16 2010/06/18 18:10:22 mnorman Exp $"
__version__  = "$Revision: 1.16 $"

import operator

from WMCore.JobSplitting.JobFactory import JobFactory
from WMCore.DataStructs.Fileset import Fileset
from WMCore.Services.UUID import makeUUID

class LumiBased(JobFactory):
    """
    Split jobs by number of events
    """

    locations = []


    def algorithm(self, *args, **kwargs):
        """
        _algorithm_

        Split files into a number of lumis per job
        Allow a flag to determine if we split files between jobs
        """


        lumisPerJob  = kwargs.get('lumis_per_job', None)
        splitFiles   = kwargs.get('split_files_between_job', False)

        lDict = self.sortByLocation()
        locationDict = {}

        for key in lDict.keys():
            newlist = []
            for f in lDict[key]:
                if hasattr(f, 'loadData'):
                    f.loadData()
                if len(f['runs']) == 0:
                    continue
                f['lowestRun'] = sorted(f['runs'])[0]
                newlist.append(f)
            locationDict[key] = sorted(newlist, key=operator.itemgetter('lowestRun'))




        if splitFiles:
            self.withFileSplitting(lumisPerJob = lumisPerJob,
                                   locationDict = locationDict)
        else:
            self.noFileSplitting(lumisPerJob = lumisPerJob,
                                 locationDict = locationDict)

        return
        

                


    def noFileSplitting(self, lumisPerJob, locationDict):
        """
        Split files into jobs by lumi without splitting files

        Will create jobs with AT LEAST that number of lumis

        if lumisPerJob = 3:
        2 files of 3 lumis each  = 2 jobs
        2 files of 2 lumis each  = 1 job
        2 files of 1 lumi each   = 1 job
        10 files of 1 lumi each  = 4 jobs
        """

        totalJobs    = 0
        for location in locationDict.keys():

            # Create a new jobGroup
            self.newGroup()

            # Start this out high so we immediately create a new job
            lumisInJob  = lumisPerJob + 100

            for f in locationDict[location]:
                fileLength = sum([ len(run) for run in f['runs']])
                if fileLength == 0:
                    # Then we have no lumis
                    # BORING.  Go home
                    continue

                fileRuns = list(f['runs'])
                if lumisInJob >= lumisPerJob:
                    # Then we need to close out this job
                    # And start a new job
                    self.newJob(name = self.getJobName(length=totalJobs))
                    firstRun = fileRuns[0]
                    self.currentJob['mask']['FirstRun']  = firstRun.run
                    self.currentJob['mask']['FirstLumi'] = firstRun.lumis[0]
                    lumisInJob = 0
                    totalJobs += 1


                # Actually add the file to the job
                self.currentJob.addFile(f)
                lumisInJob += fileLength

                
                if lumisInJob >= lumisPerJob:
                    # Write down the ending info from this job
                    # Do not close job until you get the
                    # start info from the next file
                    # This simplifies things
                    lastRun = fileRuns[-1]
                    self.currentJob["mask"]['LastRun']   = lastRun.run
                    self.currentJob["mask"]['LastLumi']  = lastRun.lumis[-1]

        return


    def withFileSplitting(self, lumisPerJob, locationDict):
        """
        Split files into jobs allowing one file to be in multiple jobs

        Creates jobs with EXACTLY lumisPerJob lumis
        """


        totalJobs = 0
        for location in locationDict.keys():

            # Create a new jobGroup
            self.newGroup()

            # Start this out so we immediately create a new job
            lumisInJob  = lumisPerJob

            for f in locationDict[location]:

                if self.currentJob and not lumisInJob == lumisPerJob:
                        # Add a new file to the job
                        # When starting a new file
                        self.currentJob.addFile(f)

                for run in f['runs']:
                    
                    for lumi in run:
                        # Now we're running through lumis
                        
                        if lumisInJob == lumisPerJob:
                            # Then we need to close out this job
                            # And start a new job
                            self.newJob(name = self.getJobName(length=totalJobs))
                            self.currentJob['mask']['FirstRun']  = run.run
                            self.currentJob['mask']['FirstLumi'] = lumi
                            lumisInJob = 0
                            totalJobs += 1

                            # Add the file to new jobs
                            self.currentJob.addFile(f)

                        lumisInJob += 1

                        if lumisInJob == lumisPerJob:
                            # Then this will be closed next round
                            # Set things here
                            self.currentJob["mask"]['LastRun']   = run.run
                            self.currentJob["mask"]['LastLumi']  = lumi

                        


        return

    

