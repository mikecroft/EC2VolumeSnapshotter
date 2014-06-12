#!/usr/bin/python
##############################################################################

import subprocess
import os
import datetime
import sys
import logging
import logging.config

class EC2VolumeSnapshotter:

	region = 'eu-west-1'
	logger = logging.getLogger(__name__)
	

	#vol_name = ""

	def __init__(self, region):
		self.region = region
		logging.config.fileConfig('logging.ini', disable_existing_loggers=False)


	def runSnapshotter(self, vol_name):
		# verify vol_name is valid
		# self.logger.info("Validating volume" + vol_name)
		if (not self.isVolNameValid(vol_name)):
			# TODO handle exception and log
			raise Exception(
				  "I can't find that volume name. "
				+ "Is the name correct? "
				+ "Is the correct region set?").with_traceback(tracebackobj)

		# create new snapshot
		if (not self.createSnapshot(vol_name)):
			# TODO handle exception and log
			raise Exception(
				  "Could not create snapshot. Exiting.").with_traceback(tracebackobj)
			#sys.exit()

		snaps = self.listSnapshots(vol_name)

		# if there are not > 7 (1 week) snapshots, abort
		if (len(snaps) > 7):
			# find earliest snapshot and delete
			self.deleteSnapshot(
				self.findEarliest(snaps))
		else:
			self.logger.warn("Not enough snapshots existed. There are currently " +
				str(len(snaps)))


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

		# TODO: Handle snapshots with names (names print on a new line)

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
		# TODO This function is unneccessary. Should delete.
		return len(snapshots)

	def findEarliest(self, snapshots):
		''' Given a list of snapshot IDs and
			their timestamps, finds the oldest
			and returns the ID of the snapshot
		'''
		dates = []
		for snap in snapshots:
			dates.append(snap[1])

		for snap in snapshots:
			if (snap[1] == min(dates)):
				ss = snap [0]
		self.logger.info("The earliest snapshot is: " + ss)
		return ss


	def deleteSnapshot(self, ss):

		self.logger.info("About to delete snapshot: " + ss)
		delete = subprocess.Popen(
			['ec2delsnap', ss, '--region', self.region],
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = delete.communicate()

		return False

	def findSnapshot(self, ss):
		# TODO make sure new snapshot is completed
		return False
