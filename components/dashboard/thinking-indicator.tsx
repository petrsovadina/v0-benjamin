import { Loader2 } from "lucide-react"

export function ThinkingIndicator() {
    return (
        <div className="flex items-center gap-3 p-4 text-sm text-muted-foreground bg-muted/50 rounded-lg animate-pulse">
            <Loader2 className="h-4 w-4 animate-spin text-primary" />
            <span>SÚKL AI přemýšlí a hledá v databázi...</span>
        </div>
    )
}
