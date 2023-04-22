from langchain.chains import LLMChain
from llms import LLM_OpenAI
from prompts.prompt_templates import prompt_zh_points_and_summary
from database.fake_data import fake_news1, fake_news2

import os
from llms import OPENAI_API_KEY




llm_openai = LLM_OpenAI(OPENAI_API_KEY, temperature=0.9)
prompt = prompt_zh_points_and_summary

chain = LLMChain(llm=llm_openai.llm, prompt=prompt)
print(chain.run(fake_news1))

