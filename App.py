from flask import Flask, request, jsonify
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        url = request.form.get('url')
        if not url:
            return jsonify({'error': 'لینک یوتیوب ارائه نشده است'}), 400

        yt = YouTube(url)
        title = yt.title or 'عنوان نامشخص'
        thumbnail = yt.thumbnail_url or 'https://i.imgur.com/JpkuIu9.png'
        duration = yt.length or 0
        channel = yt.author or 'کانال نامشخص'
        views = yt.views or 0
        date = yt.publish_date.strftime('%Y/%m/%d') if yt.publish_date else 'نامشخص'
        description = yt.description or 'بدون توضیحات'

        # لینک‌های ویدیویی
        video_streams = yt.streams.filter(progressive=True, file_extension='mp4')
        video_links = [
            {
                'quality': stream.resolution,
                'size': f'{stream.filesize / (1024 * 1024):.2f} MB',
                'url': stream.url
            } for stream in video_streams
        ]

        # لینک‌های صوتی
        audio_streams = yt.streams.filter(only_audio=True, file_extension='mp4')
        audio_links = [
            {
                'quality': stream.abr or 'Unknown',
                'size': f'{stream.filesize / (1024 * 1024):.2f} MB',
                'url': stream.url
            } for stream in audio_streams
        ]

        return jsonify({
            'title': title,
            'thumbnail': thumbnail,
            'duration': f'{duration // 60}:{duration % 60:02d}',
            'channel': channel,
            'subscribers': 'نامشخص',
            'views': f'{views:,}',
            'date': date,
            'description': description,
            'videoLinks': video_links,
            'audioLinks': audio_links
        })

    except Exception as e:
        return jsonify({'error': f'خطا: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
