from langchain.document_loaders import BSHTMLLoader
import requests

class MyHTMLLoader:
    def __init__(self, html_url="https://www.google.com"):
        self.html_url = html_url
        self.loader = BSHTMLLoader(self.html_url)
 

    def load(self):
        response = requests.get(self.html_url)
        response.raise_for_status()
        return response.text

    def get_html(self):
        self.data = self.loader.load()
        print(self.data)
        return self.data

a = MyHTMLLoader()
a.get_html()
