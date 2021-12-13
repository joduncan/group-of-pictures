from flask import Flask
from routes.videos_blueprint import videos_blueprint
# from engine import ffmpeg_wrapper

app = Flask(__name__)
app.register_blueprint(videos_blueprint, url_prefix='/videos')

@app.route('/')
def index():
	return f"<html><body>Hi</body></html>"