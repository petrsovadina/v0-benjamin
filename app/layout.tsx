import type React from "react"
import type { Metadata } from "next"
import { Inter, Geist_Mono } from "next/font/google"
import { ThemeProvider } from "@/components/theme-provider"
import { AuthProvider } from "@/lib/auth-context"
import { WebVitals } from "./_components/web-vitals"
import "./globals.css"

const _inter = Inter({ subsets: ["latin", "latin-ext"] })
const _geistMono = Geist_Mono({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Czech MedAI | AI Asistent pro České Lékaře",
  description:
    "Důvěryhodný AI asistent pro české lékaře. Evidence-based odpovědi s citacemi, VZP Navigator, integrace s EHR systémy.",
  generator: "v0.app",
  keywords: ["AI", "zdravotnictví", "lékaři", "Česká republika", "klinický asistent", "SÚKL", "VZP"],
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="cs" suppressHydrationWarning>
      <body className={`font-sans antialiased`}>
        <WebVitals />
        <ThemeProvider attribute="class" defaultTheme="light" enableSystem disableTransitionOnChange>
          <AuthProvider>{children}</AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
