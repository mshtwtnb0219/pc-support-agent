import os
from dotenv import load_dotenv
from openai import OpenAI 


# envを読み込む
load_dotenv()

# OpenAIクライアントを作成する
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
)