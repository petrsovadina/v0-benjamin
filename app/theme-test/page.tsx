"use client"

import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"
import { useState, useEffect } from "react"

export default function ThemeTestPage() {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return (
    <div className="min-h-screen bg-background text-foreground p-12">
      <div className="max-w-4xl mx-auto space-y-12">
        {/* Header */}
        <div className="space-y-4">
          <h1 className="text-4xl font-bold">Czech MedAI - Theme Test</h1>
          <p className="text-lg text-muted-foreground">
            Aktuální téma: <span className="font-semibold text-primary">{theme}</span>
          </p>
          <Button onClick={() => setTheme(theme === "light" ? "dark" : "light")} className="bg-primary">
            Přepnout na {theme === "light" ? "tmavý" : "světlý"} režim
          </Button>
        </div>

        {/* Color Palette */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold">Barevná paleta</h2>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <div className="h-24 rounded-lg bg-background border-2 border-border" />
              <p className="text-sm font-medium">background</p>
            </div>

            <div className="space-y-2">
              <div className="h-24 rounded-lg bg-card border-2 border-border" />
              <p className="text-sm font-medium">card</p>
            </div>

            <div className="space-y-2">
              <div className="h-24 rounded-lg bg-primary" />
              <p className="text-sm font-medium">primary</p>
            </div>

            <div className="space-y-2">
              <div className="h-24 rounded-lg bg-secondary border-2 border-border" />
              <p className="text-sm font-medium">secondary</p>
            </div>

            <div className="space-y-2">
              <div className="h-24 rounded-lg bg-muted border-2 border-border" />
              <p className="text-sm font-medium">muted</p>
            </div>

            <div className="space-y-2">
              <div className="h-24 rounded-lg bg-accent" />
              <p className="text-sm font-medium">accent</p>
            </div>

            <div className="space-y-2">
              <div className="h-24 rounded-lg bg-destructive" />
              <p className="text-sm font-medium">destructive</p>
            </div>

            <div className="space-y-2">
              <div className="h-24 rounded-lg bg-border" />
              <p className="text-sm font-medium">border</p>
            </div>

            <div className="space-y-2">
              <div className="h-24 rounded-lg bg-input border-2 border-border" />
              <p className="text-sm font-medium">input</p>
            </div>
          </div>
        </div>

        {/* Sidebar Colors */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold">Sidebar Barvy</h2>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <div className="h-24 rounded-lg bg-sidebar border-2 border-border" />
              <p className="text-sm font-medium">sidebar</p>
            </div>

            <div className="space-y-2">
              <div className="h-24 rounded-lg bg-sidebar-primary" />
              <p className="text-sm font-medium">sidebar-primary</p>
            </div>

            <div className="space-y-2">
              <div className="h-24 rounded-lg bg-sidebar-accent border-2 border-border" />
              <p className="text-sm font-medium">sidebar-accent</p>
            </div>
          </div>
        </div>

        {/* Typography */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold">Typografie</h2>

          <div className="space-y-4">
            <div>
              <h3 className="text-3xl font-bold">Heading 1</h3>
              <p className="text-sm text-muted-foreground">text-3xl font-bold</p>
            </div>

            <div>
              <h4 className="text-2xl font-bold">Heading 2</h4>
              <p className="text-sm text-muted-foreground">text-2xl font-bold</p>
            </div>

            <div>
              <p className="text-base">Body text</p>
              <p className="text-sm text-muted-foreground">text-base</p>
            </div>

            <div>
              <p className="text-sm text-muted-foreground">Muted text</p>
              <p className="text-xs text-muted-foreground">text-sm text-muted-foreground</p>
            </div>
          </div>
        </div>

        {/* Components */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold">Komponenty</h2>

          <div className="flex gap-4 flex-wrap">
            <Button>Primary</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="destructive">Destructive</Button>
          </div>
        </div>
      </div>
    </div>
  )
}
