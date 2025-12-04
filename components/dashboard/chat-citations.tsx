import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface Citation {
  id: string
  type: "pmid" | "doi" | "guideline"
  value: string
  title: string
  year?: number
  authors?: string
}

interface ChatCitationsProps {
  citations: Citation[]
}

const getCitationLink = (citation: Citation): string => {
  switch (citation.type) {
    case "pmid":
      return `https://pubmed.ncbi.nlm.nih.gov/${citation.value}/`
    case "doi":
      return `https://doi.org/${citation.value}`
    case "guideline":
      return "#"
    default:
      return "#"
  }
}

const getCitationLabel = (citation: Citation): string => {
  switch (citation.type) {
    case "pmid":
      return "PubMed"
    case "doi":
      return "DOI"
    case "guideline":
      return "Guideline"
    default:
      return "Citation"
  }
}

export function ChatCitations({ citations }: ChatCitationsProps) {
  return (
    <div className="ml-0 mt-3 space-y-2">
      <p className="text-xs font-semibold text-muted-foreground">CITACE A ZDROJE:</p>
      <div className="space-y-2">
        {citations.map((citation) => (
          <Card key={citation.id} className="p-3 bg-muted/30 border-border hover:border-primary/50 transition-colors">
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0">
                <span className="inline-flex items-center justify-center h-6 w-6 rounded-full bg-primary/10 text-primary text-xs font-semibold">
                  {citations.indexOf(citation) + 1}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-foreground">{citation.title}</p>
                <div className="flex items-center gap-2 mt-1 text-xs text-muted-foreground">
                  {citation.authors && <span>{citation.authors}</span>}
                  {citation.year && <span>({citation.year})</span>}
                  <span className="text-primary font-medium">{getCitationLabel(citation)}</span>
                </div>
              </div>
              <Button asChild variant="ghost" size="sm" className="text-primary hover:text-primary/90 flex-shrink-0">
                <a href={getCitationLink(citation)} target="_blank" rel="noopener noreferrer">
                  Přejít
                </a>
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
