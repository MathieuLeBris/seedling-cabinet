
import csv
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

BOM_DIR = ROOT / "hardware" / "bom"
COMPONENTS_FILE = BOM_DIR / "components.csv"
PINS_FILE = BOM_DIR / "pin_assignments.csv"
HARDWARE_FILE = ROOT / "docs" / "hardware.md"

CSV_DELIMITER = ";"

# Colonnes attendues
COMPONENT_COLUMNS = [
    "id",
    "name",
    "manufacturer",
    "reference",
    "supplier",
    "url",
    "quantity",
    "unit_price",
    "status",
    "pin_assignment_required",
    "interface",
    "notes",
]

PIN_COLUMNS = [
    "component_id",
    "component_name",
    "signal",
    "gpio",
    "interface",
    "direction",
    "status",
    "notes",
]

# ============================================================
# OUTILS
# ============================================================

def read_csv(path):
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=CSV_DELIMITER)

        if not reader.fieldnames:
            raise ValueError(f"Fichier CSV vide ou invalide : {path}")

        return list(reader)


def write_csv(path, columns, rows):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=columns,
            delimiter=CSV_DELIMITER,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)


def check_columns(path, columns):
    if not path.exists():
        return

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=CSV_DELIMITER)
        missing = [column for column in columns if column not in (reader.fieldnames or [])]

    if missing:
        raise ValueError(
            f"Colonnes manquantes dans {path.name} : {', '.join(missing)}"
        )


def is_true(value):
    return str(value).strip().lower() in ("true", "1", "yes", "oui", "vrai")


def md(value):
    """Échappe les caractères qui perturbent un tableau Markdown."""
    value = str(value or "").strip()
    return value.replace("|", "\\|").replace("\n", " ")


def make_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]

    for row in rows:
        lines.append("| " + " | ".join(md(value) for value in row) + " |")

    return "\n".join(lines)


# ============================================================
# 1. LECTURE ET CONTRÔLE DES COMPOSANTS
# ============================================================

def load_components():
    if not COMPONENTS_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {COMPONENTS_FILE}"
        )

    check_columns(COMPONENTS_FILE, COMPONENT_COLUMNS)
    components = read_csv(COMPONENTS_FILE)

    ids = [row["id"].strip() for row in components]

    if any(not component_id for component_id in ids):
        raise ValueError("Un composant possède un ID vide.")

    if len(ids) != len(set(ids)):
        raise ValueError("Des identifiants de composants sont en double.")

    return components


# ============================================================
# 2. SYNCHRONISATION DES AFFECTATIONS DE BROCHES
# ============================================================

def synchronize_pins(components):
    if not PINS_FILE.exists():
        write_csv(PINS_FILE, PIN_COLUMNS, [])

    check_columns(PINS_FILE, PIN_COLUMNS)
    pins = read_csv(PINS_FILE)

    existing_ids = {
        row["component_id"].strip()
        for row in pins
        if row["component_id"].strip()
    }

    added = 0

    for component in components:
        component_id = component["id"].strip()

        if not is_true(component["pin_assignment_required"]):
            continue

        if component_id not in existing_ids:
            pins.append({
                "component_id": component_id,
                "component_name": component["name"],
                "signal": "À définir",
                "gpio": "À définir",
                "interface": component["interface"],
                "direction": "À définir",
                "status": "À définir",
                "notes": "Ligne initiale à compléter",
            })

            existing_ids.add(component_id)
            added += 1

    # Complète les noms manquants sans modifier les affectations
    names = {
        row["id"].strip(): row["name"].strip()
        for row in components
    }

    for pin in pins:
        component_id = pin["component_id"].strip()

        if not pin["component_name"].strip():
            pin["component_name"] = names.get(component_id, "")

    write_csv(PINS_FILE, PIN_COLUMNS, pins)

    # Détecte les affectations devenues orphelines
    component_ids = set(names.keys())

    orphan_ids = sorted({
        pin["component_id"].strip()
        for pin in pins
        if pin["component_id"].strip() not in component_ids
    })

    if orphan_ids:
        print(
            "Attention : affectations sans composant correspondant : "
            + ", ".join(orphan_ids)
        )

    print(f"{added} composant(s) ajouté(s) dans pin_assignments.csv.")

    return pins


# ============================================================
# 3. GÉNÉRATION DES TABLEAUX MARKDOWN
# ============================================================

def generate_inventory_table(components):
    headers = [
        "ID",
        "Composant",
        "Fabricant",
        "Référence",
        "Quantité",
        "Statut",
    ]

    rows = [
        [
            c["id"],
            c["name"],
            c["manufacturer"],
            c["reference"],
            c["quantity"],
            c["status"],
        ]
        for c in components
    ]

    return make_table(headers, rows)


def generate_interfaces_table(components):
    headers = [
        "Composant",
        "Interface",
        "Fonction",
        "Affectation des broches",
    ]

    rows = []

    for component in components:
        interfaces = [
            value.strip()
            for value in component["interface"].split("|")
            if value.strip()
        ]

        for interface in interfaces:
            rows.append([
                component["name"],
                interface,
                component["notes"],
                "Oui" if is_true(component["pin_assignment_required"]) else "Non",
            ])

    return make_table(headers, rows)


def generate_pins_table(pins):
    headers = [
        "ID composant",
        "Composant",
        "Signal",
        "GPIO",
        "Interface",
        "Direction",
        "Statut",
        "Remarques",
    ]

    rows = [
        [
            p["component_id"],
            p["component_name"],
            p["signal"],
            p["gpio"],
            p["interface"],
            p["direction"],
            p["status"],
            p["notes"],
        ]
        for p in pins
    ]

    return make_table(headers, rows)


# ============================================================
# 4. MISE À JOUR DE HARDWARE.MD
# ============================================================

def replace_section(content, name, generated):
    start = f"<!-- {name}:START -->"
    end = f"<!-- {name}:END -->"

    if start not in content or end not in content:
        raise ValueError(
            f"Marqueurs {name} introuvables dans hardware.md."
        )

    before, remainder = content.split(start, 1)
    _, after = remainder.split(end, 1)

    return before + start + "\n" + generated + "\n" + end + after


def update_hardware(components, pins):
    if not HARDWARE_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {HARDWARE_FILE}"
        )

    content = HARDWARE_FILE.read_text(encoding="utf-8")

    tables = {
        "BOM": generate_inventory_table(components),
        "INTERFACES": generate_interfaces_table(components),
        "PINS": generate_pins_table(pins),
    }

    for name, table in tables.items():
        content = replace_section(content, name, table)

    HARDWARE_FILE.write_text(content, encoding="utf-8")

    print("hardware.md mis à jour avec succès.")


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():
    print("Génération de la documentation matérielle...")

    components = load_components()
    pins = synchronize_pins(components)

    update_hardware(components, pins)

    print("Génération terminée.")


if __name__ == "__main__":
    main()
