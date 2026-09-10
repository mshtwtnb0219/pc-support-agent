import subprocess
from openai import OpenAI
from dotenv import load_dotenv  
import os
import json

# pingコマンド実行
def ping(ip):
    result = subprocess.run(["ping", ip],capture_output=True,text=True)
    return {
        "host": ip,
        "success": result.returncode == 0,
        "output": result.stdout
    }
    
# ipconfigコマンド実行
def ipconfig():
    result = subprocess.run(["ipconfig"],capture_output=True,text=True)
    return {
        "success": result.returncode == 0,
        "output": result.stdout
    }

# LLMに見せる「ツールの説明」ping
pingTools = [
    {
        "type": "function",
        "name": "ping",
        "description": "指定したホストへのネットワーク疎通を確認する",
        "parameters": {
            "type": "object",
            "properties": {
                "ip": {
                    "type": "string"
                }
            },
            "required": ["ip"]
        }
    }
]

# LLMに見せる「ツールの説明」ipconfig
ipconfigTools = [
    {
        "type": "function",
        "name": "ipconfig",
        "description": "ipアドレス情報を取得する",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]




# envを読み込む
load_dotenv()


# OpenAIクライアントを作成する
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
)

# ツールのリストを結合
tools = pingTools + ipconfigTools

response = client.responses.create(
    model="gpt-5.5",
    # input="このpcのipアドレス情報を確認してください",
    input="8.8.8.8で疎通ができるか確認してください",
    tools=tools
)

# responseの中身
# [ResponseFunctionToolCall(arguments='{"ip":"8.8.8.8"}', call_id='call_XPXIOH2EtrrfSdxefM4R9PSR', name='ping', type='function_call', id='fc_05719beef615cc6b006aa10ef8a1cc87d0aa93f6f054124c36', caller=None, namespace=None, status='completed')]
print(response.output)


tool_outputs = []

# 複数ツールを実行する　→　実行結果をtool_outputsに格納
for item in response.output:
    if item.type == "function_call":
        # tool_callingの選択
        if item.name == "ping":
            arguments = json.loads(item.arguments)
            result = ping(arguments["ip"])
        elif item.name == "ipconfig":
            result = ipconfig()
            
        result_json = json.dumps(result,ensure_ascii=False)
        # LLMに返却する情報を詰め込む
        tool_outputs.append(
        {
            "type": "function_call_output",
            "call_id": item.call_id,
            "output":result_json
        }
        )
        


# ツールの実行結果をLLMに返却する
response = client.responses.create(
    model="gpt-5.5",
    previous_response_id=response.id,
    input=tool_outputs
)


print(response.output_text)
