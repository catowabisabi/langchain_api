from langchain.llms import OpenAI
import configparser
import os
config = configparser.ConfigParser()

config.read('config\config.ini')
OPENAI_API_KEY = config.get('openai', 'OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

class LLM_OpenAI:
    def __init__(self, OPENAI_API_KEY=OPENAI_API_KEY, temperature=0.5, max_tokens=2000):
        self.llm = OpenAI(openai_api_key = OPENAI_API_KEY, temperature=temperature, max_tokens=max_tokens)
    
    def get_llm_anwser(self, quesiton):

        text = quesiton
        reply = self.llm(text)
        print(reply)

llm = LLM_OpenAI()
llm.get_llm_anwser("我住多倫多, 幫我找一間本地好的大學, 我想學習AI")