import Link from "next/link"
import { ForgotPasswordForm } from "@/components/auth/forgot-password-form"

export const metadata = {
  title: "Zapomenuté heslo | Czech MedAI",
  description: "Obnovte si heslo do Czech MedAI",
}

export default function ForgotPasswordPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold text-foreground">Zapomenuté heslo</h1>
        <p className="text-sm text-muted-foreground">Zadejte svůj email a my vám pošleme odkaz pro obnovení hesla</p>
      </div>

      {/* Form */}
      <ForgotPasswordForm />

      {/* Footer links */}
      <div className="flex justify-center gap-4 text-sm">
        <Link href="/auth/login" className="text-primary hover:underline font-medium">
          Zpět na přihlášení
        </Link>
      </div>
    </div>
  )
}
