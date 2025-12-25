import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

const recentQueries = [
  {
    id: 1,
    query: "Interakce sertralin + warfarin + bisoprolol?",
    date: "Dnes 14:32",
    category: "Lékové interakce",
  },
  {
    id: 2,
    query: "NICE guidelines na fibrilaci síní 2024",
    date: "Dnes 11:15",
    category: "Guidelines",
  },
  {
    id: 3,
    query: "VZP úhrada terapie amiodaronem",
    date: "Včera 16:45",
    category: "VZP Navigator",
  },
  {
    id: 4,
    query: "Diagnostika diabetu 2. typu",
    date: "Včera 09:20",
    category: "Diagnostika",
  },
]

export function RecentQueries() {
  return (
    <Card className="p-6 bg-card border border-border">
      <h2 className="text-lg font-semibold text-foreground mb-4">Nedávné dotazy</h2>
      <div className="space-y-3">
        {recentQueries.map((q) => (
          <div
            key={q.id}
            className="flex items-start justify-between p-3 rounded-lg hover:bg-muted/30 cursor-pointer transition-colors"
          >
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-foreground truncate">{q.query}</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-xs px-2 py-1 rounded bg-primary/10 text-primary">{q.category}</span>
                <span className="text-xs text-muted-foreground">{q.date}</span>
              </div>
            </div>
            <Button variant="ghost" size="sm" className="ml-2 text-muted-foreground hover:text-foreground">
              →
            </Button>
          </div>
        ))}
      </div>
    </Card>
  )
}
