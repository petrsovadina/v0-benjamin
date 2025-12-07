import { HistoryInterface } from "@/components/dashboard/history-interface"

export const metadata = {
  title: "Historie | Czech MedAI",
  description: "Přehled vašich dosavadních dotazů",
}

export default function HistoryPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Historie</h1>
        <p className="text-muted-foreground mt-1">Přehled vašich dosavadních dotazů a odpovědí</p>
      </div>
      <HistoryInterface />
    </div>
  )
}
