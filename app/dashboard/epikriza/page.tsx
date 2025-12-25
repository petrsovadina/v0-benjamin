import { EpicrisisGenerator } from "@/components/dashboard/epicrisis-generator"

export const metadata = {
    title: "Generátor Epikrízy | Czech MedAI",
    description: "Automatické generování lékařských zpráv z poznámek",
}

export default function EpicrisisPage() {
    return (
        <div className="space-y-6 h-full flex flex-col">
            <div>
                <h1 className="text-3xl font-bold text-foreground">Generátor Epikrízy</h1>
                <p className="text-muted-foreground mt-1">
                    Převeďte své poznámky nebo přepis diktafonu do strukturované lékařské zprávy.
                </p>
            </div>

            <div className="flex-1">
                <EpicrisisGenerator />
            </div>
        </div>
    )
}
