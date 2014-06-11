#!/usr/bin/python
##############################################################################

import subprocess
import os
import datetime
import sys
import logging
import logging.config

class EC2VolumeSnapshotter:

	ec2_home = ""
	path = ""
	java_home = ""
	region = 'eu-west-1'
	aws_access_key = ""
	aws_secret_key = ""
	logger = logging.getLogger(__name__)
	

	#vol_name = ""

	def __init__(self, ec2_home, 
				 path, java_home, region,
				 aws_access_key, aws_secret_key):
		self.ec2_home = ec2_home
		self.path = path
		self.java_home = java_home
		self.region = region
		self.aws_access_key = aws_access_key
		self.aws_secret_key = aws_secret_key
		logging.config.fileConfig('logging.ini', disable_existing_loggers=False)


	def runSnapshotter(vol_name):
		# verify vol_name is valid
		# logger.info("Validating volume" + vol_name)
		if (not isVolNameValid(vol_name)):
			# TODO handle exception and log
			raise Exception(
				  "I can't find that volume name. "
				+ "Is the name correct? "
				+ "Is the correct region set?").with_traceback(tracebackobj)

		# create new snapshot
		if (not createSnapshot(vol_name)):
			# TODO handle exception and log
			raise Exception(
				  "Could not create snapshot. Exiting.").with_traceback(tracebackobj)
			#sys.exit()

		# if there are not > 7 (1 week) snapshots, abort
		if (countSnapshots(listSnapShots(vol_name) > 7)):
			# find earliest snapshot and delete
			deleteSnapshot(
				findEarliest(
					listSnapShots(vol_name)))
		else:
			self.logger.warn("Not enough snapshots existed. There are currently " +
				countSnapshots(listSnapShots(vol_name)))


	def isVolNameValid(self, vol_name):
		''' Uses ec2dvol to get a list of all volume
			names in given region then checks to see
			if vol_name is in the list
		'''

		vol_error = "Client.InvalidVolume.NotFound: The volume '" + vol_name + "' does not exist."

		vTest = subprocess.Popen(
			['ec2dvol', '--region', self.region, vol_name],
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = vTest.communicate()

		if (out != vol_error and err == ""):
			self.logger.info("The volume appears to be valid.\n" + out)
			return True
		elif (out == vol_error and err == ""):
			# TODO fix comparison so it only compares the first part of vol_error
			self.logger.error("Could not find volume. AWS returned: " + out)
			return False
		self.logger.critical("An unexpected error occurred: " + err)
		# TODO raise exception
		return False


	def createSnapshot(self, vol_name):
		''' Uses ec2addsnap to create a snapshot from
			the given volume name
		'''
		addSnap = subprocess.Popen(
			['ec2addsnap', '--region', self.region, vol_name],
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = addSnap.communicate()

		if (err == ""):
			self.logger.info("Created snapshot:\n" + out)
			return True
		self.logger.error("Could not create snapshot. AWS returned stderr: " + err)
		return False


	def listSnapshots(self, vol_name):
		''' Uses ec2dsnap to list all the snapshots for
			the given volume name.

			Returns a list of lists (2d array) or snapshots
			like [[snap, timestamp],...[snapN, timestampN]]
		'''

		describe = subprocess.Popen(
			['ec2dsnap', '--region', self.region, '-F', 'volume-id=' + vol_name],
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = describe.communicate()

		self.logger.info("For volume " +
			vol_name + " found the following snapshots:\n" + out)

		lines = filter(None, out.splitlines())

		snaps = []
		for line in lines:
			words = line.split()
			snaps.append([words[1], words[4]])

		return snaps


	def countSnapshots(self, snapshots):
		return number

	def findEarliest(self, snapshots):

		return ss


	def deleteSnapshot(self, ss):
		return False















