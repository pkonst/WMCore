#!/usr/bin/env python
from distutils.core import setup

setup (name='wmcore',
       version='1.0',
       package_dir={'WMCore': 'src/python/WMCore','WMComponent' : 'src/python/WMComponent','WMQuality' : 'src/python/WMQuality'},
       packages=['WMComponent.Proxy.Handler',
                 'WMComponent.Proxy',
                 'WMComponent.ErrorHandler.Database.MySQL',
                 'WMComponent.ErrorHandler.Database',
                 'WMComponent.ErrorHandler',
                 'WMComponent',
                 'WMQuality',
                 'WMCore.MsgService.Oracle',
                 'WMCore.MsgService.MySQL',
                 'WMCore.MsgService',
                 'WMCore.Trigger.Oracle',
                 'WMCore.Trigger.MySQL',
                 'WMCore.Trigger',
                 'WMCore.Alerts.MySQL',
                 'WMCore.Alerts',
                 'WMCore.Agent',
                 'WMCore.Algorithms',
                 'WMCore.JobSplitting',
                 'WMCore.JobStateMachine',                 
                 'WMCore.WMBS.SQLite.Jobs',
                 'WMCore.WMBS.SQLite.Masks',
                 'WMCore.WMBS.SQLite.Workflow',
                 'WMCore.WMBS.SQLite.JobGroup',
                 'WMCore.WMBS.SQLite.Fileset',
                 'WMCore.WMBS.SQLite.Locations',
                 'WMCore.WMBS.SQLite.Files',
                 'WMCore.WMBS.SQLite.Subscriptions',
                 'WMCore.WMBS.SQLite',
                 'WMCore.WMBS.Oracle.Jobs',
                 'WMCore.WMBS.Oracle.Masks',
                 'WMCore.WMBS.Oracle.Workflow',
                 'WMCore.WMBS.Oracle.JobGroup',
                 'WMCore.WMBS.Oracle.Fileset',
                 'WMCore.WMBS.Oracle.Locations',
                 'WMCore.WMBS.Oracle.Files',
                 'WMCore.WMBS.Oracle.Subscriptions',
                 'WMCore.WMBS.Oracle',                 
                 'WMCore.WMBS.Actions.Fileset',
                 'WMCore.WMBS.Actions.Files',
                 'WMCore.WMBS.Actions.Subscriptions',
                 'WMCore.WMBS.Actions',
                 'WMCore.WMBS.WMBSAccountant',
                 'WMCore.WMBS.Oracle',
                 'WMCore.WMBS.WMBSAllocater.Allocaters',
                 'WMCore.WMBS.WMBSAllocater',
                 'WMCore.WMBS.WMBSFeeder.Feeders',
                 'WMCore.WMBS.WMBSFeeder',
                 'WMCore.WMBS.T0AST',
                 'WMCore.WMBS.MySQL.Jobs',
                 'WMCore.WMBS.MySQL.Masks',
                 'WMCore.WMBS.MySQL.Workflow',
                 'WMCore.WMBS.MySQL.JobGroup',
                 'WMCore.WMBS.MySQL.Fileset',
                 'WMCore.WMBS.MySQL.Locations',
                 'WMCore.WMBS.MySQL.Files',
                 'WMCore.WMBS.MySQL.Subscriptions',
                 'WMCore.WMBS.MySQL',
                 'WMCore.WMBS',
                 'WMCore.DataStructs',
                 'WMCore.WMBSFeeder.DBS',
                 'WMCore.WMBSFeeder.PhEDExNotifier',
                 'WMCore.WMBSFeeder.Fake',
                 'WMCore.WMBSFeeder',
                 'WMCore.ThreadPool.MySQL',
                 'WMCore.ThreadPool',
                 'WMCore.Services.SAM',
                 'WMCore.Services.Dashboard',
                 'WMCore.Services.JSONParser',
                 'WMCore.Services.SiteDB',
                 'WMCore.Services',
                 'WMCore.SiteScreening',
                 'WMCore.Database',
                 'WMCore'],)

