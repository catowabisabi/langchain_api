
from langchain.prompts import PromptTemplate

prompt_zh_points_and_summary = PromptTemplate(    
       
    input_variables=["text"],
    template="請用繁體中文例出用戶提供的文字的重點, 以點的形式。 \
        例如:\n \
        1) 重點1\
        2) 重點2\
        3) 重點3\
        如此類推。\
        然後再用繁體中文總結用戶提供的文字的重點。並說明文章所述的各項事件對經濟, 巿場, 或加密幣貨幣的影響, 請詳細說明有正面還是負面的影響, 並列出有可能受影響的股票或加密産品\
        例如: \
        \n總結:\n\
        用戶提供的文字: {text}"
    )