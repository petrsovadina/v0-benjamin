import Link from "next/link"
import { Button } from "@/components/ui/button"

const plans = [
  {
    name: "Free",
    price: "0",
    description: "Pro vyzkoušení základních funkcí",
    features: ["50 dotazů měsíčně", "Základní AI odpovědi", "PubMed citace", "Webové rozhraní"],
    cta: "Začít zdarma",
    popular: false,
  },
  {
    name: "Professional",
    price: "990",
    description: "Pro aktivní ambulantní lékaře",
    features: [
      "Neomezené dotazy",
      "VZP Navigator",
      "SÚKL databáze",
      "Historie dotazů",
      "Prioritní podpora",
      "CME kredity",
    ],
    cta: "Vybrat Professional",
    popular: true,
  },
  {
    name: "Premium",
    price: "1 990",
    description: "Pro náročné specialisty",
    features: [
      "Vše z Professional",
      "DeepConsult (20×/měsíc)",
      "API přístup",
      "Týmový účet (5 uživatelů)",
      "Personalizace",
      "Offline přístup",
    ],
    cta: "Vybrat Premium",
    popular: false,
  },
]

export function PricingSection() {
  return (
    <section id="cenik" className="py-24 md:py-32">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4 text-balance">Transparentní ceník</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-pretty">
            Vyberte si plán podle vašich potřeb. Bez skrytých poplatků.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative rounded-2xl border p-8 ${
                plan.popular ? "border-primary bg-primary/5 scale-105" : "border-border/60 bg-card/30"
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 rounded-full bg-primary text-primary-foreground text-sm font-medium">
                  Nejoblíbenější
                </div>
              )}
              <div className="text-center mb-8">
                <h3 className="text-xl font-semibold text-foreground mb-2">{plan.name}</h3>
                <div className="flex items-baseline justify-center gap-1 mb-2">
                  <span className="text-4xl font-bold text-foreground">{plan.price}</span>
                  <span className="text-muted-foreground">Kč/měsíc</span>
                </div>
                <p className="text-sm text-muted-foreground">{plan.description}</p>
              </div>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-3">
                    <span className="text-primary mt-0.5">✓</span>
                    <span className="text-sm text-foreground">{feature}</span>
                  </li>
                ))}
              </ul>

              <Link href="/auth/register">
                <Button
                  className={`w-full ${
                    plan.popular
                      ? "bg-primary text-primary-foreground hover:bg-primary/90"
                      : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
                  }`}
                >
                  {plan.cta}
                </Button>
              </Link>
            </div>
          ))}
        </div>

        {/* Enterprise CTA */}
        <div className="mt-16 text-center">
          <p className="text-muted-foreground mb-4">Potřebujete řešení pro celou nemocnici nebo síť ordinací?</p>
          <Link href="/kontakt">
            <Button variant="outline" size="lg">
              Kontaktujte nás pro Enterprise nabídku
            </Button>
          </Link>
        </div>
      </div>
    </section>
  )
}
