
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
import tokenize

class PythonLoader(TextLoader):
    """
    Load Python files, respecting any non-default encoding if specified.
    """

    def __init__(self, file_path: str):
        with open(file_path, "rb") as f:
            encoding, _ = tokenize.detect_encoding(f.readline)
        super().__init__(file_path=file_path, encoding=encoding)

path = "c:\\Users\\enoma\\Desktop\\Programming\\WB_Trade_Server"

class MyPyDirLoader:
    def __init__(self, path: str):
        self.path = path
        
        self.loader = DirectoryLoader(path=path, glob="**/*.py", loader_cls=PythonLoader)
        self.docs = self.loader.load()

    def summary(self):
        print("...")
        print(f"Loaded {len(self.docs)} documents from {self.path}")
        print("...")
    
    def print_content(self):
        if self.docs:
            print(self.docs[0].page_content)
            #for doc in self.docs:
            #    print(doc.page_content)
    
    def get_content(self, ):
        return self.docs[0].page_content

#py_loader = MyPyDirLoader(path=path)
#py_loader.summary()
#py_loader.print_content()