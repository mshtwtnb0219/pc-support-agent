import { Box, Button, Container, Heading, Input, Text } from "@chakra-ui/react"
import ReactMarkdown from "react-markdown"
import { useState } from "react"


type ChatMessage = {
  role: "user" | "agent",
  content: string
}


function App() {

  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState<ChatMessage[]>([])
  // loading
  const [loading, setLoading] = useState(false)


  const handleSubmit = async () => {
    try {
      setLoading(true)

      // 履歴の作成 質問
      const userMessage: ChatMessage = {
        role: "user",
        content: message
      }
      setMessages((prev) => [...prev, userMessage])

      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message,
        }),
      })

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
      setMessage("")

    } catch (error) {
      const errorMessage: ChatMessage = {
        role: "agent",
        content: `エラーが発生しました。もう一度お試しください。: ${error}`,
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
          <Input value={message} onChange={(e) => setMessage(e.target.value)} placeholder="例：インターネットにつながりません" />
          <Button mt="3" onClick={handleSubmit} disabled={loading}>
            {loading ? "回答生成中...." : "送信"}
          </Button>


          {messages.map((chatMessage, index) => (
            <Box
              key={index}
              mt="4"
              p="4"
              bg={chatMessage.role === "user" ? "gray.100" : "white"}
            >
              <Text fontWeight="bold" mb="2">
                {chatMessage.role === "user" ? "あなた" : "Agent"}
              </Text>

              <ReactMarkdown>
                {chatMessage.content}
              </ReactMarkdown>
            </Box>
          ))}
        </Box>
      </Container>
    </Box>
  )
}

export default App
