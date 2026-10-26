from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/get-link', methods=['POST'])
def get_link():
    data = request.json
    video_url = data.get('url')
    
    ydl_opts = {'format': 'best'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_url = info.get('url')
            return jsonify({'status': 'success', 'url': direct_url})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

