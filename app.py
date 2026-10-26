from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/get-link', methods=['POST'])
def get_link():
    data = request.json
    video_url = data.get('url')
    
    ydl_opts = {
        'format': 'best/bestvideo+bestaudio/best',  # Sabse best format automatic uthane ke liye
        'cookiefile': 'cookies.txt',
        'noplaylist': True,  # Sirf single video ke liye strict rule
        'extractor_args': {
            'youtube': {'player_client': ['android', 'web']}
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # Direct video download link nikalna
            direct_url = info.get('url')
            if not direct_url and 'entries' in info:
                direct_url = info['entries'][0].get('url')
                
            return jsonify({'status': 'success', 'url': direct_url})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
