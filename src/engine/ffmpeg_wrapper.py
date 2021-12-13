from pathlib import Path
import subprocess
import json
from tempfile import NamedTemporaryFile

def check_video_file(filename):
	if not filename.endswith('mp4'):
		raise TypeError
	if not Path(filename).is_file():
		raise FileNotFoundError

def frames(filename):
	command = f"ffprobe -show_frames -print_format json {filename}"
	# We're trusting/assuming that this will raise some sort of OS-level exception
	# if the source video file is corrupted or invalid in some other way.
	output = subprocess.check_output(command, shell=True, stderr=None)
	return json.loads(output)['frames']

def iframes(filename):
	check_video_file(filename)
	all_frames = frames(filename)
	return [frame for frame in all_frames if frame['pict_type'] == 'I']
	
# This function employs a bit of a sleight of hand.
# I'm making a named tempfile with python
# but opening it in a binary read/write mode (and don't write to it)
# passing the filename to ffmpeg (with the overwrite flag)
# so that it can write to the file
# (ffmpeg can't write to stdout b/c it needs to seek backwards at times, apparently)
# I then read the contents of the file in python and send them out to the web client.
# when flask finishes reading/sending the last byte, it will close the file
# and python should remove the tempfile without any manual intervention.
# NOTE: this will not work if your flask server somehow spawns external processes
# using a different user id. (due to NamedTemporaryFile() using mkstemp() underneath)
def gop(filename, gop_index):
	check_video_file(filename)
	indexed_iframes = [
		{
			'index': index,
			'frame': frame
		}
		for index, frame in enumerate(frames(filename))
		if frame['pict_type'] == 'I'
		]
	current_iframe = indexed_iframes[gop_index]['frame']
	frames_arg = ""
	# for all but the last gop i-frame, we want to slice only the # of frames
	# between the current i-frame and the next i-frame. for the last i-frame, we
	# start our slice at the i-frame's timestamp and let ffmpeg copy to the end of the video.
	if gop_index < (len(indexed_iframes) - 1):
		frames_arg = f"-frames:v {indexed_iframes[gop_index+1]['index'] - indexed_iframes[gop_index]['index']}"
	# NOTE: The output from ffprobe shows two fields that (as far as I can tell with the sample video)
	# are identical. more research would be needed to determine if/when pkt_pts_time and
	# best_effort_timestamp_time ever deviate. Ditto for if there was ever a DTS stream
	# or timestamps in the video file.
	command = f"ffmpeg -y -ss {current_iframe['pkt_pts_time']} -i {filename} -c:a copy -c:v copy {frames_arg} "
	with NamedTemporaryFile('r+b', suffix='.mp4') as tempfile:
		command += tempfile.name
		ffmpeg_output = subprocess.check_output(command, shell=True, stderr=None)
		return tempfile.read()


# we could either return the # of gops in the video file (length of the iframes list)
# or the actual iframes list, or a list of indices of the iframes in the list.
# 
# while the last option may sound a little silly, I considered it for a minute,
# just so that the controller wouldn't need to enumerate 0..<length of list> if
# I return the length of the list.
#
# I'm not returning the iframes themselves b/c that feels like a lot of info to
# send back to the controller when all we really need to do at that level is
# generate links to the gop slicer url for each group.
def all_gops(filename):
	check_video_file(filename)
	return len(iframes(filename))
