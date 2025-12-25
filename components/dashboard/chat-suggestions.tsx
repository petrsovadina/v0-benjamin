import { Button } from "@/components/ui/button"
import { Sparkles } from "lucide-react"

interface ChatSuggestionsProps {
    suggestions: string[]
    onSelect: (suggestion: string) => void
}

export function ChatSuggestions({ suggestions, onSelect }: ChatSuggestionsProps) {
    if (!suggestions || suggestions.length === 0) return null

    return (
        <div className="flex flex-wrap gap-2 mt-3 ml-0">
            {suggestions.map((suggestion, index) => (
                <Button
                    key={index}
                    variant="outline"
                    size="sm"
                    className="text-xs h-7 bg-background/50 hover:bg-background hover:text-primary border-primary/20 hover:border-primary/50 transition-all duration-200"
                    onClick={() => onSelect(suggestion)}
                >
                    <Sparkles className="w-3 h-3 mr-1.5 opacity-70" />
                    {suggestion}
                </Button>
            ))}
        </div>
    )
}
