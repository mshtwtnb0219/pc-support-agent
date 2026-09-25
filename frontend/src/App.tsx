import { Box, Button, Container, Flex, Heading, Input, Text } from "@chakra-ui/react"
import ReactMarkdown from "react-markdown"
import { useEffect, useRef, useState } from "react"


type ChatMessage = {
  role: "user" | "agent",
  content: string
}


function App() {

  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [loading, setLoading] = useState(false)

  // メッセージが追加されたら自動で一番下へスクロール
  const bottomRef = useRef<HTMLDivElement>(null)


  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth"
    })
  }, [messages, loading])





  const handleSubmit = async () => {

    // 空文字の場合
    if (!message.trim() || loading) {
      return
    }

    const currentMessage = message
    setMessage("")

    try {
      setLoading(true)

      // 履歴の作成 質問
      const userMessage: ChatMessage = {
        role: "user",
        content: currentMessage
      }
      setMessages((prev) => [...prev, userMessage])

      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: currentMessage,
          history: messages,
        }),
      })

      if (response.status === 429) {
        throw new Error(
          "APIの利用上限に達したか、一時的にリクエストが集中しています。しばらくしてからもう一度お試しください。"
        )
      }

      if (response.status >= 500) {
        throw new Error("サーバーでエラーが発生しました。しばらくしてからもう一度お試しください。");
      }

      if (!response.ok) {
        throw new Error("APIリクエストに失敗しました")
      }

      const data = await response.json()

      // 履歴の作成 agent
      const agentMessage: ChatMessage = {
        role: "agent",
        content: data.answer
      }
      setMessages((prev) => [...prev, agentMessage])

    } catch (error) {
      const errorMessage: ChatMessage = {
        role: "agent",
        content:
          error instanceof Error
            ? error.message
            : "予期しないエラーが発生しました。",
      }

      setMessages((prev) => [...prev, errorMessage])


    } finally {
      setLoading(false)
    }
  }


  return (
    <Box minH="100vh" bg="gray.50" py="8">
      <Container maxW="3xl">
        <Heading size="xl">
          PC Support  Agent
        </Heading>
        <Text mt="2" color="gray.600">
          PCのトラブルについて質問してください
        </Text>

        <Box mt="8">

          {/* チャット履歴 */}
          <Box
            h="500px"
            overflowY="auto"
            p="4"
            bg="gray.50"
            borderRadius="lg"
          >
            {messages.map((chatMessage, index) => (
              <Flex
                key={index}
                justifyContent={
                  chatMessage.role === "user" ? "flex-end" : "flex-start"
                }
                mt="4"
              >
                <Box
                  maxW="80%"
                  p="4"
                  bg={chatMessage.role === "user" ? "blue.100" : "white"}
                  borderRadius="lg"
                  boxShadow="sm"
                >
                  <Text fontWeight="bold" mb="2">
                    {chatMessage.role === "user" ? "あなた" : "Agent"}
                  </Text>

                  <ReactMarkdown>
                    {chatMessage.content}
                  </ReactMarkdown>
                </Box>
              </Flex>
            ))}

            {/* 回答生成中 */}
            {loading && (
              <Flex justifyContent="flex-start" mt="4">
                <Box
                  maxW="80%"
                  p="4"
                  bg="white"
                  borderRadius="lg"
                  boxShadow="sm"
                >
                  <Text fontWeight="bold" mb="2">
                    Agent
                  </Text>

                  <Text color="gray.500">
                    回答を生成中...
                  </Text>
                </Box>
              </Flex>
            )}

            {/* 自動スクロールの移動先 */}
            <div ref={bottomRef} />
          </Box>

          {/* 入力エリア */}
          <Flex gap="2" mt="4">
            <Input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleSubmit()
                }
              }}
              placeholder="例：インターネットにつながりません"
            />

            <Button
              onClick={handleSubmit}
              disabled={loading || !message.trim()}
            >
              {loading ? "回答生成中..." : "送信"}
            </Button>
          </Flex>

        </Box>
      </Container>
    </Box>
  )
}

export default App
