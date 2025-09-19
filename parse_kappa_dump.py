#!/usr/bin/env python3
# parse_kappa_dump.py
# Parse a raw Tinkercad class page dump into a roster CSV for the showcase.

import re, csv, sys
from pathlib import Path
from datetime import date

RAW_FILE = Path("raw_kappa.txt")
OUT_DIR = Path("showcase/rosters")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_CSV = OUT_DIR / "rm225-g3-kappa.csv"

KLASS = "RM225 - G3 - Kappa"
GRADE = "Grade 3"

# Heuristics: a username line looks like Kappa_###; the title is usually on the line just above it.
USER_RE = re.compile(r"^Kappa_\d{3}$", re.I)
NO_TITLE = set([
    "Private","Edited","React","View in 3D","Upload Image","Tinker this","Download",
    "Share class link","Students","Activities","Designs","Moderation","Co-teachers",
    "Share to Classroom","Copy link","Change visibility to share","Report content",
    "Start Simulating","Editing Components","Wiring Components","View It","Place It",
    "Learn the Moves","undefined","Tomorrow's innovators are made today","Start Tinkering",
])

def normalize_id(*parts):
    s = "-".join(p for p in parts if p)
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def main():
    if not RAW_FILE.exists():
        sys.exit(f"Missing {RAW_FILE}. Put your pasted class text there.")

    lines = [ln.strip() for ln in RAW_FILE.read_text(encoding="utf-8").splitlines()]
    pairs = []
    prev = ""
    for ln in lines:
        if USER_RE.match(ln):
            user = ln
            title = prev.strip()
            if title and title not in NO_TITLE and not USER_RE.match(title):
                pairs.append((title, user))
        if ln:
            prev = ln

    # Deduplicate in order
    seen = set()
    unique = []
    for title, user in pairs:
        key = (title, user)
        if key not in seen:
            seen.add(key)
            unique.append((title, user))

    headers = ["id","title","student","klass","grade","thumbnail","embedUrl","tags","date"]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        for title, user in unique:
            student_priv = user  # Replace later with "First L."
            pid = normalize_id("rm225-g3-kappa", user, title[:40])
            tags = []
            if re.search(r"tree|house", title, re.I): tags.append("treehouse")
            if re.search(r"rocket|mars", title, re.I): tags.append("space")
            if re.search(r"circuit|wire|simulate|components", title, re.I): tags.append("circuits")
            w.writerow([
                pid,
                title,
                student_priv,
                KLASS,
                GRADE,
                "",  # thumbnail (optional)
                "",  # embedUrl (fill after you or students make public)
                ";".join(tags),
                str(date.today())
            ])

    print(f"[OK] Wrote {OUT_CSV} with {len(unique)} rows.")
    print("Next: Open the CSV, paste each student's Tinkercad *Embed* URL into the embedUrl column.")
    print("Then run:  python setup_showcase.py --build-json")

if __name__ == "__main__":
    main()
