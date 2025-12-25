import type React from "react"
import { DashboardWrapper } from "@/components/dashboard/dashboard-wrapper"
import { ErrorBoundary } from "@/components/error-boundary"

export const metadata = {
  title: "Dashboard | Czech MedAI",
  description: "Váš AI asistent pro klinické rozhodování",
}

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <DashboardWrapper>
      <ErrorBoundary>
        {children}
      </ErrorBoundary>
    </DashboardWrapper>
  )
}

