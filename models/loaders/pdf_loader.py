from langchain.document_loaders import PyPDFLoader




class PDFLoader:
    def __init__(self, pdf_location="example_data/layout-parser-paper.pdf") -> None:
        self.pdf_loader = PyPDFLoader(pdf_location)
        self.pages =  self.pdf_loader.load_and_split()
    
    def print_page_1(self):
        print(self.pages[11])
    
    def print_len(self):
        print(len(self.pages))

    def load_and_split(self):
        return self.pdf_loader.load_and_split()

