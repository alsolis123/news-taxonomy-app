# News Taxonomy App

Aplicación CLI en Python que enriquece noticias en español:
- Extrae entidades (organizaciones, personas y lugares) usando spaCy.
- Detecta palabras clave con YAKE.
- Clasifica el texto según una taxonomía simple (`src/taxonomy.py`).

## Requisitos

- Python 3.10+ (probado con 3.12).
- `pip` para instalar dependencias.

## Instalación

```bash
git clone https://github.com/tu-usuario/news-taxonomy-app.git
cd news-taxonomy-app

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements-dev.txt
python -m spacy download es_core_news_md  # solo si el wheel falla
```

Si preferís instalar solo las dependencias de ejecución, usá `pip install -r src/requirements.txt`.

## Uso

Texto como argumento:

```bash
python src/main.py --text "Un banco anunció una alianza con una entidad regional para desplegar modelos de riesgo en la nube."
```

Ingreso manual (stdin):

```bash
python src/main.py
# pegá la noticia y cerrá con Ctrl+D (Linux/Mac) o Ctrl+Z + Enter (Windows)
```

La salida es JSON con las claves:
- `text`: texto original.
- `entities.organizations/persons/locations`: entidades detectadas.
- `keywords`: lista de palabras clave con puntaje YAKE.
- `categories`: categorías de la taxonomía que matchean.

## Tests

La suite usa `pytest`. Ejecutala con el entorno virtual activado:

```bash
pytest
```

Incluye pruebas para la taxonomía, la extracción de entidades/palabras clave y el pipeline `enrich_text` con mocks para mantener determinismo.

## Más ideas

- Ajustar la taxonomía a verticales específicas (ej. banca, seguros, risk consulting).
- Procesar lotes desde CSV/JSON y guardar resultados enriquecidos.
- Empaquetar como servicio web o función serverless.
