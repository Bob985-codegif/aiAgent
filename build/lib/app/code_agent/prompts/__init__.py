from langchain_core.output_parsers import StrOutputParser

from app.code_agent.model.qwen import llm_qwen
from app.code_agent.prompts.multi_chat_prompts import multi_chat_prompt

chain = multi_chat_prompt | llm_qwen | StrOutputParser()

for chunk in chain.stream({"question": "你是谁"}):
    print(chunk.content, end="")
