import subprocess
import os

SYRO_SUBDIR_NAME = "syrodata"
SYRO_DATA_PREFIX = "syrodata_"
# Uncomment/comment as appropriate
#SYRO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/bin/syro-mac") #OSX
SYRO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/bin/syro-raspi") #RasPi
SYRO_EXEC = "syro_volcasample_example"
# AUDIO_PLAYER_EXEC = "afplay" # OSX
AUDIO_PLAYER_EXEC = "aplay"

def afplay(filename):
	"""
	Play a file via the audio out of the server 
	"""
	cmd = [AUDIO_PLAYER_EXEC,filename]
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	out,err = p.communicate()
	return out

def syroconvert(filename, slot_number):
	"""
	Create a syro-encoded wav file.
	"""
	print "Syroconvert"

	print filename

	source_file = filename

	# define the output file for syroconvert
	syrostream_file = os.path.join(os.path.dirname(source_file), SYRO_SUBDIR_NAME, (SYRO_DATA_PREFIX + os.path.basename(filename)))
	print syrostream_file

	# create a folder at the path of the file
	create_syro_subdir = os.path.join(os.path.dirname(source_file), SYRO_SUBDIR_NAME)

	# check it doesn't exist first
	if not os.path.exists(create_syro_subdir):
		os.mkdir(create_syro_subdir)

	# format the command passed to the syro command line utility
	syrocmd = "s%sc:%s" %(str(slot_number), source_file)

	cmd = [os.path.join(SYRO_PATH, SYRO_EXEC),syrostream_file,syrocmd]

	print cmd
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	out,err = p.communicate()
	out
	return syrostream_file

def syroplay(filename):
	"""
	Play a file via the audio out of the server, take the path of the source file and open the syro-encoded output
	"""
	
	# work out the location of the encoded file from the source file
	syrostream_file = os.path.join(os.path.dirname(filename), SYRO_SUBDIR_NAME, (SYRO_DATA_PREFIX + os.path.basename(filename)))
	
	cmd = [AUDIO_PLAYER_EXEC, syrostream_file]
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	out,err = p.communicate()
	return out
	

