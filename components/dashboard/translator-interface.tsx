"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card } from "@/components/ui/card"
import { Loader2, Languages, ArrowRight, ArrowLeftRight } from "lucide-react"

export function TranslatorInterface() {
    const [input, setInput] = useState("")
    const [output, setOutput] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const [targetLang, setTargetLang] = useState("Czech")

    const handleTranslate = async () => {
        if (!input.trim()) return

        setIsLoading(true)
        try {
            const response = await fetch("/api/translate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: input, language: targetLang }),
            })

            if (!response.ok) throw new Error("Failed to translate")

            const data = await response.json()
            setOutput(data.response)
        } catch (error) {
            console.error("Error:", error)
            setOutput("Chyba při překladu.")
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[calc(100vh-10rem)]">
            {/* Input Column */}
            <Card className="flex flex-col p-4 border-border bg-card">
                <div className="mb-4 flex justify-between items-center">
                    <h2 className="font-semibold text-lg flex items-center gap-2">
                        <Languages className="h-5 w-5 text-primary" />
                        Zdrojový text
                    </h2>
                    <div className="text-xs text-muted-foreground p-1 border rounded bg-muted">
                        Auto-detect
                    </div>
                </div>
                <Textarea
                    placeholder="Vložte text k překladu (např. anglická lékařská zpráva)..."
                    className="flex-1 resize-none font-mono text-sm bg-muted/50 focus:bg-background transition-colors"
                    value={input}
                    onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setInput(e.target.value)}
                />
            </Card>

            {/* Output Column */}
            <Card className="flex flex-col p-4 border-border bg-card relative">
                <div className="mb-4 flex justify-between items-center">
                    <h2 className="font-semibold text-lg">Český překlad</h2>
                    <Button variant="outline" size="sm" onClick={() => navigator.clipboard.writeText(output)} disabled={!output}>
                        Kopírovat
                    </Button>
                </div>

                <div className="flex-1 overflow-auto rounded-md border border-border bg-muted/30 p-4 font-mono text-sm whitespace-pre-wrap">
                    {isLoading ? (
                        <div className="h-full flex items-center justify-center text-muted-foreground">
                            <Loader2 className="h-8 w-8 animate-spin" />
                        </div>
                    ) : output ? (
                        output
                    ) : (
                        <div className="h-full flex flex-col items-center justify-center text-muted-foreground opacity-50">
                            <ArrowLeftRight className="h-12 w-12 mb-2" />
                            <p>Zde se objeví překlad</p>
                        </div>
                    )}
                </div>
            </Card>

            <div className="lg:col-span-2 flex justify-center">
                <Button
                    size="lg"
                    className="w-full md:w-auto px-8"
                    onClick={handleTranslate}
                    disabled={isLoading || !input.trim()}
                >
                    {isLoading ? "Překládám..." : "Přeložit do Češtiny"}
                </Button>
            </div>
        </div>
    )
}
