from langchain.document_loaders import YoutubeLoader

class YoutubeLoader:
    def __init__(self, video_id):
        self.video_id = video_id
        self.data = None
    
    def load_data(self):
        loader = YoutubeLoader.from_youtube_url(f"https://www.youtube.com/watch?v={self.video_id}", add_video_info=True)
        self.data = loader.load()
        return self.data