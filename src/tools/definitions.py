# LLMに渡すTool定義

tools = [
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
    },
    {
        "type": "function",
        "name": "ipconfig",
        "description": "IPアドレス情報を取得する",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
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
    },
    {
        "type": "function",
        "name": "search_knowledge",
        "description": (
            "PCトラブルに関するナレッジを検索します。"
            "トラブルの原因、確認手順、対処方法などの情報が必要な場合に使用してください。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "検索したいPCトラブルの内容"
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
]