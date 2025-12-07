import type React from "react"
import { DashboardWrapper } from "@/components/dashboard/dashboard-wrapper"

export const metadata = {
  title: "Dashboard | Czech MedAI",
  description: "Váš AI asistent pro klinické rozhodování",
}

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return <DashboardWrapper>{children}</DashboardWrapper>
}
