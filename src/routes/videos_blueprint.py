from flask import Blueprint
from controllers.videos_controller import iframes, gop, all_gops

videos_blueprint = Blueprint('videos_blueprint', __name__)

videos_blueprint.route('/<video_file>/group-of-pictures.json', methods=['GET'])(iframes)
videos_blueprint.route('/<video_file>/group-of-pictures/<int:group_index>.mp4', methods=['GET'])(gop)
videos_blueprint.route('/<video_file>/group-of-pictures', methods=['GET'])(all_gops)
