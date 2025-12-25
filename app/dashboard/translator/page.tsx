import { TranslatorInterface } from "@/components/dashboard/translator-interface"

export const metadata = {
    title: "Překladač | Czech MedAI",
    description: "Přesný lékařský překladač",
}

export default function TranslatorPage() {
    return (
        <div className="space-y-6 h-full flex flex-col">
            <div>
                <h1 className="text-3xl font-bold text-foreground">Lékařský Překladač</h1>
                <p className="text-muted-foreground mt-1">
                    Obousměrný překlad lékařských zpráv a dokumentace se zachováním terminologie.
                </p>
            </div>

            <div className="flex-1">
                <TranslatorInterface />
            </div>
        </div>
    )
}
