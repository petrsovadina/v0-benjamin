"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ThemeToggle } from "@/components/ui/theme-toggle"
import { useState } from "react"

export function SettingsInterface() {
  const [settings, setSettings] = useState({
    name: "MUDr. Jan Novák",
    email: "jan.novak@example.com",
    specialization: "Interní medicína",
    notifications: true,
    emailDigest: false,
  })

  return (
    <div className="space-y-6 max-w-2xl">
      {/* Profile section */}
      <Card className="p-6 bg-card border border-border space-y-4">
        <h2 className="text-lg font-semibold text-foreground">Profil</h2>

        <div className="space-y-3">
          <div>
            <label className="text-sm font-medium text-foreground">Jméno</label>
            <Input
              type="text"
              value={settings.name}
              onChange={(e) => setSettings({ ...settings, name: e.target.value })}
              className="mt-1 bg-input border-border text-foreground"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-foreground">Email</label>
            <Input
              type="email"
              value={settings.email}
              onChange={(e) => setSettings({ ...settings, email: e.target.value })}
              className="mt-1 bg-input border-border text-foreground"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-foreground">Specializace</label>
            <Input
              type="text"
              value={settings.specialization}
              onChange={(e) => setSettings({ ...settings, specialization: e.target.value })}
              className="mt-1 bg-input border-border text-foreground"
            />
          </div>
        </div>

        <Button className="bg-primary text-primary-foreground hover:bg-primary/90">Uložit změny</Button>
      </Card>

      <Card className="p-6 bg-card border border-border space-y-4">
        <h2 className="text-lg font-semibold text-foreground">Zobrazení</h2>

        <div className="space-y-3">
          <div className="flex flex-col gap-2">
            <p className="font-medium text-foreground">Režim vzhledu</p>
            <p className="text-sm text-muted-foreground mb-2">Zvolte si preferovaný témový režim</p>
            <ThemeToggle />
          </div>
        </div>
      </Card>

      {/* Preferences section */}
      <Card className="p-6 bg-card border border-border space-y-4">
        <h2 className="text-lg font-semibold text-foreground">Preference</h2>

        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 rounded-lg bg-muted/30">
            <div>
              <p className="font-medium text-foreground">Notifikace</p>
              <p className="text-sm text-muted-foreground">Dostávejte upozornění na nové odpovědi</p>
            </div>
            <input
              type="checkbox"
              checked={settings.notifications}
              onChange={(e) => setSettings({ ...settings, notifications: e.target.checked })}
              className="w-5 h-5 cursor-pointer"
            />
          </div>

          <div className="flex items-center justify-between p-3 rounded-lg bg-muted/30">
            <div>
              <p className="font-medium text-foreground">Email digest</p>
              <p className="text-sm text-muted-foreground">Týdenní souhrn nejčastějších dotazů</p>
            </div>
            <input
              type="checkbox"
              checked={settings.emailDigest}
              onChange={(e) => setSettings({ ...settings, emailDigest: e.target.checked })}
              className="w-5 h-5 cursor-pointer"
            />
          </div>
        </div>
      </Card>
    </div>
  )
}
