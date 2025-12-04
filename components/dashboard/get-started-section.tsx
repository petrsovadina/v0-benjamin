import { Card } from "@/components/ui/card"
import Link from "next/link"

const guides = [
  {
    title: "Jak psát dotazy",
    description: "Naučte se psát efektivní klinické dotazy",
    href: "#",
  },
  {
    title: "VZP Navigator",
    description: "Zjistěte info o úhradách pojišťovny",
    href: "#",
  },
  {
    title: "Interpretace odpovědí",
    description: "Porozumějte citacím a zdrojům",
    href: "#",
  },
]

export function GetStartedSection() {
  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-foreground">Začínal jste</h2>
      {guides.map((guide) => (
        <Card
          key={guide.title}
          className="p-4 bg-card border border-border hover:border-primary/50 transition-colors cursor-pointer"
        >
          <Link href={guide.href} className="space-y-2">
            <h3 className="font-medium text-foreground">{guide.title}</h3>
            <p className="text-sm text-muted-foreground">{guide.description}</p>
          </Link>
        </Card>
      ))}
    </div>
  )
}
