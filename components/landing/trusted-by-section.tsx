const partners = [
  { name: "FN Motol", emoji: "🏥" },
  { name: "IKEM", emoji: "🏢" },
  { name: "ČLK", emoji: "🎓" },
  { name: "VFN Praha", emoji: "🏥" },
  { name: "FN Brno", emoji: "🏥" },
]

export function TrustedBySection() {
  return (
    <section className="py-12 border-y border-border/40 bg-secondary/20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <p className="text-center text-sm text-muted-foreground mb-8 uppercase tracking-wider">
          Důvěřují nám lékaři z předních zdravotnických zařízení
        </p>
        <div className="flex flex-wrap items-center justify-center gap-8 md:gap-16">
          {partners.map((partner) => (
            <div
              key={partner.name}
              className="flex items-center gap-2 text-muted-foreground/60 hover:text-muted-foreground transition-colors"
            >
              <span className="text-2xl">{partner.emoji}</span>
              <span className="text-sm font-medium">{partner.name}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
