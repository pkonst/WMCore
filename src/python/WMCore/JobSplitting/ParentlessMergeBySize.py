#!/usr/bin/env python
"""
_ParentlessMergeBySize_

WMBS merging that ignores file parents.
"""
import time
import threading

from WMCore.WMBS.File import File
from WMCore.DataStructs.Run import Run

from WMCore.DAOFactory import DAOFactory
from WMCore.JobSplitting.JobFactory import JobFactory

def fileCompare(a, b):
    """
    _fileCompare_

    Compare two files based on their "file_first_event" attribute.
    """
    if a["file_run"] > b["file_run"]:
        return 1
    elif a["file_run"] == b["file_run"]:
        if a["file_lumi"] > b["file_lumi"]:
            return 1
        elif a["file_lumi"] == b["file_lumi"]:
            if a["file_first_event"] > b["file_first_event"]:
                return 1
            if a["file_first_event"] == b["file_first_event"]:
                return 0

    return -1

class ParentlessMergeBySize(JobFactory):
    def defineFileGroups(self, mergeableFiles):
        """
        _defineFileGroups_

        Group mergeable files by their SE name and run number so that we don't
        try to merge together files on different SEs.  Merging against across
        run boundaries is configurable.
        """
        fileGroups = {}
        foundFiles = []

        for mergeableFile in mergeableFiles:
            if mergeableFile["file_lfn"] not in foundFiles:
                foundFiles.append(mergeableFile["file_lfn"])
            else:
                continue

            if not fileGroups.has_key(mergeableFile["se_name"]):
                if self.mergeAcrossRuns:
                    fileGroups[mergeableFile["se_name"]] = []
                else:
                    fileGroups[mergeableFile["se_name"]] = {}

            if self.mergeAcrossRuns:
                fileGroups[mergeableFile["se_name"]].append(mergeableFile)
            else:
                if not fileGroups[mergeableFile["se_name"]].has_key(mergeableFile["file_run"]):
                    fileGroups[mergeableFile["se_name"]][mergeableFile["file_run"]] = []
                fileGroups[mergeableFile["se_name"]][mergeableFile["file_run"]].append(mergeableFile)

        return fileGroups

    def createMergeJob(self, mergeableFiles):
        """
        _createMergeJob_

        Create a merge job for the given merge units.  All the files contained
        in the merge units will be associated to the job.
        """
        if self.currentGroup == None:
            self.newGroup()

        self.newJob(name = self.getJobName())
        mergeableFiles.sort(fileCompare)

        for file in mergeableFiles:
            newFile = File(id = file["file_id"], lfn = file["file_lfn"],
                           events = file["file_events"])

            # The WMBS data structure puts locations that are passed in through
            # the constructor in the "newlocations" attribute.  We want these to
            # be in the "locations" attribute so that they get picked up by the
            # job submitter.
            newFile["locations"] = set([file["se_name"]])
            newFile.addRun(Run(file["file_run"], file["file_lumi"]))
            self.currentJob.addFile(newFile)

    def defineMergeJobs(self, mergeableFiles):
        """
        _defineMergeJobs_

        Try to define merge jobs that meet the size requirement.
        """
        mergeJobFileSize = 0
        mergeJobEvents   = 0
        mergeJobFiles    = []
        earliestInsert   = 999999999999999

        mergeableFiles.sort(fileCompare)

        for mergeableFile in mergeableFiles:
            if mergeableFile["file_size"] > self.maxMergeSize or \
                   mergeableFile["file_events"] > self.maxMergeEvents:
                self.createMergeJob([mergeableFile])
                continue
            elif mergeableFile["file_size"] + mergeJobFileSize > self.maxMergeSize or \
                     mergeableFile["file_events"] + mergeJobEvents > self.maxMergeEvents:
                if mergeJobFileSize > self.minMergeSize or \
                       self.forceMerge == True or \
                       time.time() - mergeableFile['insert_time'] > self.maxWaitTime:
                    self.createMergeJob(mergeJobFiles)
                    mergeJobFileSize = 0
                    mergeJobEvents = 0
                    mergeJobFiles = []
                else:
                    continue

            mergeJobFiles.append(mergeableFile)
            mergeJobFileSize += mergeableFile["file_size"]
            mergeJobEvents += mergeableFile["file_events"]
            if mergeableFile['insert_time'] < earliestInsert:
                earliestInsert = mergeableFile['insert_time']

        if mergeJobFileSize > self.minMergeSize or self.forceMerge == True or \
               time.time() - earliestInsert > self.maxWaitTime:
            if len(mergeJobFiles) > 0:
                self.createMergeJob(mergeJobFiles)

        return

    def algorithm(self, *args, **kwargs):
        """
        _algorithm_

        Try to merge any available files for the subscription provided.  This
        accepts the following keyword arguments:
          max_merge_size - The maximum size of merged files
          min_merge_size - The minimum size of merged files
          max_merge_events - The maximum number of events in a merge file
          merge_across_runs - Whether or not we merge across runs
        """
        # This doesn't use a proxy
        self.grabByProxy = False

        self.maxMergeSize    = int(kwargs.get("max_merge_size", 1000000000))
        self.minMergeSize    = int(kwargs.get("min_merge_size", 1048576))
        self.maxMergeEvents  = int(kwargs.get("max_merge_events", 50000))
        self.mergeAcrossRuns = kwargs.get("merge_across_runs", True)
        self.maxWaitTime     = kwargs.get("max_wait_time", 12 * 3600)

        self.subscription["fileset"].load()

        if self.subscription["fileset"].open == True:
            self.forceMerge = False
        else:
            self.forceMerge = True

        myThread = threading.currentThread()
        daoFactory = DAOFactory(package = "WMCore.WMBS",
                                logger = myThread.logger,
                                dbinterface = myThread.dbi)

        if self.forceMerge:
            # Check and see if we have an injected workflow
            # If the workflow is not injected, then we can't forceMerge
            getAction = daoFactory(classname = "Workflow.CheckInjectedWorkflow")
            injected  = getAction.execute(name = self.subscription["workflow"].name,
                                          conn = myThread.transaction.conn,
                                          transaction = True)

            if not injected:
                self.forceMerge = False

        mergeDAO       = daoFactory(classname = "Subscriptions.GetFilesForParentlessMerge")
        mergeableFiles = mergeDAO.execute(self.subscription["id"],
                                          conn = myThread.transaction.conn,
                                          transaction = True)

        groupedFiles = self.defineFileGroups(mergeableFiles)

        for seName in groupedFiles.keys():
            if self.mergeAcrossRuns:
                self.defineMergeJobs(groupedFiles[seName])
            else:
                for runNumber in groupedFiles[seName].keys():
                    self.defineMergeJobs(groupedFiles[seName][runNumber])

        return
