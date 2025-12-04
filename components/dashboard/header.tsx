"use client"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ThemeToggle } from "@/components/ui/theme-toggle"
import { useState, useEffect } from "react"

export function DashboardHeader() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-40">
        <div className="px-6 py-3 flex items-center justify-between gap-4">
          <div className="flex-1 max-w-md" />
          <div className="flex items-center gap-3">
            <div className="w-20 h-10 bg-muted rounded" />
            <div className="w-10 h-10 bg-muted rounded-full" />
          </div>
        </div>
      </header>
    )
  }

  return (
    <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-40">
      <div className="px-6 py-3 flex items-center justify-between gap-4">
        <div className="flex-1 max-w-md">
          <Input
            type="search"
            placeholder="Hledat v historii..."
            className="bg-input border-border text-foreground placeholder:text-muted-foreground"
          />
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" className="border-border hover:bg-muted hidden sm:inline-flex bg-transparent">
            Oznámení
          </Button>

          {/* Nahrazeno jednoduchým tlačítkem s ThemeToggle komponentou */}
          <ThemeToggle />

          <Button variant="ghost" className="w-10 h-10 rounded-full flex items-center justify-center hover:bg-muted">
            <div className="w-8 h-8 rounded-full bg-primary text-primary-foreground text-sm font-semibold flex items-center justify-center">
              JN
            </div>
          </Button>
        </div>
      </div>
    </header>
  )
}
