"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState, useEffect } from "react"
import { useAuth } from "@/lib/auth-context"
import { useRouter } from "next/navigation"
import { createClient } from "@/lib/supabase/client"

interface HistoryItem {
  id: string
  query: string
  date: string
  category: string
  preview: string
}

export function HistoryInterface() {
  const { user } = useAuth()
  const router = useRouter()
  const [searchQuery, setSearchQuery] = useState("")
  const [historyItems, setHistoryItems] = useState<HistoryItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchHistory = async () => {
      if (!user) {
        setLoading(false)
        return
      }

      try {
        const supabase = createClient()
        const { data: { session } } = await supabase.auth.getSession()
        const token = session?.access_token

        if (!token) return

        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

        const res = await fetch(`${apiUrl}/api/v1/query/history`, {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        })

        if (!res.ok) throw new Error("Failed to fetch history")

        const data = await res.json()

        const items = data.map((item: any) => ({
          id: item.id,
          query: item.query_text,
          date: new Date(item.created_at).toLocaleString('cs-CZ'),
          category: item.query_type === 'drug_info' ? 'Léky' :
            (item.query_type === 'guidelines' ? 'Guidelines' : 'Klinický dotaz'),
          preview: item.response_text ? item.response_text.substring(0, 80) + "..." : "Bez odpovědi"
        }))

        setHistoryItems(items)
      } catch (err) {
        console.error("Failed to fetch sessions", err)
      } finally {
        setLoading(false)
      }
    }

    fetchHistory()
  }, [user])

  const filteredHistory = historyItems.filter(
    (item) =>
      item.query.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.category.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  return (
    <div className="space-y-4">
      {/* Search */}
      <Input
        type="search"
        placeholder="Hledat v historii..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        className="bg-input border-border text-foreground placeholder:text-muted-foreground"
      />

      {/* Items */}
      <div className="space-y-3">
        {loading ? (
          <div className="text-center text-muted-foreground py-4">Načítám historii...</div>
        ) : filteredHistory.length === 0 ? (
          <div className="text-center text-muted-foreground py-4">Žádná historie nenalezena.</div>
        ) : (
          filteredHistory.map((item) => (
            <Card
              key={item.id}
              // Note: Currently just viewing recent queries. 
              // In full app, clicking might reload that query context or show detail.
              // For now, doing nothing or maybe pre-filling chat?
              // Let's keep it clickable but maybe just console log or TODO
              onClick={() => console.log("Load query", item.id)}
              className="p-4 bg-card border border-border hover:border-primary/50 cursor-pointer transition-colors"
            >
              <div className="space-y-3">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium text-foreground">{item.query}</h3>
                    <p className="text-sm text-muted-foreground mt-1">{item.preview}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <span className="px-2 py-1 rounded bg-primary/10 text-primary">{item.category}</span>
                  <span className="text-muted-foreground">{item.date}</span>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  )
}
