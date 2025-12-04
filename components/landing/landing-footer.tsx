import Link from "next/link"

const footerLinks = {
  produkt: [
    { label: "Funkce", href: "#funkce" },
    { label: "Ceník", href: "#cenik" },
    { label: "API", href: "/api-docs" },
    { label: "Integrace", href: "/integrace" },
  ],
  spolecnost: [
    { label: "O nás", href: "/o-nas" },
    { label: "Blog", href: "/blog" },
    { label: "Kariéra", href: "/kariera" },
    { label: "Kontakt", href: "/kontakt" },
  ],
  pravni: [
    { label: "Ochrana soukromí", href: "/ochrana-soukromi" },
    { label: "Podmínky užití", href: "/podminky" },
    { label: "GDPR", href: "/gdpr" },
    { label: "Bezpečnost", href: "/bezpecnost" },
  ],
  podpora: [
    { label: "Dokumentace", href: "/docs" },
    { label: "FAQ", href: "/faq" },
    { label: "Podpora", href: "/podpora" },
    { label: "Status", href: "/status" },
  ],
}

export function LandingFooter() {
  return (
    <footer className="border-t border-border/40 bg-secondary/10">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-8">
          {/* Brand */}
          <div className="col-span-2 md:col-span-1">
            <Link href="/" className="flex items-center gap-2 mb-4">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary text-primary-foreground font-bold text-sm">
                CM
              </div>
              <span className="text-lg font-semibold text-foreground">Czech MedAI</span>
            </Link>
            <p className="text-sm text-muted-foreground">
              AI asistent pro české lékaře. Evidence-based odpovědi s citacemi.
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="font-semibold text-foreground mb-4">Produkt</h4>
            <ul className="space-y-2">
              {footerLinks.produkt.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-foreground mb-4">Společnost</h4>
            <ul className="space-y-2">
              {footerLinks.spolecnost.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-foreground mb-4">Právní</h4>
            <ul className="space-y-2">
              {footerLinks.pravni.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-foreground mb-4">Podpora</h4>
            <ul className="space-y-2">
              {footerLinks.podpora.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-12 pt-8 border-t border-border/40 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-muted-foreground">
            © {new Date().getFullYear()} Czech MedAI s.r.o. Všechna práva vyhrazena.
          </p>
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground">Hostováno v EU</span>
            <span className="text-sm text-muted-foreground">GDPR Compliant</span>
          </div>
        </div>
      </div>
    </footer>
  )
}
