"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"
import { signOut } from "@/lib/auth-actions"

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: "◆" },
  { href: "/dashboard/chat", label: "AI Chat", icon: "◆" },
  { href: "/dashboard/epikriza", label: "Generátor Epikrízy", icon: "◆" },
  { href: "/dashboard/translator", label: "Překladač", icon: "◆" },
  { href: "/dashboard/history", label: "Historie", icon: "◆" },
  { href: "/dashboard/vzp-navigator", label: "VZP Navigator", icon: "◆" },
  { href: "/dashboard/guidelines", label: "Guidelines Upload", icon: "◆" },
  { href: "/dashboard/settings", label: "Nastavení", icon: "◆" },
]

export function DashboardSidebar() {
  const pathname = usePathname()

  const handleSignOut = async () => {
    await signOut()
  }

  return (
    <aside className="w-64 border-r border-sidebar-border bg-sidebar min-h-screen flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-sidebar-border">
        <Link href="/dashboard" className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-lg bg-sidebar-primary flex items-center justify-center">
            <span className="text-sidebar-primary-foreground font-bold">CM</span>
          </div>
          <div className="flex-1">
            <div className="font-semibold text-sidebar-foreground text-sm">Czech MedAI</div>
            <div className="text-xs text-sidebar-accent-foreground/70">AI Asistent</div>
          </div>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link key={item.href} href={item.href}>
              <Button
                variant="ghost"
                className={`w-full justify-start gap-3 ${isActive
                  ? "bg-sidebar-primary text-sidebar-primary-foreground hover:bg-sidebar-primary/90"
                  : "text-sidebar-accent-foreground hover:bg-sidebar-accent/50"
                  }`}
              >
                <span>{item.icon}</span>
                {item.label}
              </Button>
            </Link>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-sidebar-border space-y-3">
        <div className="p-3 rounded-lg bg-sidebar-accent/30 text-xs text-sidebar-foreground">
          <p className="font-medium mb-1">Tip</p>
          <p className="text-sidebar-accent-foreground/80">
            Zadejte svůj dotaz přirozeným jazykem a obdržíte odpověď s citacemi
          </p>
        </div>
        <Button
          onClick={handleSignOut}
          variant="outline"
          className="w-full border-sidebar-border text-sidebar-foreground hover:bg-sidebar-accent/30 bg-transparent"
        >
          Odhlásit se
        </Button>
      </div>
    </aside>
  )
}
