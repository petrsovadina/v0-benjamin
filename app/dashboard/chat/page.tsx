import { ChatInterface } from "@/components/dashboard/chat-interface"

export const metadata = {
  title: "AI Chat | Czech MedAI",
  description: "Komunikujte s AI asistentem",
}

import { ErrorBoundary } from "@/components/error-boundary"

export default function ChatPage() {
  return (
    <div className="h-[calc(100vh-120px)] flex flex-col">
      <ErrorBoundary>
        <ChatInterface />
      </ErrorBoundary>
    </div>
  )
}
