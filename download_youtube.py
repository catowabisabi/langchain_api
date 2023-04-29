import pytube
import speech_recognition as sr
import re

id = "XLG-qtZwxIw"

# 指定 YouTube 影片的 URL
url = f'https://www.youtube.com/watch?v={id}'

# 建立 YouTube 物件
yt = pytube.YouTube(url)


id_cleaned = re.sub(r'\W+', '', id)
filename = f"{id_cleaned}.mp4"
print(filename)

# 下载视频的音频
audio = yt.streams.filter(only_audio=True).first()
audio.download('audio_folder', filename=filename)
