import { Card } from "@/components/ui/card"

const stats = [
  {
    label: "Dotazů dnes",
    value: "12",
    change: "+3 od včeraj",
    color: "text-chart-1",
  },
  {
    label: "Ušetřený čas",
    value: "2h 34m",
    change: "Průměr 12 min/dotaz",
    color: "text-chart-2",
  },
  {
    label: "Tier",
    value: "Professional",
    change: "Neomezené dotazy",
    color: "text-chart-3",
  },
]

export function QuickStatsCards() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {stats.map((stat) => (
        <Card key={stat.label} className="p-4 bg-card border border-border">
          <div className="space-y-2">
            <p className="text-sm font-medium text-muted-foreground">{stat.label}</p>
            <div className="flex items-baseline gap-2">
              <p className={`text-2xl font-bold ${stat.color}`}>{stat.value}</p>
            </div>
            <p className="text-xs text-muted-foreground">{stat.change}</p>
          </div>
        </Card>
      ))}
    </div>
  )
}
