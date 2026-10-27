from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/get-link', methods=['POST'])
def get_link():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'status': 'error', 'message': 'URL missing'})
        
    video_url = data.get('url')
    
    # Android client use karne se n-challenge aur format error bypass ho jata hai
    ydl_opts = {
        'format': 'best',
        'cookiefile': 'cookies.txt',                       
        'noplaylist': True,                                
        'extractor_args': {
            'youtube': {'player_client': ['android']}
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_url = info.get('url')
            
            if not direct_url and 'entries' in info and len(info['entries']) > 0:
                direct_url = info['entries'][0].get('url')
                
            if not direct_url:
                direct_url = info.get('webpage_url')
                
            return jsonify({'status': 'success', 'url': direct_url})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
