import { RegisterForm } from "@/components/auth/register-form"
import Link from "next/link"

export const metadata = {
  title: "Registrace | Czech MedAI",
  description: "Vytvořte si účet v Czech MedAI",
}

export default function RegisterPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold text-foreground">Registrace</h1>
        <p className="text-sm text-muted-foreground">Vytvořte si účet a začněte s Czech MedAI zdarma</p>
      </div>

      {/* Form */}
      <RegisterForm />

      {/* Footer links */}
      <div className="text-center text-sm">
        <p className="text-muted-foreground">
          Již máte účet?{" "}
          <Link href="/auth/login" className="text-primary hover:underline font-medium">
            Přihlaste se
          </Link>
        </p>
      </div>
    </div>
  )
}
