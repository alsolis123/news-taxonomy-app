TAXONOMY = {
    "Finanzas/Banca": [
        "banco", "riesgo", "crédito", "hipoteca", "liquidez", "interés"
    ],
    "Finanzas/Mercados": [
        "bonos", "acciones", "mercado", "inversión", "emisión", "default"
    ],
    "Tecnología/Nube": [
        "nube", "cloud", "infraestructura", "servidores", "data center"
    ],
    "Tecnología/IA": [
        "inteligencia artificial", "ia", "machine learning",
        "modelo de lenguaje", "modelo generativo"
    ]
}


def classify_text(text: str) -> list[str]:
    """
    Clasifica un texto en categorías de la TAXONOMY
    usando simple matching de palabras clave.
    """
    text_lower = text.lower()
    categories = set()

    for category, keywords in TAXONOMY.items():
        for kw in keywords:
            if kw in text_lower:
                categories.add(category)
                break

    return sorted(categories)
