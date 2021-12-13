import json
from flask import Response, request, abort
from engine import ffmpeg_wrapper

def iframes(video_file):
	try:
		response = Response(json.dumps(ffmpeg_wrapper.iframes(video_file)))
		response.headers['Content-Type'] = 'application/json'
		return response
	except FileNotFoundError:
		abort(404)

def gop(video_file, group_index):
	try:
		response = Response(ffmpeg_wrapper.gop(video_file, group_index))
		response.headers['Content-Type'] = 'video/mp4'
		return response
	except FileNotFoundError:
		abort(404)


def all_gops(video_file):
	try:
		total_gops = ffmpeg_wrapper.all_gops(video_file)
		video_elems = [
			(
				'<video controls width="250" style="margin: 10px">'
				f'<source src={request.path}/{vid_index}.mp4 type="video/mp4">'
				'</video>'
			)
			for vid_index in range(total_gops)
		]
		# please excuse this super-basic markup.
		return f'<html><body><div style="margin: 10px">{"".join(video_elems)}</div></body></html>'
	except FileNotFoundError:
		abort(404)