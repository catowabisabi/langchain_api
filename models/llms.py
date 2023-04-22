from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
import configparser

from prompts.prompt_templates import prompt_zh_points_and_summary
from database.fake_data import fake_news1, fake_news2

config = configparser.ConfigParser()
config.read('config\config.ini')
OPENAI_API_KEY = config.get('openai', 'OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

class LLM_OpenAI:
    def __init__(self, OPENAI_API_KEY, temperature=0, max_tokens=-1):
        self.llm = OpenAI(openai_api_key = OPENAI_API_KEY, temperature=temperature, max_tokens=1000)
    
    def get_llm_anwser(self):

        text = "what are 5 vacation destinations for someone who likes to eat pasta?"
        reply = self.llm(text)
        print(reply)

    def get_llm_anwser_with_prompt_template(self):
        prompt = PromptTemplate(
            input_variables=["food"],
            template="What are 5 vacation destinations for someone who likes to eat {food}?"
            )
        print(prompt.format(food="apple"))
        print(self.llm(prompt.format(food="apple")))

    def summarize_text(self, text, prompt_template=prompt_zh_points_and_summary):
        prompt = prompt_template
        #print(prompt.format(text=text))
        print(self.llm(prompt.format(text=text)))

#chatbot = LLM(OPENAI_API_KEY)
#chatbot.get_llm_anwser_with_prompt_template()
#chatbot.summarize_text(fake_news2, prompt_zh_points_and_summary)

