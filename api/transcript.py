from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/transcript')
def transcript():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Missing ?id=VIDEO_ID"}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify(transcript)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---- 核心修改点 ----
# ✅ Vercel 会直接调用名为 "app" 的 Flask 实例，不需要 handler()
# ✅ 因此只保留 app 即可，不要定义 handler()
if __name__ == "__main__":
    app.run()
