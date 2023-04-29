import json
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
import re
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from models.llms import LLM_OpenAI
import csv
import pandas as pd
import openpyxl
# 在文件開頭添加以下引入
from google.cloud import speech_v1p1beta1 as speech
import io
import youtube_dl
from collections import OrderedDict

from pytube import YouTube


filename = ""
def write_to_csv(data_list, filename):
    keys = data_list[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for data in data_list:
            writer.writerow(data)

def write_to_excel(data_list, filename):
    try:
        if not os.path.exists(filename):
            # 創建 Excel 文件和工作表
            writer = pd.ExcelWriter(filename, engine='openpyxl', mode="a")
            df = pd.DataFrame(columns=['Title', 'Summary', 'Dialogue'])
            df.to_excel(writer, index=False)
            writer.save()

        # 讀取現有的數據
        df = pd.read_excel(filename, engine='openpyxl')

        # 將摘要添加到 DataFrame 中
        summary = data_list.pop('Summary')
        data_list['Summary'] = summary

        # 插入新行
        df.loc[len(df)] = data_list.values()

        # 寫入 Excel 文件
        writer = pd.ExcelWriter(filename, engine='openpyxl')
        df.to_excel(writer, index=False, mode="a")
        writer.save()
    except Exception as e:
        print("Error writing to Excel file." + str(e))



# 添加下載音頻的函數
def download_youtube_audio(video_id):#"XLG-qtZwxIw"  tFsUuvlYyqE
    print("Downloading audio file...")
    id_cleaned = re.sub(r'\W+', '', video_id)
    filename = f"{id_cleaned}.mp4"  # pytube 下載的音頻文件將為 mp4 格式
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    # 建立 YouTube 物件
    yt = YouTube(url)

    try:
        # 選擇最高品質的音頻
        audio = yt.streams.filter(only_audio=True).first()
        audio = audio.download(output_path='audio_folder', filename=filename)
        print("Finished downloading audio file.")
        return audio
    except Exception as e:
        print("Error downloading audio file." + str(e))
        audio = None
        return audio
    
    

# 添加將音頻轉換為文字的函數
def transcribe_audio_file(file_path):
    try:
        print("Transcribing audio file...")
        client = speech.SpeechClient()

        with io.open(file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="zh-TW",
        )

        response = client.recognize(config=config, audio=audio)

        transcript = ''
        for result in response.results:
            transcript += result.alternatives[0].transcript
        print("Finished transcribing audio file.")
        return transcript
    except Exception as e:
        print("Error transcribing audio file." + str(e))
        transcript = None
        return transcript

# 從 YouTube 影片 ID 取得字幕

def get_youtube_video_captions(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string.replace(" - YouTube", "")

    dialogue = ''
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en', 'zh-Hans'])

        for caption in transcript.fetch():
            text = caption['text']
            dialogue += text.strip() + ', '

    except:
        print("Failed to retrieve captions, using Speech-to-Text API instead.")
        audio_file = download_youtube_audio(video_id)
        dialogue = transcribe_audio_file(audio_file)

    if dialogue:
        try:
            data = {
                'title': title,
                'summary': '',
                'dialogue': dialogue[:-2]
            }

            script_dir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.join(script_dir, "dl_captions")
            if not os.path.exists(directory):
                os.makedirs(directory)

            filename = re.sub(r'[^a-zA-Z0-9一-龥]+', '_', title)

            with open(os.path.join(directory, f'{filename}.json'), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                print('Captions saved as captions.json.')
                return data, filename
        except Exception as e:
            print("Error saving captions." + str(e))
            return None, None
    else:
        print("Error retrieving captions.")
        return None, None


video_id = input('Enter YouTube video ID: ')
video_captions, filename = get_youtube_video_captions(video_id)

if filename and video_captions:
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dl_captions")

    openai = LLM_OpenAI()
    try:
        summary = openai.summarize_youtube_video(video_captions)
        summary_tech = openai.text_to_zh(video_captions)

        print(f"Title: {video_captions['title']}")
        print(f"GPT: {summary}")
        print(f"GPT Tech Sum: {summary_tech}")

        if summary:
            # 将摘要添加到 JSON 数据中
            video_captions['summary'] = summary
            

            # 将摘要添加到标题后面
            ordered_video_captions = OrderedDict()
            ordered_video_captions['title'] = video_captions['title']
            ordered_video_captions['summary'] = summary
            ordered_video_captions['dialogue'] = video_captions['dialogue']

            # 将修改后的数据保存到原有的 JSON 文件中
            with open(os.path.join(directory, f'{filename}.json'), 'w', encoding='utf-8') as f:
                json.dump(ordered_video_captions, f, ensure_ascii=False, indent=2)

             # 把数据写入 caption_summarys.xlsx
            excel_filename = 'caption_summarys.xlsx'
            if not os.path.exists(excel_filename):
                write_to_excel(video_captions, 'caption_summarys.xlsx')
            else:
                with pd.ExcelWriter(excel_filename, engine='openpyxl', mode='a') as writer:
                    df = pd.DataFrame(video_captions, index=[0])
                    df.to_excel(writer, sheet_name='caption_summarys', index=False, header=False)
            
            #while True:

             #   question = input("Ask a question about the video: ")
             #   ans = openai.answer_question(question, video_captions['summary'])
              #  if question.lower() == 'exit':
             #       break

    except Exception as e:
        print("Failed to summarize video. Error: ", e)
