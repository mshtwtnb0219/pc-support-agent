import json

from src.openai_client import client
from src.tools.definitions import tools
from src.tools.ping import ping
from src.tools.ipconfig import ipconfig
from src.tools.nslookup import nslookup
from src.tools.search_knowledge import search_knowledge


INSTRUCTIONS = """
あなたはPCネットワークトラブルを診断するAIエージェントです。

診断に必要な情報が不足している場合は、利用可能なツールを実際に呼び出してください。

ツールを実行していないのに「実行しました」「確認しました」と回答してはいけません。

必要に応じて複数のツールを連続して使用してください。

十分な調査結果が揃った場合のみ、原因候補・確認結果・対処方法を回答してください。
"""


def run_agent(user_message: str, history: list) -> str:
    
    # OpenAIに渡すinputを作成する
    input_message = []
    
    for chat_message in history:
        role = (
            "assistant"
            if chat_message.role == "agent"
            else "user"
        )
        
        input_message.append({
            "role": role,
            "content":chat_message.content
        })
    
    # 今回の質問を最後に追加
    input_message.append({
        "role": "user",
        "content": user_message
    })

    response = client.responses.create(
        model="gpt-5.5",
        input=input_message,
        instructions=INSTRUCTIONS,
        tools=tools
    )

    count = 0

    while True:
        count += 1

        if count >= 5:
            return "診断回数が上限に達しました。"

        tool_outputs = []

        for item in response.output:
            if item.type != "function_call":
                continue

            if item.name == "ping":
                arguments = json.loads(item.arguments)
                result = ping(arguments["ip"])

            elif item.name == "ipconfig":
                result = ipconfig()

            elif item.name == "nslookup":
                arguments = json.loads(item.arguments)
                result = nslookup(arguments["host"])
            elif item.name == "search_knowledge":
                arguments = json.loads(item.arguments)
                result = search_knowledge(arguments["query"])

            else:
                result = {
                    "success": False,
                    "error": f"未対応のToolです：{item.name}"
                }

            print(f"[TOOL RESULT] {result}")
            
            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(
                        result,
                        ensure_ascii=False
                    )
                }
            )

        if not tool_outputs:
            return response.output_text

        response = client.responses.create(
            model="gpt-5.5",
            previous_response_id=response.id,
            input=tool_outputs,
            tools=tools
        )
        
if __name__ == "__main__":
    print(
        run_agent(
            "DNSトラブルの確認手順を教えてください。",
            []
        )
    )