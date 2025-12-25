import { LoginForm } from "@/components/auth/login-form"
import Link from "next/link"

export const metadata = {
  title: "Přihlášení | Czech MedAI",
  description: "Přihlaste se do Czech MedAI",
}

export default function LoginPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold text-foreground">Přihlášení</h1>
        <p className="text-sm text-muted-foreground">Přihlaste se ke svému účtu a pokračujte v práci s AI asistentem</p>
      </div>

      {/* Form */}
      <LoginForm />

      {/* Footer links */}
      <div className="flex flex-col gap-3 text-center text-sm">
        <p className="text-muted-foreground">
          Nemáte účet?{" "}
          <Link href="/auth/register" className="text-primary hover:underline font-medium">
            Registrujte se
          </Link>
        </p>
        <Link href="/auth/forgot-password" className="text-muted-foreground hover:text-primary transition-colors">
          Zapomněli jste heslo?
        </Link>
      </div>
    </div>
  )
}
