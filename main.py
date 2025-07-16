from flask import Flask, request, send_file
import yt_dlp, subprocess, os, uuid

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h3>YouTube Trimmer</h3>
    <form method="post" action="/trim">
      YouTube Link: <input name="url" required><br>
      Start Time (e.g., 00:00:05): <input name="start" required><br>
      End Time (e.g., 00:00:20): <input name="end" required><br>
      <button type="submit">Trim & Download</button>
    </form>
    '''

@app.route('/trim', methods=['POST'])
def trim():
    url = request.form['url']
    start = request.form['start']
    end = request.form['end']
    vid_id = str(uuid.uuid4())
    in_file = f"{vid_id}.mp4"
    out_file = f"trimmed_{vid_id}.mp4"

    with yt_dlp.YoutubeDL({'outtmpl': in_file}) as ydl:
        ydl.download([url])

    subprocess.run([
        "ffmpeg", "-i", in_file, "-ss", start,
        "-to", end, "-c", "copy", out_file, "-y"
    ])
    os.remove(in_file)
    return send_file(out_file, as_attachment=True)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

