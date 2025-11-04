from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/transcript')
def get_transcript():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Missing ?id=VIDEO_ID"}), 400
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify(transcript)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel entrypoint
def handler(request, response):
    with app.request_context(request.environ):
        return app.full_dispatch_request()
