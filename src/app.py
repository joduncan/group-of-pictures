from flask import Flask
from routes.videos_blueprint import videos_blueprint

app = Flask(__name__)
app.register_blueprint(videos_blueprint, url_prefix='/videos')

@app.route('/')
def index():
	return f"<html><body>Hi</body></html>"