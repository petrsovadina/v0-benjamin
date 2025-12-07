import { SettingsInterface } from "@/components/dashboard/settings-interface"

export const metadata = {
  title: "Nastavení | Czech MedAI",
  description: "Nastavte si preferenci a profil",
}

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Nastavení</h1>
        <p className="text-muted-foreground mt-1">Spravujte svůj profil a preference aplikace</p>
      </div>
      <SettingsInterface />
    </div>
  )
}
