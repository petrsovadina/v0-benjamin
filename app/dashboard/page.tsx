import { QuickStatsCards } from "@/components/dashboard/quick-stats-cards"
import { RecentQueries } from "@/components/dashboard/recent-queries"
import { GetStartedSection } from "@/components/dashboard/get-started-section"

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Vítejte v Czech MedAI</h1>
        <p className="text-muted-foreground mt-1">
          Váš AI asistent pro klinické dotazy s evidence-based odpověďmi a citacemi
        </p>
      </div>

      {/* Quick stats */}
      <QuickStatsCards />

      {/* Get started / Recent queries grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <GetStartedSection />
        <div className="lg:col-span-2">
          <RecentQueries />
        </div>
      </div>
    </div>
  )
}
