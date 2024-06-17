import os
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# 替換成你本地的影片文件路徑
VIDEO_PATH = "video.mp4"  # 替換為你的影片文件路徑
VIDEO_PATH_2 = "video.mp4"
VIDEO_PATH_3 = "video.mp4"

@app.route('/')
def home():
    # 渲染 index.html 模板
    return render_template('index.html')

@app.route('/play-video', methods=['GET'])
def play_video():
    try:
        # 使用 VLC 播放器播放影片，並設置全屏模式
        if os.name == 'nt':  # Windows
            vlc_path = 'C:/Program Files/VideoLAN/VLC/vlc.exe'  # VLC 的安裝路徑，請確認安裝位置
            os.system(f'"{vlc_path}" "{VIDEO_PATH}" --fullscreen --play-and-exit')
        elif os.name == 'posix':  # macOS, Linux
            os.system(f'vlc "{VIDEO_PATH}" --fullscreen --play-and-exit')
        return jsonify({'status': 'success', 'message': '影片已播放'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/play-video-2', methods=['GET'])
def play_video_2():
    try:
        # 使用 VLC 播放器播放影片，並設置全屏模式
        if os.name == 'nt':  # Windows
            vlc_path = 'C:/Program Files/VideoLAN/VLC/vlc.exe'  # VLC 的安裝路徑，請確認安裝位置
            os.system(f'"{vlc_path}" "{VIDEO_PATH}" --fullscreen --play-and-exit')
        elif os.name == 'posix':  # macOS, Linux
            os.system(f'vlc "{VIDEO_PATH_2}" --fullscreen --play-and-exit')
        return jsonify({'status': 'success', 'message': '影片已播放'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/play-video-3', methods=['GET'])
def play_video_3():
    try:
        # 使用 VLC 播放器播放影片，並設置全屏模式
        if os.name == 'nt':  # Windows
            vlc_path = 'C:/Program Files/VideoLAN/VLC/vlc.exe'  # VLC 的安裝路徑，請確認安裝位置
            os.system(f'"{vlc_path}" "{VIDEO_PATH}" --fullscreen --play-and-exit')
        elif os.name == 'posix':  # macOS, Linux
            os.system(f'vlc "{VIDEO_PATH_3}" --fullscreen --play-and-exit')
        return jsonify({'status': 'success', 'message': '影片已播放'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
