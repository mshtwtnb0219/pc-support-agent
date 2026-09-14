import json

from src.openai_client import client
from src.tools.definitions import tools
from src.tools.ping import ping
from src.tools.ipconfig import ipconfig
from src.tools.nslookup import nslookup


INSTRUCTIONS = """
あなたはPCネットワークトラブルを診断するAIエージェントです。

診断に必要な情報が不足している場合は、利用可能なツールを実際に呼び出してください。

ツールを実行していないのに「実行しました」「確認しました」と回答してはいけません。

必要に応じて複数のツールを連続して使用してください。

十分な調査結果が揃った場合のみ、原因候補・確認結果・対処方法を回答してください。
"""


def run_agent(user_message: str) -> str:
    response = client.responses.create(
        model="gpt-5.5",
        input=user_message,
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

            else:
                result = {
                    "success": False,
                    "error": f"未対応のToolです：{item.name}"
                }

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