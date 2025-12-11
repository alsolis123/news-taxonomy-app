import argparse
import json
import spacy
import yake

from taxonomy import classify_text

# Carga del modelo de spaCy (español)
# Hay que asegurarse de haber corrido antes:
#   python -m spacy download es_core_news_md
NLP = spacy.load("es_core_news_md")


#this one uses the spacy model to identify companies, people and places
def extract_entities(text: str) -> dict:
    """
    Extrae entidades de tipo organización, persona y lugar.
    """
    doc = NLP(text)
    orgs = []
    persons = []
    locations = []

    for ent in doc.ents:
        if ent.label_ == "ORG":
            orgs.append(ent.text)
        elif ent.label_ in ("PER", "PERSON"):
            persons.append(ent.text)
        elif ent.label_ in ("LOC", "GPE"):
            locations.append(ent.text)

    return {
        "organizations": sorted(set(orgs)),
        "persons": sorted(set(persons)),
        "locations": sorted(set(locations)),
    }


def extract_keywords(text: str, top_n: int = 10) -> list[dict]:
    """
    Extrae palabras clave usando YAKE.
    """
    kw_extractor = yake.KeywordExtractor(lan="es", n=1, top=top_n)
    keywords = kw_extractor.extract_keywords(text)

    return [
        {"keyword": k, "score": float(score)}
        for k, score in keywords
    ]


def enrich_text(text: str) -> dict:
    """
    Pipeline completo:
      - entidades
      - keywords
      - categorías (taxonomía)
    """
    entities = extract_entities(text)
    keywords = extract_keywords(text)
    categories = classify_text(text)

    return {
        "text": text,
        "entities": entities,
        "keywords": keywords,
        "categories": categories,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Enriquecedor de noticias: entidades, keywords y taxonomía."
    )
    parser.add_argument(
        "--text",
        type=str,
        help="Texto de la noticia a procesar (si no se pasa, se lee de stdin).",
    )
    args = parser.parse_args()

    if args.text:
        text = args.text
    else:
        print("Pegá el texto de la noticia y luego Ctrl+D (Linux/Mac) o Ctrl+Z + Enter (Windows):")
        text = "".join(iter(input, ""))

    result = enrich_text(text) #the way to enrich the text
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
