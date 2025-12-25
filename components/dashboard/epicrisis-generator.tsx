"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card } from "@/components/ui/card"
import { Loader2, FileText, ArrowRight } from "lucide-react"

export function EpicrisisGenerator() {
    const [input, setInput] = useState("")
    const [output, setOutput] = useState("")
    const [isLoading, setIsLoading] = useState(false)


    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (!file) return

        setIsLoading(true)
        try {
            const formData = new FormData()
            formData.append("file", file)

            const response = await fetch("/api/transcribe", {
                method: "POST",
                body: formData,
            })

            if (!response.ok) throw new Error("Transcription failed")

            const data = await response.json()
            setInput((prev) => (prev ? prev + "\n\n" + data.transcript : data.transcript))
        } catch (error) {
            console.error("Transcription error:", error)
        } finally {
            setIsLoading(false)
            e.target.value = ""
        }
    }

    const handleGenerate = async () => {
        if (!input.trim()) return

        setIsLoading(true)
        try {
            const response = await fetch("/api/epicrisis", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ items: input }),
            })

            if (!response.ok) throw new Error("Failed to generate report")

            const data = await response.json()
            setOutput(data.response)
        } catch (error) {
            console.error("Error:", error)
            setOutput("Chyba při generování reportu. Zkuste to prosím znovu.")
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[calc(100vh-10rem)]">
            {/* Input Column */}
            <Card className="flex flex-col p-4 border-border bg-card">
                <div className="mb-4 flex justify-between items-start">
                    <div>
                        <h2 className="font-semibold text-lg flex items-center gap-2">
                            <FileText className="h-5 w-5 text-primary" />
                            Vstupní data
                        </h2>
                        <p className="text-sm text-muted-foreground">
                            Vložte poznámky nebo nahrajte diktát.
                        </p>
                    </div>
                    <div>
                        <input
                            type="file"
                            accept="audio/*"
                            className="hidden"
                            id="audio-upload"
                            onChange={handleFileUpload}
                            disabled={isLoading}
                        />
                        <Button
                            variant="secondary"
                            size="sm"
                            onClick={() => document.getElementById("audio-upload")?.click()}
                            disabled={isLoading}
                        >
                            {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Loader2 className="h-4 w-4 mr-2" />}
                            {isLoading ? "Zpracovávám..." : "Nahrát diktát"}
                        </Button>
                    </div>
                </div>
                <Textarea
                    placeholder="Např.: Pacient (72 let) přichází pro dušnost. Anamnéza: HT, DM2..."
                    className="flex-1 resize-none font-mono text-sm bg-muted/50 focus:bg-background transition-colors"
                    value={input}
                    onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setInput(e.target.value)}
                />
                <Button
                    className="mt-4 w-full"
                    onClick={handleGenerate}
                    disabled={isLoading || !input.trim()}
                >
                    {isLoading ? (
                        <>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Generuji report...
                        </>
                    ) : (
                        <>
                            Generovat Epikrízu <ArrowRight className="ml-2 h-4 w-4" />
                        </>
                    )}
                </Button>
            </Card>

            {/* Output Column */}
            <Card className="flex flex-col p-4 border-border bg-card relative overflow-hidden">
                <div className="mb-4 flex justify-between items-center">
                    <h2 className="font-semibold text-lg">Výstupní zpráva</h2>
                    {output && (
                        <Button variant="outline" size="sm" onClick={() => navigator.clipboard.writeText(output)}>
                            Kopírovat
                        </Button>
                    )}
                </div>
                <div className="flex-1 overflow-auto rounded-md border border-border bg-muted/30 p-4 font-mono text-sm whitespace-pre-wrap">
                    {output ? (
                        output
                    ) : (
                        <div className="h-full flex flex-col items-center justify-center text-muted-foreground opacity-50">
                            <FileText className="h-12 w-12 mb-2" />
                            <p>Zde se objeví vygenerovaná epikríza</p>
                        </div>
                    )}
                </div>
            </Card>
        </div>
    )
}

