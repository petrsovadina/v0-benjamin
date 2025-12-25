const features = [
  {
    emoji: "💬",
    title: "AI Chat v češtině",
    description: "Ptejte se přirozeným jazykem. Odpovědi dostanete v češtině včetně odborné terminologie.",
  },
  {
    emoji: "📚",
    title: "Evidence-based citace",
    description: "Každá odpověď obsahuje odkazy na PubMed, SÚKL SPC a české guidelines s PMID/DOI.",
  },
  {
    emoji: "💳",
    title: "VZP Navigator",
    description: "Okamžitě zjistíte, zda je léčba hrazena z veřejného zdravotního pojištění.",
  },
  {
    emoji: "⚡",
    title: "Odpověď do 5 sekund",
    description: "Rychlé odpovědi i na složité klinické dotazy díky optimalizované RAG architektuře.",
  },
  {
    emoji: "🔒",
    title: "GDPR & MDR Ready",
    description: "Data hostována v EU, plná compliance s GDPR. Připraveno pro MDR certifikaci.",
  },
  {
    emoji: "🌐",
    title: "EHR Integrace",
    description: "REST API pro integraci s ICZ, CGM, Medisoft a dalšími českými EHR systémy.",
  },
  {
    emoji: "📄",
    title: "DeepConsult",
    description: "Hloubková analýza komplexních případů s podrobným rozborem a literární rešerší.",
  },
  {
    emoji: "🔔",
    title: "SÚKL Alerts",
    description: "Automatické notifikace o změnách v SPC, stažení šarží a nových varováních.",
  },
]

export function FeaturesSection() {
  return (
    <section id="funkce" className="py-24 md:py-32">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4 text-balance">
            Vše co potřebujete pro klinická rozhodnutí
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-pretty">
            Kompletní sada nástrojů navržená speciálně pro české lékaře
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group p-6 rounded-xl border border-border/60 bg-card/30 hover:bg-card/60 hover:border-primary/40 transition-all duration-300"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-2xl mb-4 group-hover:bg-primary/20 transition-colors">
                {feature.emoji}
              </div>
              <h3 className="text-lg font-semibold text-foreground mb-2">{feature.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
