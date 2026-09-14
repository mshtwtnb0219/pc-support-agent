import subprocess
from openai import OpenAI
from dotenv import load_dotenv  
import os
import json

# pingコマンド実行
def ping(ip):
    try:
        result = subprocess.run(["ping", ip],capture_output=True,text=True, timeout=10)
        return {
            "host": ip,
            "success": result.returncode == 0,
            "output": result.stdout
        }
    except Exception as e:
        return {
            "host": ip,
            "success":False,
            "error": str(e)
        }
        
    
# ipconfigコマンド実行
def ipconfig():
    try:
        result = subprocess.run(["ipconfig"],capture_output=True,text=True)
        return {
            "success": result.returncode == 0,
            "output": result.stdout
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# nslookupコマンド
def nslookup(host):
    try:
        result = subprocess.run(["nslookup",host],capture_output=True,text=True)
        return {
            "host": host,
            "success": result.returncode == 0,
            "output": result.stdout
        }
    except Exception as e:
        return {
            "host":host,
            "success":False,
            "error": str(e)
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

# LLMに見せる「ツールの説明」nslookup
nslookupTools = [
    {
        "type": "function",
        "name": "nslookup",
        "description": "指定したホスト名のDNS名前解決を確認する",
        "parameters": {
            "type": "object",
            "properties": {
                "host": {
                    "type": "string"
                }
            },
            "required": ["host"]
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
tools = pingTools + ipconfigTools + nslookupTools

response = client.responses.create(
    model="gpt-5.5",
    # input="このpcのipアドレス情報を確認してください",
    input="インターネットがつながりません。原因を調べてください。",
    instructions="""
あなたはPCネットワークトラブルを診断するAIエージェントです。

診断に必要な情報が不足している場合は、利用可能なツールを実際に呼び出してください。
ツールを実行していないのに「実行しました」「確認しました」と回答してはいけません。

必要に応じて複数のツールを連続して使用してください。
十分な調査結果が揃った場合のみ、原因候補・確認結果・対処方法を回答してください。
""",
    tools=tools
)

# responseの中身
# [ResponseFunctionToolCall(arguments='{"ip":"8.8.8.8"}', call_id='call_XPXIOH2EtrrfSdxefM4R9PSR', name='ping', type='function_call', id='fc_05719beef615cc6b006aa10ef8a1cc87d0aa93f6f054124c36', caller=None, namespace=None, status='completed')]
print(response.output)

# Agent Loop　無限ループ抑止
count = 0

while True:
    count += 1
    print(f"Agent Loop開始： {count}")
    
    if count >= 5:
        print("最大回数に到達したため終了します")
        break
    
    # function callの実行結果
    tool_outputs = []
# 複数ツールを実行する　→　実行結果をtool_outputsに格納
    for item in response.output:
        
        # ツールの実行
        if item.type == "function_call":
            print("呼び出されたTool：" , item.name)
            # tool_callingの選択
            if item.name == "ping":
                arguments = json.loads(item.arguments)
                result = ping(arguments["ip"])
            elif item.name == "ipconfig":
                result = ipconfig()
            elif item.name == "nslookup":
                arguments = json.loads(item.arguments)
                result = nslookup(arguments["host"])
            else:
                result = {
                    "success": False,
                    "error":f"未対応のToolです：{item.name}"
                }
                
            result_json = json.dumps(result,ensure_ascii=False)
            # LLMに返却する情報を詰め込む
            tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output":result_json
            }
            )
            print("Tool実行結果：",result_json[:500])
    

    # 全部調べて空の場合
    if not tool_outputs:
        print(response.output_text)
        break 
    
    print("LLMへ返すtool_outputs:", tool_outputs)
    
    # ツールの実行結果をLLMに返却する
    response = client.responses.create(
        model="gpt-5.5",
        previous_response_id=response.id,
        input=tool_outputs,
        tools=tools
    )

    print("新しいresponse.id:", response.id)
        






