const testimonials = [
  {
    quote:
      "Czech MedAI mi šetří hodiny každý týden. Konečně nástroj, který rozumí českému kontextu a zná naše guidelines.",
    author: "MUDr. Jana Nováková",
    role: "Praktická lékařka, Praha",
    rating: 5,
  },
  {
    quote:
      "DeepConsult je fantastický pro komplexní případy. Dostanu kompletní rešerši s citacemi za pár minut místo hodin.",
    author: "MUDr. Petr Svoboda",
    role: "Kardiolog, FN Motol",
    rating: 5,
  },
  {
    quote:
      "Na urgentním příjmu potřebuji rychlé a spolehlivé odpovědi. Czech MedAI dodává přesně to - evidence-based a okamžitě.",
    author: "MUDr. Martin Kučera",
    role: "Urgentní příjem, IKEM",
    rating: 5,
  },
]

export function TestimonialsSection() {
  return (
    <section id="reference" className="py-24 md:py-32 bg-secondary/10">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4 text-balance">Co říkají lékaři</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-pretty">
            Připojte se k stovkám lékařů, kteří již používají Czech MedAI
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="p-8 rounded-2xl border border-border/60 bg-card/30">
              <div className="flex gap-1 mb-4">
                {Array.from({ length: testimonial.rating }).map((_, i) => (
                  <span key={i} className="text-lg">
                    ⭐
                  </span>
                ))}
              </div>
              <blockquote className="text-foreground mb-6 leading-relaxed">
                &ldquo;{testimonial.quote}&rdquo;
              </blockquote>
              <div>
                <div className="font-semibold text-foreground">{testimonial.author}</div>
                <div className="text-sm text-muted-foreground">{testimonial.role}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
