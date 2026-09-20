import os


from dotenv import load_dotenv
from  supabase import create_client, client


# .envを読み込む
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# クライアントの作成  supabase: client　→　型推論
supabase: client = create_client(url,key)


# print("URL:", url)
# print("KEY EXISTS:", bool(key))
# print("KEY PREFIX:", key[:15] if key else None)

