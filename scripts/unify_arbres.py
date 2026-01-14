import json
from pathlib import Path

PARIS_FILE = Path("data-raw") / "arbres_paris.json"
IDF_FILE = Path("data") / "arbres-remarquables-du-territoire-des-hauts-de-seine-hors-proprietes-privees.json"
OUT_FILE = Path("data") / "arbres.json"


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_paris(record: dict) -> dict:
    fields = record.get("fields", record)
    return {
        "source": "paris",
        "id": record.get("recordid"),
        "commune": "Paris",
        "espece": fields.get("libellefrancais"),
        "genre": fields.get("genre"),
        "hauteur": fields.get("hauteurenm"),
        "circonference": fields.get("circonferenceencm"),
        "remarquable": False,
    }


def normalize_idf(record: dict) -> dict:
    return {
        "source": "idf",
        "id": record.get("code_insee"),
        "commune": record.get("commune"),
        "espece": record.get("espece"),
        "genre": record.get("genre"),
        "hauteur": record.get("hauteur"),
        "circonference": record.get("circonference"),
        "remarquable": True,
    }


def main():
    arbres = []

    # --- PARIS ---
    paris_data = load_json(PARIS_FILE)
    if isinstance(paris_data, dict) and "records" in paris_data:
        paris_records = paris_data["records"]
    else:
        paris_records = paris_data

    for r in paris_records:
        arbres.append(normalize_paris(r))

    # --- IDF ---
    idf_data = load_json(IDF_FILE)
    for r in idf_data:
        arbres.append(normalize_idf(r))

    OUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(arbres, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(arbres)} arbres unifiés dans {OUT_FILE}")


if __name__ == "__main__":
    main()
