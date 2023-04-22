from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from llms import LLM_OpenAI, OPENAI_API_KEY

import configparser
import os

config = configparser.ConfigParser()
config.read('config\config.ini')
SERPAPI_API_KEY = config.get('serpapi', 'SERPAPI_API_KEY')
os.environ["SERPAPI_API_KEY"] = SERPAPI_API_KEY



#開agent
llm_openai = LLM_OpenAI(OPENAI_API_KEY)
tools = load_tools(['serpapi', "llm-math"], llm=llm_openai.llm)
agent = initialize_agent(tools, llm=llm_openai.llm, agent="zero-shot-react-description", verbose=True)

#問問題:
agent.run("今日天氣如何? 明天會下雨嗎? 有沒有什麼明天可以做的活動?")