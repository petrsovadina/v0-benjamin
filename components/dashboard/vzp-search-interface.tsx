"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { VzpResultCard } from "@/components/dashboard/vzp-result-card"

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

const mockResults: VzpResult[] = [
  {
    id: "1",
    name: "Bisoprolol",
    inn: "Bisoprolol fumarate",
    atc: "C07AB07",
    form: "5 mg tableta",
    coverage: "full",
    conditions: ["Hypertenze", "Fibrilace síní", "Angina pectoris"],
    alternatives: ["Metoprolol", "Atenolol", "Propranolol"],
  },
  {
    id: "2",
    name: "Warfarin",
    inn: "Warfarin sodium",
    atc: "B01AA03",
    form: "5 mg tableta",
    coverage: "partial",
    conditions: ["Fibrilace síní", "Trombóza", "Embolie"],
    alternatives: ["Dabigatran", "Rivaroxaban", "Apixaban"],
  },
  {
    id: "3",
    name: "Sertralin",
    inn: "Sertraline hydrochloride",
    atc: "N06AB06",
    form: "50 mg tableta",
    coverage: "limited",
    conditions: ["Deprese", "Úzkostná porucha"],
    alternatives: ["Fluoxetin", "Paroxetin", "Escitalopram"],
  },
]

export function VzpSearchInterface() {
  const [searchQuery, setSearchQuery] = useState("")
  const [results, setResults] = useState<VzpResult[]>([])
  const [hasSearched, setHasSearched] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const handleSearch = async () => {
    if (!searchQuery.trim()) return

    setIsLoading(true)
    setHasSearched(true)

    // Simulate API call
    setTimeout(() => {
      const filtered = mockResults.filter(
        (r) =>
          r.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          r.inn.toLowerCase().includes(searchQuery.toLowerCase()) ||
          r.atc.toLowerCase().includes(searchQuery.toLowerCase()),
      )
      setResults(filtered.length > 0 ? filtered : mockResults)
      setIsLoading(false)
    }, 800)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault()
      handleSearch()
    }
  }

  return (
    <div className="space-y-6">
      {/* Search box */}
      <Card className="p-6 bg-card border border-border">
        <div className="space-y-4">
          <div className="flex gap-3">
            <Input
              type="text"
              placeholder="Vyhledejte lék (např. 'Bisoprolol', 'warfarin', 'C07AB07')..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
              className="flex-1 bg-input border-border text-foreground placeholder:text-muted-foreground"
            />
            <Button
              onClick={handleSearch}
              disabled={isLoading || !searchQuery.trim()}
              className="px-8 bg-primary text-primary-foreground hover:bg-primary/90"
            >
              {isLoading ? "Hledám..." : "Vyhledat"}
            </Button>
          </div>

          {/* Search tips */}
          <div className="flex flex-wrap gap-2 text-xs">
            <span className="text-muted-foreground">Tipy:</span>
            <button
              onClick={() => setSearchQuery("Bisoprolol")}
              className="px-2 py-1 rounded bg-primary/10 text-primary hover:bg-primary/20 transition-colors"
            >
              Bisoprolol
            </button>
            <button
              onClick={() => setSearchQuery("C07AB")}
              className="px-2 py-1 rounded bg-primary/10 text-primary hover:bg-primary/20 transition-colors"
            >
              C07AB (beta-blokátory)
            </button>
            <button
              onClick={() => setSearchQuery("Warfarin")}
              className="px-2 py-1 rounded bg-primary/10 text-primary hover:bg-primary/20 transition-colors"
            >
              Warfarin
            </button>
          </div>
        </div>
      </Card>

      {/* Results */}
      {hasSearched && (
        <div className="space-y-4">
          {results.length > 0 ? (
            <>
              <p className="text-sm text-muted-foreground">
                Nalezeno <span className="font-semibold text-foreground">{results.length}</span> výsledků
              </p>
              {results.map((result) => (
                <VzpResultCard key={result.id} result={result} />
              ))}
            </>
          ) : (
            <Card className="p-6 bg-card border border-border text-center">
              <p className="text-muted-foreground">
                Žádné výsledky pro "{searchQuery}". Zkuste jiný název léku či ATC kód.
              </p>
            </Card>
          )}
        </div>
      )}

      {!hasSearched && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {mockResults.map((result) => (
            <VzpResultCard key={result.id} result={result} />
          ))}
        </div>
      )}
    </div>
  )
}
