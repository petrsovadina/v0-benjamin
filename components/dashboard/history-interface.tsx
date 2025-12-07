"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState } from "react"

interface HistoryItem {
  id: string
  query: string
  date: string
  category: string
  preview: string
}

const mockHistory: HistoryItem[] = [
  {
    id: "1",
    query: "Interakce sertralin + warfarin + bisoprolol?",
    date: "Dnes 14:32",
    category: "Lékové interakce",
    preview: "Závažná interakce mezi warfarinem a SSRI...",
  },
  {
    id: "2",
    query: "NICE guidelines na fibrilaci síní 2024",
    date: "Dnes 11:15",
    category: "Guidelines",
    preview: "NICE doporučuje CHA2DS2-VASc skóre...",
  },
  {
    id: "3",
    query: "VZP úhrada terapie amiodaronem",
    date: "Včera 16:45",
    category: "VZP Navigator",
    preview: "Amiodaron je hrazen pod podmínkou...",
  },
]

export function HistoryInterface() {
  const [searchQuery, setSearchQuery] = useState("")

  const filteredHistory = mockHistory.filter(
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
        {filteredHistory.map((item) => (
          <Card
            key={item.id}
            className="p-4 bg-card border border-border hover:border-primary/50 cursor-pointer transition-colors"
          >
            <div className="space-y-3">
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-foreground">{item.query}</h3>
                  <p className="text-sm text-muted-foreground mt-1">{item.preview}</p>
                </div>
                <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground flex-shrink-0">
                  →
                </Button>
              </div>
              <div className="flex items-center gap-2 text-xs">
                <span className="px-2 py-1 rounded bg-primary/10 text-primary">{item.category}</span>
                <span className="text-muted-foreground">{item.date}</span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
