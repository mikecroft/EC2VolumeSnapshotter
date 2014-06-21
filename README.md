# EC2VolumeSnapshotter #

This is a simple utility to take snapshots of EC2 volumes and make sure that the number of snapshots doesn't grow.

### What is this repository for? ###

I wrote this mostly as a way for me to learn a bit more about Python. Criticisms/comments/pull requests all welcome.


### Files and usage ###
There are three configuration INI files and 3 python scripts.

* EC2VolumeSnapshotter is the class which does all the work. Create an instance of this to actually do the snapshotting.
To run it once on a volume, it needs to know the:
    * vol_name - Volume name
    * ssMin    - minimum number of snapshots to maintain (i.e. don't delete old snapshots if there aren't this many there)
    * region - the EC2 region, e.g. eu-west-1
* EC2Runner is the script which kicks it all off. It needs a logging.ini (which is used for the standard python logger) to specify how to do logging and a config.ini, which describes the volumes to snapshot and provides the vol_name, ssMin and region for the EC2VolumeSnapshotter
* EmailNotifier uses the details in the emailconf.ini to send an email with the given subject, body and optional attachment.