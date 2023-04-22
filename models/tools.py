from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS 

from google_drive import GoogleDrive
import io

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

import os
import configparser

config = configparser.ConfigParser()
config.read('config\config.ini')
OPENAI_API_KEY = config.get('openai', 'OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


drive = GoogleDrive()
""" file_id = drive.get_file_by_name('example_file')
if file_id:
    try:
        drive.download_file(file_id, 'example_file.txt')
        print('下載完成')
    except Exception as e:
        print(f'下載失敗: {e}')
else:
    print('下載失敗') """

#drive.list_files()
#drive.about()

folders = drive.list_files_in_all_folders("PDFs") # 拿到所有PDFs文件夾中的文件, 返回文件名和ID的字典



""" file_names = [
    "stablediffusion",
    "webui.sh",
    "launch.py",
    "index",
    "HEAD",
    "paths_internal.cpython-39.pyc",
    "cmd_args.cpython-39.pyc",
    "__pycache__",
    "ORIG_HEAD",
    "FETCH_HEAD",
]

for file_name in file_names:
    drive.get_file_by_name(file_name)
    print() """

#文件ID
file_id = '1Zs2LWiMfrnb-R2yRavPEp06hHsX2EzTI'
file_content = drive.get_file_content(file_id)
file_stream = io.BytesIO(file_content)

# 讀取PDF文件
pdf_reader = PdfReader(file_stream)
print(pdf_reader)

# 提取PDF文件中的文本
raw_text = ""
for i, page in enumerate(pdf_reader.pages):
    text = page.extract_text()
    if text: 
        raw_text += text

#print(raw_text[:1000])

# 分割文本
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function = len,
)

# 分割文本, 返回分割後的文本列表
texts = text_splitter.split_text(raw_text)
#print(len(texts))
#print(texts[20])



# 創建嵌入模型
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
docsearch = FAISS.from_texts(texts, embeddings)

chain = load_qa_chain(OpenAI(), chain_type="stuff")

query = "what is the book title"
docs = docsearch.similarity_search(query)
print(chain)
chain.run(input_documents = docs, question = query)




