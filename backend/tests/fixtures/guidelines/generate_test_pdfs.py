"""
Generate 3 different Czech guideline PDF formats for testing:
1. Standard text PDF (MS Word export style)
2. PDF with tables (dosage guidelines)
3. Multi-column PDF (journal format)

Run this script to generate test PDFs in the fixtures directory.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Frame, PageTemplate, BaseDocTemplate
)
from reportlab.pdfgen import canvas

# Directory for output
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def create_standard_text_pdf():
    """
    Create a standard text PDF simulating MS Word export.
    Simple paragraphs with headings - typical guideline format.
    """
    filename = os.path.join(OUTPUT_DIR, "standard_text_guideline.pdf")
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2.5*cm,
        leftMargin=2.5*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=10
    )
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=8
    )

    content = []

    # Title
    content.append(Paragraph(
        "Klinické doporučení pro léčbu diabetes mellitus 2. typu",
        title_style
    ))
    content.append(Spacer(1, 20))

    # Section 1
    content.append(Paragraph("1. Úvod", heading_style))
    content.append(Paragraph(
        "Toto klinické doporučení shrnuje aktuální poznatky a evidence-based přístupy "
        "k léčbě diabetes mellitus 2. typu v České republice. Cílem je poskytnout "
        "zdravotnickým pracovníkům praktický návod pro diagnostiku a terapii.",
        body_style
    ))
    content.append(Paragraph(
        "Diabetes mellitus 2. typu je metabolické onemocnění charakterizované "
        "chronickou hyperglykémií v důsledku poruchy sekrece inzulinu a/nebo "
        "inzulinové rezistence. Prevalence tohoto onemocnění v České republice "
        "neustále roste a dosahuje přibližně 8% populace.",
        body_style
    ))

    # Section 2
    content.append(Paragraph("2. Diagnostická kritéria", heading_style))
    content.append(Paragraph(
        "Diagnóza diabetes mellitus se stanovuje na základě následujících kritérií: "
        "glykémie nalačno ≥ 7,0 mmol/l, náhodná glykémie ≥ 11,1 mmol/l s příznaky, "
        "nebo HbA1c ≥ 48 mmol/mol (6,5%). Pro potvrzení diagnózy je nutné opakované "
        "měření s výjimkou jasných symptomů.",
        body_style
    ))

    # Section 3 - Treatment recommendations
    content.append(Paragraph("3. Léčebné cíle a doporučení", heading_style))
    content.append(Paragraph(
        "Cílová hodnota HbA1c by měla být individualizována podle věku pacienta, "
        "délky trvání diabetu, přítomnosti komplikací a rizika hypoglykémie. "
        "Pro většinu pacientů je doporučený cíl HbA1c < 53 mmol/mol (7,0%).",
        body_style
    ))
    content.append(Paragraph(
        "U pacientů s nově diagnostikovaným diabetem a bez kardiovaskulárních "
        "komplikací lze cílit na HbA1c < 48 mmol/mol (6,5%). Naopak u starších "
        "pacientů s komorbiditami může být přijatelný cíl HbA1c < 64 mmol/mol (8,0%).",
        body_style
    ))

    # Page 2
    content.append(PageBreak())

    # Section 4
    content.append(Paragraph("4. Farmakoterapie", heading_style))
    content.append(Paragraph(
        "Metformin zůstává lékem první volby pro většinu pacientů s diabetes mellitus "
        "2. typu. Začíná se dávkou 500 mg 1-2x denně s postupnou titrací do maximální "
        "dávky 3000 mg denně rozděleně. Kontraindikací je těžká renální insuficience "
        "(eGFR < 30 ml/min).",
        body_style
    ))
    content.append(Paragraph(
        "Při nedostatečné kompenzaci na monoterapii metforminem se přidává druhý "
        "antidiabetický lék. Volba závisí na přítomnosti kardiovaskulárního "
        "onemocnění, srdečního selhání, nebo chronického onemocnění ledvin.",
        body_style
    ))
    content.append(Paragraph(
        "SGLT2 inhibitory (empagliflozin, dapagliflozin, canagliflozin) jsou "
        "doporučeny u pacientů s prokázaným kardiovaskulárním onemocněním "
        "nebo vysokým kardiovaskulárním rizikem. Tyto léky snižují riziko "
        "kardiovaskulárních příhod a hospitalizace pro srdeční selhání.",
        body_style
    ))

    # Section 5
    content.append(Paragraph("5. Monitorování a follow-up", heading_style))
    content.append(Paragraph(
        "Kontrola HbA1c by měla být prováděna každé 3 měsíce u pacientů, kteří "
        "nedosahují cílových hodnot, a každých 6 měsíců u stabilizovaných pacientů. "
        "Pravidelně by měly být sledovány i lipidogram, jaterní testy, renální funkce "
        "a albuminurie.",
        body_style
    ))

    doc.build(content)
    return filename


def create_table_pdf():
    """
    Create a PDF with tables - typical for dosage guidelines.
    """
    filename = os.path.join(OUTPUT_DIR, "dosage_table_guideline.pdf")
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=15
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=12,
        spaceAfter=8
    )
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        spaceAfter=6
    )

    content = []

    # Title
    content.append(Paragraph(
        "Dávkovací doporučení antidiabetik",
        title_style
    ))
    content.append(Spacer(1, 10))

    # Introduction
    content.append(Paragraph(
        "Následující tabulky poskytují přehled doporučených dávek perorálních "
        "antidiabetik a GLP-1 agonistů pro léčbu diabetes mellitus 2. typu.",
        body_style
    ))

    # Table 1: Metformin dosing
    content.append(Paragraph("Tabulka 1: Dávkování metforminu", heading_style))

    metformin_data = [
        ['Fáze léčby', 'Dávka', 'Frekvence', 'Poznámky'],
        ['Zahájení', '500 mg', '1x denně', 'S večeří'],
        ['Týden 2', '500 mg', '2x denně', 'S jídlem'],
        ['Týden 3-4', '850-1000 mg', '2x denně', 'Dle tolerance'],
        ['Udržovací', '1000-1500 mg', '2x denně', 'Max. 3000 mg/den'],
        ['Renální insuf.', 'eGFR 30-60: max 1000mg', '2x denně', 'eGFR <30: kontraindikováno'],
    ]

    table1 = Table(metformin_data, colWidths=[3.5*cm, 4*cm, 3*cm, 5*cm])
    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    content.append(table1)
    content.append(Spacer(1, 15))

    # Table 2: SGLT2 inhibitors
    content.append(Paragraph("Tabulka 2: Dávkování SGLT2 inhibitorů", heading_style))

    sglt2_data = [
        ['Léčivo', 'Počáteční dávka', 'Maximální dávka', 'Úprava při renální insuf.'],
        ['Empagliflozin', '10 mg', '25 mg', 'eGFR <30: nepodávat nově'],
        ['Dapagliflozin', '5-10 mg', '10 mg', 'eGFR <25: nepodávat nově'],
        ['Canagliflozin', '100 mg', '300 mg', 'eGFR 30-60: max 100mg'],
        ['Ertugliflozin', '5 mg', '15 mg', 'eGFR <45: nepodávat'],
    ]

    table2 = Table(sglt2_data, colWidths=[3.5*cm, 3.5*cm, 3.5*cm, 5*cm])
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    content.append(table2)
    content.append(Spacer(1, 15))

    # Page 2
    content.append(PageBreak())

    # Table 3: GLP-1 agonists
    content.append(Paragraph("Tabulka 3: Dávkování GLP-1 agonistů", heading_style))

    glp1_data = [
        ['Léčivo', 'Forma podání', 'Počáteční dávka', 'Titrace', 'Cílová dávka'],
        ['Liraglutid', 's.c. 1x denně', '0.6 mg', '+0.6 mg/týden', '1.2-1.8 mg'],
        ['Semaglutid s.c.', 's.c. 1x týdně', '0.25 mg', '+0.25 mg/4 týdny', '0.5-1.0 mg'],
        ['Semaglutid p.o.', 'p.o. 1x denně', '3 mg', '+3-7 mg/4 týdny', '7-14 mg'],
        ['Dulaglutid', 's.c. 1x týdně', '0.75 mg', 'po 4 týdnech', '1.5-4.5 mg'],
        ['Tirzepatid', 's.c. 1x týdně', '2.5 mg', '+2.5 mg/4 týdny', '5-15 mg'],
    ]

    table3 = Table(glp1_data, colWidths=[3*cm, 3*cm, 3*cm, 3*cm, 3*cm])
    table3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    content.append(table3)
    content.append(Spacer(1, 15))

    # Additional notes
    content.append(Paragraph("Důležité poznámky:", heading_style))
    content.append(Paragraph(
        "• Všechny GLP-1 agonisty podávané subkutánně lze aplikovat do břicha, stehna nebo paže.",
        body_style
    ))
    content.append(Paragraph(
        "• Perorální semaglutid se musí užívat nalačno, nejméně 30 minut před prvním jídlem.",
        body_style
    ))
    content.append(Paragraph(
        "• Při kombinaci SGLT2 inhibitoru s inzulinem nebo sulfonylureou je třeba zvážit snížení dávky těchto léků pro prevenci hypoglykémie.",
        body_style
    ))

    doc.build(content)
    return filename


def create_multicolumn_pdf():
    """
    Create a multi-column PDF simulating journal article format.
    """
    filename = os.path.join(OUTPUT_DIR, "journal_multicolumn_guideline.pdf")

    # Custom document with two-column layout
    class TwoColumnDocTemplate(BaseDocTemplate):
        def __init__(self, filename, **kw):
            BaseDocTemplate.__init__(self, filename, **kw)
            # Two frames for two columns
            frame_width = (A4[0] - 3*cm) / 2 - 0.5*cm
            frame1 = Frame(
                1.5*cm, 2*cm, frame_width, A4[1] - 4*cm,
                id='col1', showBoundary=0
            )
            frame2 = Frame(
                1.5*cm + frame_width + 1*cm, 2*cm, frame_width, A4[1] - 4*cm,
                id='col2', showBoundary=0
            )
            self.addPageTemplates([
                PageTemplate(id='TwoCol', frames=[frame1, frame2])
            ])

    doc = TwoColumnDocTemplate(filename, pagesize=A4)

    styles = getSampleStyleSheet()

    # Journal-style styles
    abstract_style = ParagraphStyle(
        'Abstract',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        spaceAfter=6,
        fontStyle='italic'
    )
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading3'],
        fontSize=10,
        spaceBefore=10,
        spaceAfter=4,
        fontWeight='bold'
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        spaceAfter=4,
        alignment=4  # Justify
    )

    content = []

    # Abstract - spans both columns via first appearance
    content.append(Paragraph(
        "<b>ABSTRAKT</b>",
        section_style
    ))
    content.append(Paragraph(
        "Hypertenze je jedním z nejvýznamnějších modifikovatelných rizikových faktorů "
        "kardiovaskulárních onemocnění. Tento přehled shrnuje aktuální doporučení "
        "pro diagnostiku a léčbu arteriální hypertenze u dospělých pacientů v České "
        "republice. Cílové hodnoty krevního tlaku, volba farmakoterapie a nefarmakologické "
        "intervence jsou diskutovány v kontextu současné evidence.",
        abstract_style
    ))
    content.append(Spacer(1, 8))

    # Introduction
    content.append(Paragraph("<b>ÚVOD</b>", section_style))
    content.append(Paragraph(
        "Arteriální hypertenze postihuje přibližně 40% dospělé populace České republiky "
        "a představuje významný rizikový faktor pro vznik cévní mozkové příhody, "
        "ischemické choroby srdeční, srdečního selhání a chronického onemocnění ledvin. "
        "Adekvátní kontrola krevního tlaku významně snižuje kardiovaskulární morbiditu "
        "a mortalitu.",
        body_style
    ))
    content.append(Paragraph(
        "Diagnostika hypertenze vyžaduje opakované měření krevního tlaku při více "
        "návštěvách nebo potvrzení pomocí ambulantního 24hodinového monitorování "
        "krevního tlaku (ABPM). Za hypertenzi se považují hodnoty ≥ 140/90 mmHg "
        "při opakovaném měření v ordinaci.",
        body_style
    ))

    # Diagnostic criteria
    content.append(Paragraph("<b>DIAGNOSTICKÁ KRITÉRIA</b>", section_style))
    content.append(Paragraph(
        "Klasifikace hypertenze podle ESC/ESH 2023: Optimální TK < 120/80 mmHg, "
        "normální TK 120-129/80-84 mmHg, vysoký normální 130-139/85-89 mmHg. "
        "Hypertenze 1. stupně 140-159/90-99 mmHg, 2. stupně 160-179/100-109 mmHg, "
        "3. stupně ≥ 180/≥ 110 mmHg.",
        body_style
    ))
    content.append(Paragraph(
        "Při podezření na sekundární hypertenzi (náhlý vznik, rezistence na léčbu, "
        "hypokalémie) je indikováno vyšetření příčin včetně renovaskulární hypertenze, "
        "primárního hyperaldosteronismu a feochromocytomu.",
        body_style
    ))

    # Treatment targets
    content.append(Paragraph("<b>CÍLOVÉ HODNOTY</b>", section_style))
    content.append(Paragraph(
        "U většiny pacientů je doporučeno dosáhnout cílového TK < 140/90 mmHg. "
        "U pacientů mladších 65 let a pacientů s diabetem by měl být cílový "
        "systolický TK 120-130 mmHg, pokud je léčba tolerována.",
        body_style
    ))
    content.append(Paragraph(
        "U starších pacientů (≥ 65 let) je doporučen cílový systolický TK "
        "130-139 mmHg. U pacientů s chronickým onemocněním ledvin je cílový "
        "TK < 130/80 mmHg, zejména při přítomnosti albuminurie.",
        body_style
    ))

    # Pharmacotherapy
    content.append(Paragraph("<b>FARMAKOTERAPIE</b>", section_style))
    content.append(Paragraph(
        "Základními skupinami antihypertenziv jsou: ACE inhibitory nebo ARB, "
        "blokátory kalciových kanálů, thiazidová diuretika (včetně chlorthalidonu "
        "a indapamidu) a beta-blokátory. Volba závisí na přítomnosti komorbidit.",
        body_style
    ))
    content.append(Paragraph(
        "U většiny pacientů s hypertenzí 1. stupně a zvýšeným kardiovaskulárním "
        "rizikem je doporučeno zahájit léčbu kombinací dvou antihypertenziv "
        "v nízkých dávkách, ideálně jako fixní kombinace v jedné tabletě.",
        body_style
    ))
    content.append(Paragraph(
        "Preferovanými kombinacemi jsou: ACE-I nebo ARB + blokátor kalciových kanálů, "
        "ACE-I nebo ARB + thiazidové diuretikum. Kombinace ACE-I + ARB není doporučena.",
        body_style
    ))

    # Non-pharmacological
    content.append(Paragraph("<b>NEFARMAKOLOGICKÁ LÉČBA</b>", section_style))
    content.append(Paragraph(
        "Životospráva je základem léčby hypertenze. Doporučuje se omezení příjmu "
        "soli na < 5 g denně, redukce hmotnosti při nadváze nebo obezitě, "
        "pravidelná fyzická aktivita (30 min aerobního cvičení 5-7x týdně), "
        "omezení alkoholu a zanechání kouření.",
        body_style
    ))
    content.append(Paragraph(
        "DASH dieta bohatá na ovoce, zeleninu, celozrnné produkty a nízkotučné "
        "mléčné výrobky prokazatelně snižuje krevní tlak a měla by být doporučena "
        "všem pacientům s hypertenzí.",
        body_style
    ))

    # Conclusions
    content.append(Paragraph("<b>ZÁVĚR</b>", section_style))
    content.append(Paragraph(
        "Účinná léčba hypertenze vyžaduje kombinaci farmakologických a nefarmakologických "
        "intervencí, individualizaci terapie podle přítomnosti komorbidit a pravidelné "
        "monitorování dosažení cílových hodnot TK. Adherence pacienta k léčbě je klíčová "
        "pro dlouhodobý úspěch.",
        body_style
    ))

    doc.build(content)
    return filename


def main():
    """Generate all 3 test PDF formats."""
    print("Generating test PDF fixtures...")

    pdf1 = create_standard_text_pdf()
    print(f"  Created: {os.path.basename(pdf1)}")

    pdf2 = create_table_pdf()
    print(f"  Created: {os.path.basename(pdf2)}")

    pdf3 = create_multicolumn_pdf()
    print(f"  Created: {os.path.basename(pdf3)}")

    print(f"\nAll PDFs generated in: {OUTPUT_DIR}")
    return [pdf1, pdf2, pdf3]


if __name__ == "__main__":
    main()
