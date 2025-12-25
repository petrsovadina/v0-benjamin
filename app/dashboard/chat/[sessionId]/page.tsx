import { ChatInterface } from "@/components/dashboard/chat-interface"

interface ChatPageProps {
    params: Promise<{
        sessionId: string
    }>
}

export const metadata = {
    title: "Chat | Czech MedAI",
    description: "Klinický AI asistent",
}

export default async function ChatPage({ params }: ChatPageProps) {
    const { sessionId } = await params
    return <ChatInterface sessionId={sessionId} />
}
