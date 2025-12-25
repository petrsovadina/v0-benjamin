import Link from "next/link"
import { Button } from "@/components/ui/button"

export function HeroSection() {
  return (
    <section className="relative pt-32 pb-20 md:pt-40 md:pb-32 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-primary/20 rounded-full blur-[120px] opacity-50" />
      </div>

      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 rounded-full border border-border/60 bg-secondary/50 px-4 py-1.5 text-sm text-muted-foreground mb-8">
            <span>✨</span>
            <span>Nová generace klinické podpory</span>
          </div>

          {/* Headline */}
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight text-foreground mb-6">
            <span className="text-balance">AI asistent pro</span>
            <br />
            <span className="text-primary">české lékaře</span>
          </h1>

          {/* Subheadline */}
          <p className="mx-auto max-w-2xl text-lg md:text-xl text-muted-foreground mb-10 text-pretty">
            Evidence-based odpovědi do 5 sekund. Citace z PubMed, SÚKL a českých guidelines. Váš důvěryhodný partner pro
            klinická rozhodnutí.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Link href="/auth/register">
              <Button size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90 h-12 px-8 text-base">
                Začít zdarma →
              </Button>
            </Link>
            <Link href="#jak-to-funguje">
              <Button size="lg" variant="outline" className="h-12 px-8 text-base border-border/60 bg-transparent">
                Jak to funguje
              </Button>
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-3xl mx-auto">
            <div className="flex flex-col items-center gap-2">
              <div className="flex items-center gap-2 text-primary">
                <span>⏱</span>
                <span className="text-3xl font-bold text-foreground">&lt;5s</span>
              </div>
              <span className="text-sm text-muted-foreground">Průměrná doba odpovědi</span>
            </div>
            <div className="flex flex-col items-center gap-2">
              <div className="flex items-center gap-2 text-primary">
                <span>📚</span>
                <span className="text-3xl font-bold text-foreground">29M+</span>
              </div>
              <span className="text-sm text-muted-foreground">Článků v databázi</span>
            </div>
            <div className="flex flex-col items-center gap-2">
              <div className="flex items-center gap-2 text-primary">
                <span>🔒</span>
                <span className="text-3xl font-bold text-foreground">100%</span>
              </div>
              <span className="text-sm text-muted-foreground">GDPR compliant</span>
            </div>
          </div>
        </div>

        {/* Chat Preview */}
        <div className="mt-20 relative">
          <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent z-10 pointer-events-none" />
          <div className="rounded-xl border border-border/60 bg-card/50 backdrop-blur-sm overflow-hidden shadow-2xl">
            <div className="flex items-center gap-2 px-4 py-3 border-b border-border/40 bg-secondary/30">
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-destructive/60" />
                <div className="w-3 h-3 rounded-full bg-chart-4/60" />
                <div className="w-3 h-3 rounded-full bg-chart-3/60" />
              </div>
              <span className="text-sm text-muted-foreground ml-2">Czech MedAI Chat</span>
            </div>
            <div className="p-6 space-y-4">
              {/* User message */}
              <div className="flex justify-end">
                <div className="max-w-md rounded-2xl rounded-br-md bg-primary/20 px-4 py-3">
                  <p className="text-sm text-foreground">Jaké jsou interakce mezi warfarinem a ibuprofenem?</p>
                </div>
              </div>
              {/* AI response */}
              <div className="flex justify-start">
                <div className="max-w-lg rounded-2xl rounded-bl-md bg-secondary/50 px-4 py-3">
                  <p className="text-sm text-foreground mb-3">
                    Warfarin a ibuprofen mají klinicky významnou interakci. NSAID jako ibuprofen zvyšují riziko krvácení
                    při současném užívání s warfarinem prostřednictvím dvou mechanismů:
                  </p>
                  <ul className="text-sm text-foreground space-y-1 mb-3 list-disc list-inside">
                    <li>Inhibice syntézy tromboxanu A2 v trombocytech</li>
                    <li>Gastrointestinální toxicita NSAID</li>
                  </ul>
                  <div className="flex flex-wrap gap-2 text-xs">
                    <span className="px-2 py-1 rounded bg-primary/20 text-primary">PMID: 12345678</span>
                    <span className="px-2 py-1 rounded bg-primary/20 text-primary">SÚKL SPC</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
