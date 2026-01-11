import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-a5bc80b2ab0043e49c16a846e81e02b8",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3-235b-a22b",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "你是谁？"
        },
    ],
)
print(completion.model_dump_json())
