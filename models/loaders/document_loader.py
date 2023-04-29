from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain
#from langchain.document_loaders import PythonLoader
from langchain.document_loaders import DirectoryLoader
from langchain import OpenAI

import configparser
import os

config = configparser.ConfigParser()
config.read('config\config.ini')
OPENAI_API_KEY = config.get('openai', 'OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


file_location = "c:\\Users\\enoma\\Desktop\\Programming\\WB_Trade_Server\\common\\database\\test.txt"
folder_location = "c:\\Users\\enoma\\Desktop\\Programming\\WB_Trade_Server\\common\\database\\db_controller.py"

class DocLoader:
    
    def __init__(self, file_location=file_location, folder_location=folder_location):
        self.file_location = file_location
        self.python_folder_location = folder_location
        self.llm = OpenAI(openai_api_key = OPENAI_API_KEY, temperature=0.9, max_tokens=1000)
        self.docs = []

    def load_doc(self):
        self.doc_loader = UnstructuredFileLoader(self.file_location)
        self.docs = self.doc_loader.load()
        return self.docs

    def load_python(self):
        if not self.docs:
            self.load_doc()
        self.python_loader = DirectoryLoader(self.python_folder_location, glob="**/*.py", loader_cls=PythonLoader)
        self.docs = self.python_loader.load()
        return self.docs

    def summary(self):
        if not self.docs:
            self.load_doc()
        print(f"你有 {len(self.docs)} 個文件")
        num_words = sum([len(doc.page_content.split(' ')) for doc in self.docs])
        print(f"你的文件大約有 {num_words} 個字")
        print()
        #print(f"你的文件是Preview: {self.docs[0].page_content.split('.')[0]}")
        print(f"你的文件是Preview: {self.docs[0].page_content[:50]}")
    
    def load_llm(self):
        if not self.docs:
            self.load_doc()
        
 

#doc = DocLoader() # 可以用黎load python file
#doc.summary()