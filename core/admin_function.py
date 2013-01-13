#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''
# This will contain all the Admin Functions

import os,stat
import sys
import zipfile
from cStringIO import StringIO
import shutil
from time import gmtime, strftime
from config.config import MaildbRoot, reportRoot, DBFile
from db.db import Maildatabase
from core.common import Dictionary	
from core.logging import MaildbLog as MaildbLog
Month = strftime ("%B", gmtime())
Date = strftime ("%d", gmtime())
dir = reportRoot
zip_file = os.path.join(MaildbRoot, "Archive", Month, Date, "Archive.zip")
db = Maildatabase()


class adFunction:


    def __init__(path): # Set the Backup

        global backupDir
        backupDir = os.path.join(MaildbRoot, "Archive", Month, Date)
        if not os.path.exists(backupDir):
            os.makedirs(backupDir)
	    
    def copydb():
		db.conn.close()
		src = DBFile
		dst = os.path.join(backupDir, "Backup.db")
		shutil.copyfile(src, dst)	        
	                
    def archive(self):
		db.conn.close()
		shutil.copyfile(DBFile, os.path.join(backupDir, "Backup.db"))
		zip = zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED)
		root_len = len(os.path.abspath(dir))
		for root, dirs, files in os.walk(dir):
			archive_root = os.path.abspath(root)[root_len:]	
			for f in files:
				fullpath = os.path.join(root, f)
				archive_name = os.path.join(archive_root, f)
				zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
		zip.close()
		log = "##INFO##, Full Backup Created"
		MaildbLog().logEntry(log)
		return zip_file	

    def reset(self):
		db.conn.close()
		os.remove(DBFile)
		shutil.rmtree(reportRoot)
		if not os.path.exists(reportRoot):
			os.mkdir(reportRoot)
		if not os.path.exists(os.path.join(MaildbRoot, "tmp")):
			os.mkdir(os.path.join(MaildbRoot, "tmp"))
		from db.db import Maildatabase
		Maildatabase().generate()
        
    def restore(self, dir):
        # submit a zip file and a db file then extarct and copy in to place
        pass        
        
	def setup(self):
		# Setup up after a clear or initial install
		if not os.path.exists(reportRoot):
			os.mkdir(reportRoot)
			
		if not os.path.exists(os.path.join(MaildbRoot, "tmp")):
			os.mkdir(os.path.join(MaildbRoot, "tmp"))
			
		## Setup The Tables ###
		
		from db.db import Maildatabase
		Maildatabase().generate()				       


class recordTools:
		
	def exportDir(self, msg_id, fileID):
		print "runnign Export"
		if fileID:
			msgDir = os.path.join(MaildbRoot, "store", msg_id, "sites", fileID)
		else:
			msgDir = os.path.join(MaildbRoot, "store", msg_id)
		exp_file = os.path.join(MaildbRoot, "web", "static", "Export.zip")
		zip = zipfile.ZipFile(exp_file, 'w', compression=zipfile.ZIP_DEFLATED)
		root_len = len(os.path.abspath(msgDir))
		for root, dirs, files in os.walk(msgDir):
			archive_root = os.path.abspath(root)[root_len:]
			for f in files:
				fullpath = os.path.join(root, f)
				archive_name = os.path.join(archive_root, f)
				zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
		zip.close()
		log = "##INFO##, File Export Created for " + msg_id
		MaildbLog().logEntry(log)
		return exp_file


	def removeRecord(self, msg_id):
		# put a check here to see if record exists
		db.delRecord(msg_id)
		pathRemove = os.path.join(reportRoot, msg_id)
		if os.path.exists(pathRemove):
			shutil.rmtree(pathRemove)

