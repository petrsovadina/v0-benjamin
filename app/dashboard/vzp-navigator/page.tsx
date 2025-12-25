import { VzpSearchInterface } from "@/components/dashboard/vzp-search-interface"
import { Card } from "@/components/ui/card"

export const metadata = {
  title: "VZP Navigator | Czech MedAI",
  description: "Zjistěte informace o úhradách pojišťovny",
}

export default function VzpNavigatorPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">VZP Navigator</h1>
        <p className="text-muted-foreground mt-1">Zjistěte informace o úhradách léků a výkonů podle VZP</p>
      </div>

      {/* Info card */}
      <Card className="p-6 bg-card border border-border bg-gradient-to-r from-primary/5 to-transparent">
        <div className="space-y-3">
          <h2 className="font-semibold text-foreground">Jak používat VZP Navigator</h2>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>• Vyhledejte lék podle názvu či International Nonproprietary Name (INN)</li>
            <li>• Zjistěte příslušný ATC kód a formaci léku</li>
            <li>• Poznáte podmínky úhrady a případná omezení</li>
            <li>• Podívejte se na alternativní léky v kategoriích</li>
          </ul>
        </div>
      </Card>

      {/* Search interface */}
      <VzpSearchInterface />
    </div>
  )
}
