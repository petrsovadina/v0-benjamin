import { ChatInterface } from "@/components/dashboard/chat-interface"

export const metadata = {
  title: "AI Chat | Czech MedAI",
  description: "Komunikujte s AI asistentem",
}

export default function ChatPage() {
  return (
    <div className="h-[calc(100vh-120px)] flex flex-col">
      <ChatInterface />
    </div>
  )
}
