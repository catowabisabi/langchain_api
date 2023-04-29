
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain

from llms import LLM_OpenAI
from loaders.document_loader import DocLoader
from prompts.prompt_templates import prompt_zh_points_and_summary
from database.fake_data import fake_news1, fake_news2


from llms import OPENAI_API_KEY
from loaders.pdf_loader import PDFLoader
#from loaders.document_loader import doc




class PointAndSummaryChain:
    def __init__(self, text = fake_news1):
        self.llm_openai      = LLM_OpenAI(OPENAI_API_KEY, temperature=0.9)
        self.prompt = prompt_zh_points_and_summary
        self.chain = LLMChain(llm=self.llm_openai.llm, prompt=self.prompt)


    def run(self, text):
        response = self.chain.run(text)
        print(response)
        return response
        


#===================================================================================================
class LoadSummizeChain:
    def __init__(self, chain_type='map_reduce', verbose=True):
        self.llm_openai = OpenAI(openai_api_key= OPENAI_API_KEY, temperature=0.9)
        self.chain_type = chain_type
        self.verbose = verbose
        self.chain = load_summarize_chain(self.llm_openai.llm, chain_type=self.chain_type, verbose=self.verbose)

    def run(self, text):
        response = self.chain.run(text)
        print(response)
        return response



# load doc, 一般黎講要比返個url or link
#doc_loader= DocLoader()
#docs = doc_loader.load_doc()

#response = chain.run(docs)
#print (response)

class SplitDoc:
    def __init__(self, chunk_size=2000, chunk_overlap=0, text_location = "c:\\Users\\enoma\\Desktop\\test.docx"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_location = text_location
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
    
    def load_doc(self):
        self.doc_loader= DocLoader(self.text_location)
        self.docs = self.doc_loader.load_doc()
        print(f"你有 {len(self.docs)} 個文件")
        return self.docs

    def split_doc(self, docs):
        if docs == None:
            self.docs = self.load_doc()
        chunks = self.text_splitter.split_documents(docs)
        print(f"你有 {len(chunks)} 個chunks")
        return chunks


    def summary(self):
        print(f"你有 {len(self.docs)} 個文件")
        num_words = sum([len(doc.page_content.split(' ')) for doc in self.docs])
        print(f"你的文件大約有 {num_words} 個字")
        print()
        #print(f"你的文件是Preview: {self.docs[0].page_content.split('.')[0]}")
        print(f"你的文件是Preview: {self.docs[0].page_content[:100]}")
    
#summary(chunks)

#用返上邊既class
#chain = load_summarize_chain(llm, chain_type='map_reduce', verbose=True)
#response = chain.run(chunks)
#print (response)

class MyPDFLoader:
    def __init__(self, pdf_location="example_data/layout-parser-paper.pdf") -> None:
        self.pdf_loader = PDFLoader(pdf_location)
        
        self.pages =  self.pdf_loader.load_and_split()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=0,
        )
    
    def print_page_1(self):
        print(self.pages[0])
    
    def print_len(self):
        print(len(self.pages))

#pdf_loader = PDFLoader(pdf_location="c:\\Users\\enoma\\Downloads\\Treviranus_Value_2010.pdf")
#pdf_loader.print_page_1()
#pdf_loader.print_len()

    def split_doc(self, docs):
        if docs == None:
            self.docs = self.load_doc()
        self.chunks = self.text_splitter.split_documents(docs)
        print(f"你有 {len(self.chunks)} 個chunks")
        return self.chunks

    def run(self):
        self.chunks.run(self.text)
        return self.chunks


class QNAChain:
    def __init__(self,  input_documents, chain_type = "map_reduce", verbose = True, return_intemediate_step = True, return_only_outputs = True):
        self.input_documents               = input_documents
        self.return_only_outputs     = return_only_outputs
        self.llm_openai              = LLM_OpenAI(OPENAI_API_KEY)
        self.prompt                  = prompt_zh_points_and_summary
        self.chain_type              = chain_type
        self.verbose                 = verbose
        self.return_intemediate_step = return_intemediate_step
        self.chain                   = load_qa_chain(llm=self.llm_openai.llm, chain_type=self.chain_type, verbose=self.verbose)

    def ask(self, question = "hi"):
        response = self.chain({"input_documents": self.input_documents, "question": question}, return_only_outputs=self.return_only_outputs)
        print(response)
        return response



question = """
請用繁體中文回答以下問題:
這新聞的重點是什麼?
有沒有什麼重要的資訊?
有沒有什麼解決方案?

我想以這文章為基礎，寫一篇新的繁體中文的文章，你有什麼建議?
給我個大綱, 要有五個重點，你可以幫我寫一篇新的文章嗎?

以你給我的大網, 寫一篇新的文章, 每個段落要有至少兩個重點, 每個段落在50中文字以上。
"""
#print (fake_news1)

doc_loader = DocLoader()
docs = doc_loader.load_doc()
#print(docs[0])

""" doc_dict = {
    'page_content': docs[0].page_content,
    'metadata': docs[0].metadata
} """

qa_chain = QNAChain(input_documents = docs)
answer = qa_chain.ask(question = question)

while True:
    question = input("請問你有什麼其他問題? (輸入exit離開))")
    answer = qa_chain.ask(question = f"請以繁體中文回答以下問題: ({question})")
    print(answer)
    print()
    print()
    print()
    print()
    if question.lower() == "exit":
        break





