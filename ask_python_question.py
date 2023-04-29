from models.loaders.directory_loader import MyPyDirLoader
from langchain.agents import load_tools, initialize_agent
from models.llms import LLM_OpenAI, OPENAI_API_KEY
import configparser
import os

config = configparser.ConfigParser()
config.read('config\config.ini')
SERPAPI_API_KEY = config.get('serpapi', 'SERPAPI_API_KEY')
os.environ["SERPAPI_API_KEY"] = SERPAPI_API_KEY


llm_loader = LLM_OpenAI(OPENAI_API_KEY)
llm = llm_loader.llm


#======================================load python files
#定義一個資料夾給loader
folder_path = "c:/Users/enoma/Desktop/Programming/AI/langchain_api/docs/python/001/"

#定義一個loader
py_loader = MyPyDirLoader(path=folder_path)
py_loader.summary()


#======================================建立一個agent, 這個agent可以search, 也可以回答問題
tools = load_tools(['serpapi', "llm-math"], llm=llm)
agent = initialize_agent(tools, llm=llm, agent="zero-shot-react-description", verbose=True)
#agent.run("請使用中文回答: 今日天氣如何? 明天會下雨嗎? 有沒有什麼明天可以做的活動?")
