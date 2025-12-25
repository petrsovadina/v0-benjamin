import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export interface DrugInfo {
    suklCode: string
    name: string
    activeSubstance: string
    strength?: string
    form?: string
    packageSize?: string
}

interface DrugInfoCardProps {
    drug: DrugInfo
}

export function DrugInfoCard({ drug }: DrugInfoCardProps) {
    return (
        <Card className="p-4 bg-card border border-border mt-3">
            <div className="flex justify-between items-start mb-2">
                <div>
                    <h3 className="font-bold text-lg text-primary">{drug.name}</h3>
                    <p className="text-xs text-muted-foreground">Účinná látka: {drug.activeSubstance}</p>
                </div>
                <Badge variant="outline" className="font-mono">{drug.suklCode}</Badge>
            </div>

            <div className="grid grid-cols-2 gap-2 text-sm mt-3">
                <div className="bg-muted/30 p-2 rounded">
                    <span className="text-xs text-muted-foreground block">Síla</span>
                    <span className="font-medium">{drug.strength || "N/A"}</span>
                </div>
                <div className="bg-muted/30 p-2 rounded">
                    <span className="text-xs text-muted-foreground block">Forma</span>
                    <span className="font-medium">{drug.form || "N/A"}</span>
                </div>
                <div className="bg-muted/30 p-2 rounded col-span-2">
                    <span className="text-xs text-muted-foreground block">Balení</span>
                    <span className="font-medium">{drug.packageSize || "N/A"}</span>
                </div>
            </div>
        </Card>
    )
}
