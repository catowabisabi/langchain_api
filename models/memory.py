from llms import LLM_OpenAI, OPENAI_API_KEY
from langchain import ConversationChain, OpenAI
from langchain.memory import ConversationBufferMemory

llm = LLM_OpenAI(OPENAI_API_KEY).llm
llm = OpenAI(openai_api_key = OPENAI_API_KEY, temperature=0.5, max_tokens=-1)
conversation = ConversationChain(llm=llm, verbose=True, memory=ConversationBufferMemory())

while True:
    # 在這裡添加您要重複執行的代碼
    user_input = input ("Enter your question: ")
    print(conversation.predict(input=user_input))
    if user_input.lower() == "exit":
        break
