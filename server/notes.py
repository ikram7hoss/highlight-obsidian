from pathlib import Path
from config import NOTES_DIR, NOTE_NAME, COLORS


def create_note_if_missing(path: Path) -> None:
    """Create the note with one heading per color if it doesn't exist."""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        headings = "\n\n".join(f"## {h}" for h in COLORS.values())
        path.write_text(headings + "\n", encoding="utf-8")


def add_highlight(color: str, text: str, url: str, title: str) -> None:
    """Add a highlight under the heading that matches its color."""
    if color not in COLORS:
        raise ValueError(f"Unknown color: {color}")

    path = NOTES_DIR / NOTE_NAME
    create_note_if_missing(path)

    lines = path.read_text(encoding="utf-8").splitlines()
    heading = f"## {COLORS[color]}"
    clean_text = " ".join(text.split())  # remove line breaks
    entry = f"- {clean_text} ([{title}]({url}))"

    if heading not in lines:  # heading was deleted: add it back
        lines += ["", heading]

    start = lines.index(heading)

    # the section ends at the next "## " heading, or at the end of the file
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break

    # insert after the last non-empty line of the section
    insert_at = end
    while insert_at > start + 1 and lines[insert_at - 1].strip() == "":
        insert_at -= 1

    lines.insert(insert_at, entry)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Add a highlight to Obsidian")
    parser.add_argument("color", choices=COLORS)
    parser.add_argument("text")
    parser.add_argument("--url", default="https://example.com")
    parser.add_argument("--title", default="Example page")
    args = parser.parse_args()

    add_highlight(args.color, args.text, args.url, args.title)
    print("Saved.")