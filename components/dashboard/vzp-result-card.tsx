import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

interface VzpResult {
  id: string
  name: string
  inn: string
  atc: string
  form: string
  coverage: "full" | "partial" | "limited"
  conditions: string[]
  alternatives: string[]
}

interface VzpResultCardProps {
  result: VzpResult
}

const getCoverageBadge = (coverage: string) => {
  switch (coverage) {
    case "full":
      return <Badge className="bg-green-500/20 text-green-600 border-green-500/30">Plná úhrada</Badge>
    case "partial":
      return <Badge className="bg-yellow-500/20 text-yellow-600 border-yellow-500/30">Částečná úhrada</Badge>
    case "limited":
      return <Badge className="bg-red-500/20 text-red-600 border-red-500/30">Omezená úhrada</Badge>
    default:
      return null
  }
}

export function VzpResultCard({ result }: VzpResultCardProps) {
  return (
    <Card className="p-5 bg-card border border-border hover:border-primary/50 transition-colors">
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-start justify-between gap-3">
          <div>
            <h3 className="font-semibold text-lg text-foreground">{result.name}</h3>
            <p className="text-xs text-muted-foreground mt-1">{result.inn}</p>
          </div>
          {getCoverageBadge(result.coverage)}
        </div>

        {/* Details grid */}
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div>
            <p className="text-xs text-muted-foreground">ATC kód</p>
            <p className="font-mono text-foreground">{result.atc}</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">Forma</p>
            <p className="text-foreground">{result.form}</p>
          </div>
        </div>

        {/* Conditions */}
        <div>
          <p className="text-xs font-medium text-muted-foreground mb-2">Indikace</p>
          <div className="flex flex-wrap gap-1">
            {result.conditions.map((condition) => (
              <Badge key={condition} variant="outline" className="text-xs">
                {condition}
              </Badge>
            ))}
          </div>
        </div>

        {/* Alternatives */}
        <div>
          <p className="text-xs font-medium text-muted-foreground mb-2">Alternativy</p>
          <div className="flex flex-wrap gap-1">
            {result.alternatives.map((alt) => (
              <span key={alt} className="text-xs px-2 py-1 rounded bg-muted text-muted-foreground">
                {alt}
              </span>
            ))}
          </div>
        </div>

        {/* Action button */}
        <Button variant="outline" className="w-full border-border text-foreground hover:bg-muted bg-transparent">
          Více informací
        </Button>
      </div>
    </Card>
  )
}
