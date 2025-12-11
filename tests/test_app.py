import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import main  # noqa: E402
import taxonomy  # noqa: E402


def test_classify_text_detects_multiple_categories():
    text = (
        "El banco anunció una emisión de bonos para mejorar su infraestructura "
        "en la nube con inteligencia artificial."
    )
    categories = taxonomy.classify_text(text)
    assert categories == [
        "Finanzas/Banca",
        "Finanzas/Mercados",
        "Tecnología/IA",
        "Tecnología/Nube",
    ]


def test_extract_entities_uses_cached_nlp(monkeypatch):
    class DummyEnt:
        def __init__(self, text, label_):
            self.text = text
            self.label_ = label_

    class DummyDoc:
        def __init__(self, ents):
            self.ents = ents

    class DummyNLP:
        def __init__(self, ents):
            self._ents = ents

        def __call__(self, text):
            return DummyDoc(self._ents)

    dummy_ents = [
        DummyEnt("Banco de Costa Rica", "ORG"),
        DummyEnt("Analytica Labs", "ORG"),
        DummyEnt("Ana Pérez", "PERSON"),
        DummyEnt("San José", "GPE"),
    ]
    monkeypatch.setattr(main, "NLP", DummyNLP(dummy_ents))

    result = main.extract_entities("texto cualquiera")

    assert result == {
        "organizations": ["Analytica Labs", "Banco de Costa Rica"],
        "persons": ["Ana Pérez"],
        "locations": ["San José"],
    }


def test_extract_keywords_returns_requested_top_n():
    text = (
        "Analytica Labs y el Banco de Costa Rica colaboran para crear una "
        "plataforma cloud con foco en análisis de riesgo financiero."
    )
    keywords = main.extract_keywords(text, top_n=3)

    assert len(keywords) == 3
    for kw in keywords:
        assert set(kw.keys()) == {"keyword", "score"}
        assert isinstance(kw["keyword"], str)
        assert isinstance(kw["score"], float)


def test_enrich_text_combines_all_components(monkeypatch):
    sample_text = (
        "El banco prueba un modelo de inteligencia artificial en la nube."
    )
    fake_entities = {
        "organizations": ["Banco Demo"],
        "persons": [],
        "locations": [],
    }
    fake_keywords = [
        {"keyword": "banco", "score": 0.001},
        {"keyword": "nube", "score": 0.002},
    ]
    monkeypatch.setattr(main, "extract_entities", lambda text: fake_entities)
    monkeypatch.setattr(main, "extract_keywords", lambda text, top_n=10: fake_keywords)

    enriched = main.enrich_text(sample_text)

    assert enriched["text"] == sample_text
    assert enriched["entities"] == fake_entities
    assert enriched["keywords"] == fake_keywords
    assert "Finanzas/Banca" in enriched["categories"]
    assert "Tecnología/Nube" in enriched["categories"]
