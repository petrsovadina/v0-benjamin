import Link from "next/link"
import { Button } from "@/components/ui/button"

export function CTASection() {
  return (
    <section className="py-24 md:py-32 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-primary/20 rounded-full blur-[100px] opacity-50" />
      </div>

      <div className="relative mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 text-center">
        <div className="inline-flex items-center gap-2 rounded-full border border-border/60 bg-secondary/50 px-4 py-1.5 text-sm text-muted-foreground mb-8">
          <span>✨</span>
          <span>50 dotazů zdarma každý měsíc</span>
        </div>

        <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-6 text-balance">
          Začněte používat Czech MedAI ještě dnes
        </h2>
        <p className="text-lg md:text-xl text-muted-foreground mb-10 max-w-2xl mx-auto text-pretty">
          Připojte se k nové generaci lékařů, kteří využívají AI pro lepší klinická rozhodnutí. Registrace trvá méně než
          minutu.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link href="/auth/register">
            <Button size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90 h-14 px-10 text-lg">
              Vytvořit účet zdarma →
            </Button>
          </Link>
          <Link href="/demo">
            <Button size="lg" variant="outline" className="h-14 px-10 text-lg border-border/60 bg-transparent">
              Naplánovat demo
            </Button>
          </Link>
        </div>

        <p className="mt-6 text-sm text-muted-foreground">Žádná kreditní karta. Bez závazků. Zrušíte kdykoliv.</p>
      </div>
    </section>
  )
}
