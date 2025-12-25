import Link from "next/link"
import { Suspense } from "react"
import { ResetPasswordForm } from "@/components/auth/reset-password-form"

export const metadata = {
  title: "Obnovit heslo | Czech MedAI",
  description: "Vytvořte si nové heslo do Czech MedAI",
}

export default function ResetPasswordPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold text-foreground">Obnovit heslo</h1>
        <p className="text-sm text-muted-foreground">Zadejte nové heslo pro váš účet</p>
      </div>

      {/* Form */}
      <Suspense fallback={<div>Loading...</div>}>
        <ResetPasswordForm />
      </Suspense>

      {/* Footer links */}
      <div className="flex justify-center gap-4 text-sm">
        <Link href="/auth/login" className="text-primary hover:underline font-medium">
          Zpět na přihlášení
        </Link>
      </div>
    </div>
  )
}
