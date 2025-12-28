"use client"

import type React from "react"
import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { ChatMessage } from "@/components/dashboard/chat-message"
import { ChatCitations } from "@/components/dashboard/chat-citations"
import { ChatSuggestions } from "@/components/dashboard/chat-suggestions"
import { ThinkingIndicator } from "@/components/dashboard/thinking-indicator"
import { createClient } from "@/lib/supabase/client"
import { useAuth } from "@/lib/auth-context"
import { useRouter } from "next/navigation"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  citations?: Citation[]
  suggestions?: string[]
  timestamp: Date
}

interface Citation {
  source: string;
  title: string;
  url: string;
  metadata?: any;
}

export function ChatInterface({ sessionId }: { sessionId?: string }) {
  const { user } = useAuth()
  const router = useRouter()
  // const [currentSessionId, setCurrentSessionId] = useState<string | undefined>(sessionId)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "init",
      role: "assistant",
      content:
        "Ahoj! Jsem Czech MedAI (v2.0), tvůj AI asistent pro klinické otázky. Jak ti dnes mohu pomoci? Můžeš se mě zeptat na cokoliv vztahujícího se k medicíně, lékům, diagnóze nebo VZP úhradám.",
      citations: [],
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (textOverride?: string) => {
    const textToSend = textOverride || input
    if (!textToSend.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: textToSend,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      // 1. Get Token
      const supabase = createClient()
      const { data: { session } } = await supabase.auth.getSession()
      const token = session?.access_token

      if (!token) {
        throw new Error("Nejste přihlášen/a")
      }

      // 2. Call Backend API (Non-streaming for v2.0 MVP)
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

      const response = await fetch(`${apiUrl}/api/v1/query/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          message: textToSend,
          history: messages.map(m => ({ role: m.role, content: m.content }))
        }),
      })

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`)
      }

      const data = await response.json()

      // 3. Process Response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response,
        citations: data.citations || [],
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])

    } catch (error) {
      console.error("Error sending message:", error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: `Omlouvám se, ale došlo k chybě: ${error}`,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Messages area */}
      <div className="flex-1 overflow-auto p-6 space-y-4">
        {messages.map((message) => (
          <div key={message.id}>
            <ChatMessage message={message} />
            {/* Map backend citations to frontend component props if needed, or update ChatCitations component */}
            {message.citations && message.citations.length > 0 && <ChatCitations citations={message.citations.map((c, i) => ({
              id: i.toString(),
              type: c.source === 'pubmed' ? 'pmid' : (c.source === 'sukl' ? 'database' : 'guideline'),
              title: c.title,
              value: c.url,
              year: parseInt(c.metadata?.year || "2024"),
              authors: Array.isArray(c.metadata?.authors) ? c.metadata.authors.join(", ") : c.metadata?.authors
            }))} />}
          </div>
        ))}
        {isLoading && <ThinkingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t border-border bg-card/50 p-6 backdrop-blur-sm">
        <Card className="p-4 bg-card border border-border">
          <div className="space-y-3">
            <div className="flex gap-2">
              <Input
                type="text"
                placeholder="Zadejte svůj klinický dotaz..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={isLoading}
                className="flex-1 bg-input border-border text-foreground placeholder:text-muted-foreground"
              />
              <Button
                onClick={() => handleSendMessage()}
                disabled={isLoading || !input.trim()}
                className="px-6 bg-primary text-primary-foreground hover:bg-primary/90"
              >
                Odeslat
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}
