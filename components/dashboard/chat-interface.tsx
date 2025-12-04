"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { ChatMessage } from "@/components/dashboard/chat-message"
import { ChatCitations } from "@/components/dashboard/chat-citations"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  citations?: Citation[]
  timestamp: Date
}

interface Citation {
  id: string
  type: "pmid" | "doi" | "guideline"
  value: string
  title: string
  year?: number
  authors?: string
}

const mockCitations: Citation[] = [
  {
    id: "1",
    type: "pmid",
    value: "29832477",
    title: "Interaction of Sertraline and Warfarin",
    year: 2018,
    authors: "Smith J, et al",
  },
  {
    id: "2",
    type: "guideline",
    value: "ESC-2020",
    title: "European Society of Cardiology Guidelines on Atrial Fibrillation",
    year: 2020,
  },
  {
    id: "3",
    type: "doi",
    value: "10.1016/j.jacc.2021.01.017",
    title: "Drug Interactions in Clinical Practice",
    year: 2021,
    authors: "Johnson M, et al",
  },
]

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content:
        "Ahoj! Jsem Czech MedAI, tvůj AI asistent pro klinické otázky. Jak ti dnes mohu pomoci? Můžeš se mě zeptat na cokoliv vztahujícího se k medicíně, lékům, diagnóze nebo VZP úhradám.",
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

  const handleSendMessage = async () => {
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    // Simulate API call
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: `Zde je odpověď na váš dotaz: "${userMessage.content}"\n\nTato odpověď je založena na aktuálních vědeckých poznatcích a klinických pokynech. Viz citace níže pro více informací.`,
        citations: mockCitations,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, assistantMessage])
      setIsLoading(false)
    }, 1000)
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
            {message.citations && message.citations.length > 0 && <ChatCitations citations={message.citations} />}
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-center py-4">
            <div className="flex gap-1">
              <div className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: "0s" }}></div>
              <div className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: "0.2s" }}></div>
              <div className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: "0.4s" }}></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t border-border bg-card/50 p-6 backdrop-blur-sm">
        <Card className="p-4 bg-card border border-border">
          <div className="space-y-3">
            <div className="flex gap-2">
              <Input
                type="text"
                placeholder="Zadejte svůj klinický dotaz (např. 'Interakce sertralin + warfarin?')..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={isLoading}
                className="flex-1 bg-input border-border text-foreground placeholder:text-muted-foreground"
              />
              <Button
                onClick={handleSendMessage}
                disabled={isLoading || !input.trim()}
                className="px-6 bg-primary text-primary-foreground hover:bg-primary/90"
              >
                Odeslat
              </Button>
            </div>
            <p className="text-xs text-muted-foreground">
              💡 Tip: Buďte specifičtí. Např. místo "bolest" napište "bolest na levé straně hrudníku po fyzické námaže"
            </p>
          </div>
        </Card>
      </div>
    </div>
  )
}
