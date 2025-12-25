import { Card } from "@/components/ui/card"

interface ChatMessageProps {
  message: {
    role: "user" | "assistant"
    content: string
    timestamp: Date
  }
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user"

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <Card
        className={`max-w-2xl p-4 ${
          isUser ? "bg-primary text-primary-foreground border-primary" : "bg-card border-border text-foreground"
        }`}
      >
        <p className="leading-relaxed whitespace-pre-wrap">{message.content}</p>
        <span className={`text-xs mt-2 block ${isUser ? "text-primary-foreground/70" : "text-muted-foreground"}`}>
          {message.timestamp.toLocaleTimeString("cs-CZ", {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </span>
      </Card>
    </div>
  )
}
