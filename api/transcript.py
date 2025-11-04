import os
import tempfile
import subprocess
import openai
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/transcript')
def transcript():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Missing ?id=VIDEO_ID"}), 400

    # Step 1: try to fetch transcript directly
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify({
            "source": "youtube",
            "transcript": transcript
        })
    except (TranscriptsDisabled, NoTranscriptFound):
        pass  # fallback to Whisper

    # Step 2: fallback - download audio
    try:
        temp_dir = tempfile.mkdtemp()
        audio_path = os.path.join(temp_dir, f"{video_id}.mp3")
        subprocess.run([
            "yt-dlp", "-x", "--audio-format", "mp3",
            f"https://youtu.be/{video_id}", "-o", audio_path
        ], check=True)

        # Step 3: call Whisper API
        with open(audio_path, "rb") as audio_file:
            transcript = openai.Audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json"
            )
        return jsonify({
            "source": "whisper",
            "transcript": transcript["text"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
