"use client"

import { useTheme } from "@/components/theme-provider"
import { useState, useEffect } from "react"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <div className="inline-flex items-center gap-1 p-1 bg-muted rounded-lg">
        <div className="w-8 h-8 rounded bg-muted-foreground/20 animate-pulse" />
        <div className="w-8 h-8 rounded bg-muted-foreground/20 animate-pulse" />
        <div className="w-8 h-8 rounded bg-muted-foreground/20 animate-pulse" />
      </div>
    )
  }

  const toggleTheme = (newTheme: "light" | "dark") => {
    setTheme(newTheme)
  }

  return (
    <div className="inline-flex items-center gap-1 p-1 bg-muted rounded-lg border border-border">
      {/* Light Mode Button */}
      <button
        onClick={() => toggleTheme("light")}
        className={`px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
          theme === "light"
            ? "bg-background text-foreground shadow-sm border border-border"
            : "text-muted-foreground hover:text-foreground hover:bg-background/50"
        }`}
        title="Světlý režim"
        aria-label="Přepnout na světlý režim"
      >
        <span className="flex items-center gap-2">
          <span className="text-lg">☀️</span>
          <span className="hidden sm:inline">Světlý</span>
        </span>
      </button>

      {/* Dark Mode Button */}
      <button
        onClick={() => toggleTheme("dark")}
        className={`px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
          theme === "dark"
            ? "bg-background text-foreground shadow-sm border border-border"
            : "text-muted-foreground hover:text-foreground hover:bg-background/50"
        }`}
        title="Tmavý režim"
        aria-label="Přepnout na tmavý režim"
      >
        <span className="flex items-center gap-2">
          <span className="text-lg">🌙</span>
          <span className="hidden sm:inline">Tmavý</span>
        </span>
      </button>
    </div>
  )
}
