const steps = [
  {
    number: "01",
    emoji: "🔍",
    title: "Položte dotaz",
    description:
      "Napište svůj klinický dotaz přirozeným jazykem v češtině. Například: 'Jaká je první volba ATB u komunitní pneumonie?'",
  },
  {
    number: "02",
    emoji: "⚙️",
    title: "AI analýza",
    description: "Náš RAG systém prohledá PubMed, SÚKL databázi a české guidelines. Najde relevantní evidence.",
  },
  {
    number: "03",
    emoji: "✓",
    title: "Ověřená odpověď",
    description: "Dostanete strukturovanou odpověď s inline citacemi. Každé tvrzení je podloženo zdrojem.",
  },
]

export function HowItWorksSection() {
  return (
    <section id="jak-to-funguje" className="py-24 md:py-32 bg-secondary/10">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4 text-balance">Jak Czech MedAI funguje</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-pretty">
            Od dotazu k evidence-based odpovědi za méně než 5 sekund
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <div key={index} className="relative">
              <div className="flex flex-col items-center text-center">
                <div className="text-6xl font-bold text-primary/20 mb-4">{step.number}</div>
                <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10 text-primary mb-6 text-3xl">
                  {step.emoji}
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-3">{step.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{step.description}</p>
              </div>
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-24 right-0 translate-x-1/2 text-border">→</div>
              )}
            </div>
          ))}
        </div>

        {/* Data sources */}
        <div className="mt-20 p-8 rounded-2xl border border-border/60 bg-card/30">
          <h3 className="text-xl font-semibold text-foreground mb-6 text-center">Datové zdroje</h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-6">
            {[
              { name: "PubMed", count: "29M+" },
              { name: "SÚKL", count: "10K+" },
              { name: "ČLS JEP", count: "500+" },
              { name: "Cochrane", count: "8K+" },
              { name: "NICE", count: "2K+" },
            ].map((source) => (
              <div key={source.name} className="text-center">
                <div className="text-2xl font-bold text-primary mb-1">{source.count}</div>
                <div className="text-sm text-muted-foreground">{source.name}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
