#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup_showcase.py
Creates a complete, JSON-driven Tinkercad showcase site with filters & slideshow,
plus class roster CSV templates you can fill to generate projects.json.

USAGE:
  python setup_showcase.py                # creates showcase structure and empty templates
  python setup_showcase.py --seed 2       # also seeds 2 placeholder projects per class
  python setup_showcase.py --build-json   # build projects.json from rosters/*.csv
Requires: Python 3.8+
"""

import csv
import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from textwrap import dedent

# ---------- CONFIG: Your classes (from your message) ----------
RAW_CLASSES = [
    {"name": "Gonzalez-ULTIMATE", "count": 150, "created": "2025-09-15"},
    {"name": "Rise - 2-8", "count": 100, "created": "2025-09-05"},
    {"name": "RM325 - G5 - Omicron", "count": 25, "created": "2025-09-05"},
    {"name": "RM324 - G5 - Xi", "count": 25, "created": "2025-09-05"},
    {"name": "RM234 - G4 - Nu", "count": 25, "created": "2025-09-05"},
    {"name": "RM235 - G4 - Mu", "count": 25, "created": "2025-09-05"},
    {"name": "RM234 - G4 - Lambda", "count": 25, "created": "2025-09-05"},
    {"name": "RM225 - G3 - Kappa", "count": 25, "created": "2025-09-05"},
    {"name": "RM224 - G3 - Iota", "count": 25, "created": "2025-09-05"},
    {"name": "RM222 - G2 - Theta", "count": 25, "created": "2025-09-05"},
    {"name": "RM220 - G2 - Eta", "count": 25, "created": "2025-09-05"},
    {"name": "RM223 - G2 - Zeta", "count": 25, "created": "2025-09-05"},
    {"name": "RM143 - G1 - Epsilon", "count": 25, "created": "2025-09-05"},
    {"name": "RM142 - G1 - Delta", "count": 25, "created": "2025-09-05"},
    {"name": "RM141 - G1 - Gamma", "count": 25, "created": "2025-09-05"},
]

# ---------- Helpers to derive Grade from class name ----------
GRADE_RE = re.compile(r"\bG(\d)\b")

def derive_grade_label(class_name: str) -> str:
    """
    Returns a grade label like 'Grade 3' or 'Multi (2–8)'.
    """
    m = GRADE_RE.search(class_name)
    if m:
        return f"Grade {m.group(1)}"
    # special multi-grade
    if "2-8" in class_name or "2–8" in class_name:
        return "Multi (2–8)"
    # ULTIMATE (assume multi)
    if "ULTIMATE" in class_name.upper():
        return "Multi"
    return "Other"

def normalize_id(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s

# ---------- Files & structure ----------
ROOT = Path.cwd() / "showcase"
DATA_DIR = ROOT / "data"
ROSTERS_DIR = ROOT / "rosters"
IMAGES_DIR = ROOT / "images"

INDEX_HTML_PATH = ROOT / "index.html"
PROJECTS_JSON_PATH = ROOT / "projects.json"
README_PATH = ROOT / "README.md"

SCHEMA_PATH = ROOT / "projects.schema.json"

def ensure_dirs():
    for d in (ROOT, DATA_DIR, ROSTERS_DIR, IMAGES_DIR):
        d.mkdir(parents=True, exist_ok=True)

# ---------- HTML (data-driven; fetches projects.json) ----------
INDEX_HTML = dedent(r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>STEM Tinkercad Showcase</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="Interactive gallery and slideshow of student Tinkercad projects by grade and class." />
  <style>
    :root {
      --bg: #0f172a; --card: #111827; --muted: #94a3b8; --text: #e5e7eb;
      --accent: #22c55e; --accent-2: #06b6d4; --border: #243041;
      --chip: #1f2937; --chip-active: #0ea5e9; --shadow: 0 10px 25px rgba(0,0,0,0.35);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background:
        radial-gradient(1200px 800px at 10% -10%, rgba(34,197,94,0.06), transparent 50%),
        radial-gradient(1000px 600px at 110% 10%, rgba(6,182,212,0.08), transparent 50%),
        var(--bg);
      color: var(--text);
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Inter, "Helvetica Neue", Arial, Noto Sans, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", sans-serif;
      line-height: 1.5;
    }
    header { padding: 28px 22px 8px; max-width: 1200px; margin: 0 auto; }
    h1 { margin: 0 0 6px; font-size: clamp(1.5rem, 1.1rem + 1.8vw, 2.6rem); }
    .subtitle { color: var(--muted); font-size: 0.98rem; }

    .toolbar {
      display: grid; gap: 12px; grid-template-columns: 1fr auto; align-items: center;
      max-width: 1200px; margin: 16px auto 10px; padding: 0 22px;
    }
    .filters { display: flex; flex-wrap: wrap; gap: 8px; }
    .chip {
      border: 1px solid var(--border); background: var(--chip); color: var(--text);
      padding: 6px 12px; border-radius: 999px; cursor: pointer; font-size: 0.92rem;
      transition: transform .08s ease, background .2s ease, color .2s ease, border-color .2s ease;
      user-select: none;
    }
    .chip:hover { transform: translateY(-1px); }
    .chip.active { background: rgba(14,165,233,0.18); border-color: var(--chip-active); color: #e0f2fe; }

    .controls { display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-end; align-items: center; }
    .btn { background: linear-gradient(135deg, rgba(34,197,94,0.18), rgba(6,182,212,0.18)); color: #d1fae5; border: 1px solid var(--border); border-radius: 10px; padding: 8px 12px; font-weight: 600; cursor: pointer; transition: transform .08s ease, filter .2s ease; backdrop-filter: blur(6px); }
    .btn:hover { transform: translateY(-1px); filter: brightness(1.1); }

    .bar { max-width: 1200px; margin: 0 auto; padding: 6px 22px 12px; display: grid; grid-template-columns: 1fr auto auto; gap: 10px; align-items: center; }
    .input { background: #0c1424; border: 1px solid var(--border); color: var(--text); border-radius: 10px; padding: 8px 12px; min-width: 160px; }
    .select { background: #0c1424; border: 1px solid var(--border); color: var(--text); border-radius: 10px; padding: 8px 12px; }
    .count { color: var(--muted); font-size: 0.92rem; }

    .grid {
      max-width: 1200px; margin: 8px auto 64px; padding: 0 22px;
      display: grid; gap: 16px; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    }
    .card {
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border: 1px solid var(--border); border-radius: 14px; overflow: hidden; box-shadow: var(--shadow);
      transition: transform .08s ease, box-shadow .2s ease, border-color .2s ease; cursor: pointer; position: relative;
    }
    .card:hover { transform: translateY(-2px); border-color: #2b3b51; box-shadow: 0 12px 28px rgba(0,0,0,0.45); }
    .thumb { width: 100%; aspect-ratio: 4/3; object-fit: cover; background: #0b1220; display: block; }
    .placeholder { width: 100%; aspect-ratio: 4/3; display: grid; place-items: center; background:
        repeating-conic-gradient(from 0deg, #0b1220 0 10deg, #0d1422 10deg 20deg); color: #a5b4fc; font-weight: 600; font-size: 0.95rem; }
    .meta { padding: 12px 14px 14px; display: grid; gap: 4px; font-size: 0.95rem; }
    .title { font-weight: 700; }
    .sub { color: var(--muted); font-size: 0.9rem; }

    /* Modal / Slideshow */
    .overlay { position: fixed; inset: 0; background: rgba(2,6,23,0.84); backdrop-filter: blur(4px); display: none; align-items: center; justify-content: center; z-index: 1000; }
    .overlay.open { display: flex; }
    .viewer { width: min(1200px, 94vw); height: min(80vh, 70vw); background: #0b1220; border: 1px solid var(--border); border-radius: 16px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.6); position: relative; display: grid; grid-template-rows: auto 1fr auto; }
    .viewer header { display: flex; align-items: center; gap: 16px; padding: 10px 12px; width: 100%; }
    .viewer h3 { margin: 0; font-size: 1.05rem; }
    .viewer .tag { color: #93c5fd; font-size: 0.9rem; }
    .spacer { flex: 1; }
    .viewer .ctrl { display: flex; gap: 8px; }
    .viewer .ctrl .btn { background: rgba(255,255,255,0.06); color: #e2e8f0; border: 1px solid var(--border); padding: 6px 10px; border-radius: 8px; }
    .frame-wrap { position: relative; width: 100%; height: 100%; background: #0b1220; }
    iframe { width: 100%; height: 100%; border: 0; }

    .nav { position: absolute; inset: 0; pointer-events: none; }
    .nav button { pointer-events: auto; position: absolute; top: 50%; transform: translateY(-50%); width: 48px; height: 48px; border-radius: 50%; border: 1px solid var(--border); background: rgba(2,6,23,0.55); color: #e5e7eb; display: grid; place-items: center; cursor: pointer; transition: transform .08s ease, filter .2s ease; box-shadow: var(--shadow); }
    .nav button:hover { transform: translateY(-50%) scale(1.05); filter: brightness(1.1); }
    .nav .prev { left: 12px; }
    .nav .next { right: 12px; }
    .footer { display: flex; justify-content: space-between; align-items: center; gap: 12px; padding: 10px 12px; border-top: 1px solid var(--border); color: var(--muted); font-size: 0.9rem; }
    .status { color: #a7f3d0; }
    .hint { color: #94a3b8; }

    @media (max-width: 640px) {
      .nav button { width: 40px; height: 40px; }
      .viewer { height: 76vh; }
      .bar { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <h1 id="pageTitle">STEM Tinkercad Showcase</h1>
    <div class="subtitle">Browse by grade or class; click any project to open the interactive viewer or start a slideshow.</div>
  </header>

  <div class="toolbar">
    <div class="filters" id="gradeFilters"></div>
    <div class="controls">
      <button class="btn" id="presentBtn" title="Start slideshow of current filter">Start Slideshow</button>
    </div>
  </div>

  <div class="bar">
    <select id="classSelect" class="select" title="Filter by class">
      <option value="__ALL__">All Classes</option>
    </select>
    <input id="searchBox" class="input" placeholder="Search (title, student, tags)…" />
    <select id="sortSelect" class="select" title="Sort">
      <option value="date-desc">Newest first</option>
      <option value="date-asc">Oldest first</option>
      <option value="title-asc">Title A→Z</option>
      <option value="student-asc">Student A→Z</option>
    </select>
    <div class="count" id="countText"></div>
  </div>

  <main class="grid" id="grid"></main>

  <!-- Modal / Slideshow -->
  <div class="overlay" id="overlay" aria-hidden="true">
    <div class="viewer" role="dialog" aria-modal="true" aria-label="Tinkercad Project Viewer">
      <header>
        <h3 id="viewerTitle">Project Title</h3>
        <span class="tag" id="viewerTag">Class</span>
        <div class="spacer"></div>
        <div class="ctrl">
          <button class="btn" id="autoBtn" title="Toggle autoplay">Auto</button>
          <button class="btn" id="closeBtn" title="Close (Esc)">Close</button>
        </div>
      </header>
      <div class="frame-wrap">
        <iframe id="viewerFrame" loading="lazy" allowfullscreen title="Tinkercad 3D Viewer" referrerpolicy="no-referrer"></iframe>
        <div class="nav">
          <button class="prev" id="prevBtn" aria-label="Previous">◀</button>
          <button class="next" id="nextBtn" aria-label="Next">▶</button>
        </div>
      </div>
      <div class="footer">
        <div class="status" id="status">1 / 1</div>
        <div class="hint">Tips: ◀ ▶ arrows • Space toggles autoplay • Esc to close</div>
      </div>
    </div>
  </div>

  <script>
    // ------- Load data -------
    const params = new URLSearchParams(location.search);
    let DATA = { meta:{ title:"STEM Tinkercad Showcase", autoplayMs:9000 }, projects:[], classes:[] };
    let ALL = []; let LIST = []; let CLASSES = []; let GRADES = [];
    let filterGrade = params.get('grade') || 'All';
    let filterClass = '__ALL__';
    let idx = 0; let autoplay = false; let timer = null;

    // Elements
    const pageTitle = document.getElementById('pageTitle');
    const gradeFilters = document.getElementById('gradeFilters');
    const classSelect = document.getElementById('classSelect');
    const searchBox = document.getElementById('searchBox');
    const sortSelect = document.getElementById('sortSelect');
    const gridEl = document.getElementById('grid');
    const countText = document.getElementById('countText');

    const overlay = document.getElementById('overlay');
    const viewerFrame = document.getElementById('viewerFrame');
    const viewerTitle = document.getElementById('viewerTitle');
    const viewerTag = document.getElementById('viewerTag');
    const status = document.getElementById('status');
    const closeBtn = document.getElementById('closeBtn');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const autoBtn = document.getElementById('autoBtn');
    const presentBtn = document.getElementById('presentBtn');

    init();
    async function init() {
      try {
        const res = await fetch('projects.json', { cache:'no-store' });
        if (!res.ok) throw new Error('projects.json not found');
        DATA = await res.json();
      } catch (e) {
        console.error(e);
        gridEl.innerHTML = `<div style="grid-column:1/-1;color:#fca5a5;background:#1f2937;padding:12px 14px;border:1px solid #374151;border-radius:10px;">
          Couldn't load <b>projects.json</b>. Make sure it's in the root next to <b>index.html</b>.
        </div>`;
        return;
      }

      pageTitle.textContent = DATA.meta?.title || 'STEM Tinkercad Showcase';
      ALL = (DATA.projects || []).map(p => ({ ...p, _q: (p.title + ' ' + p.student + ' ' + (p.tags||[]).join(' ') + ' ' + p.klass).toLowerCase() }));
      CLASSES = DATA.classes || [];
      GRADES = ['All', ...Array.from(new Set(CLASSES.map(c => c.grade))).sort((a,b)=> (a==='All')? -1 : (a>b?1:-1))];

      // Render grade chips
      renderGradeFilters();

      // Populate class select
      populateClasses();

      // Wire controls
      wireControls();

      // Initial render
      applyFilter();
    }

    function renderGradeFilters() {
      gradeFilters.innerHTML = '';
      GRADES.forEach(g => {
        const btn = document.createElement('button');
        btn.className = 'chip' + (g === filterGrade ? ' active' : '');
        btn.textContent = g;
        btn.onclick = () => { filterGrade = g; syncGradeChips(); populateClasses(); applyFilter(); };
        gradeFilters.appendChild(btn);
      });
    }
    function syncGradeChips() {
      Array.from(gradeFilters.children).forEach(ch => {
        ch.classList.toggle('active', ch.textContent === filterGrade);
      });
    }

    function populateClasses() {
      const classes = CLASSES.filter(c => filterGrade === 'All' || c.grade === filterGrade);
      classSelect.innerHTML = `<option value="__ALL__">All Classes${filterGrade!=='All'?' ('+filterGrade+')':''}</option>` +
        classes.map(c => `<option value="${escapeAttr(c.name)}">${escapeHtml(c.name)}</option>`).join('');
      filterClass = '__ALL__';
    }

    function wireControls() {
      classSelect.addEventListener('change', () => { filterClass = classSelect.value; applyFilter(); });
      searchBox.addEventListener('input', () => applyFilter());
      sortSelect.addEventListener('change', () => applyFilter());

      closeBtn.addEventListener('click', closeViewer);
      prevBtn.addEventListener('click', prev);
      nextBtn.addEventListener('click', next);
      autoBtn.addEventListener('click', toggleAutoplay);
      presentBtn.addEventListener('click', () => openViewer(0));
      overlay.addEventListener('click', (e) => { if (e.target === overlay) closeViewer(); });

      document.addEventListener('keydown', (e) => {
        if (!overlay.classList.contains('open')) return;
        if (e.key === 'Escape') { e.preventDefault(); closeViewer(); }
        if (e.key === 'ArrowLeft') { e.preventDefault(); prev(); }
        if (e.key === 'ArrowRight') { e.preventDefault(); next(); }
        if (e.key === ' ') { e.preventDefault(); toggleAutoplay(); }
      });
    }

    function applyFilter() {
      const q = (searchBox.value || '').toLowerCase().trim();

      LIST = ALL.filter(p => {
        const gradeMatch = (filterGrade === 'All') || (p.grade === filterGrade);
        const classMatch = (filterClass === '__ALL__') || (p.klass === filterClass);
        const searchMatch = !q || p._q.includes(q);
        return gradeMatch && classMatch && searchMatch;
      });

      // Sort
      const sort = sortSelect.value;
      LIST.sort((a, b) => {
        switch (sort) {
          case 'date-asc': return (a.date||'') < (b.date||'') ? -1 : 1;
          case 'date-desc': return (a.date||'') > (b.date||'') ? -1 : 1;
          case 'title-asc': return (a.title||'').localeCompare(b.title||'');
          case 'student-asc': return (a.student||'').localeCompare(b.student||'');
          default: return 0;
        }
      });

      renderGrid();
      countText.textContent = `${LIST.length} project${LIST.length!==1?'s':''}`;
    }

    function renderGrid() {
      gridEl.innerHTML = LIST.map((p, i) => cardTemplate(p, i)).join('');
      gridEl.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', () => openViewer(Number(card.getAttribute('data-idx'))));
      });
    }

    function cardTemplate(p, i) {
      const img = p.thumbnail && p.thumbnail.trim().length > 0
        ? `<img class="thumb" src="${escapeAttr(p.thumbnail)}" alt="${escapeAttr(p.title)} thumbnail" loading="lazy" />`
        : `<div class="placeholder">No thumbnail</div>`;
      const title = escapeHtml(p.title);
      const sub = `${escapeHtml(p.student)} • ${escapeHtml(p.klass)}`;

      return `
        <article class="card" data-idx="${i}" title="Open ${escapeAttr(p.title)}">
          ${img}
          <div class="meta">
            <div class="title">${title}</div>
            <div class="sub">${sub}</div>
          </div>
        </article>
      `;
    }

    function openViewer(i = 0) {
      if (LIST.length === 0) return;
      idx = ((i % LIST.length) + LIST.length) % LIST.length;
      updateViewer();
      overlay.classList.add('open');
      overlay.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }
    function closeViewer() {
      overlay.classList.remove('open');
      overlay.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      stopAutoplay();
      viewerFrame.src = 'about:blank';
    }
    function updateViewer() {
      const p = LIST[idx];
      viewerTitle.textContent = `${p.title} — ${p.student}`;
      viewerTag.textContent = `${p.klass} • ${p.grade}`;
      status.textContent = `${idx + 1} / ${LIST.length}`;
      viewerFrame.src = p.embedUrl;
    }
    function prev() { idx = (idx - 1 + LIST.length) % LIST.length; updateViewer(); }
    function next() { idx = (idx + 1) % LIST.length; updateViewer(); }
    function startAutoplay() { autoplay = true; autoBtn.textContent = 'Auto: ON'; timer = setInterval(next, DATA.meta?.autoplayMs || 9000); }
    function stopAutoplay() { autoplay = false; autoBtn.textContent = 'Auto'; if (timer) clearInterval(timer); timer = null; }
    function toggleAutoplay() { autoplay ? stopAutoplay() : startAutoplay(); }

    function escapeHtml(s) { return String(s ?? '').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m])); }
    function escapeAttr(s) { return String(s ?? '').replace(/"/g, '&quot;'); }
  </script>
</body>
</html>
""").strip("\n")

# ---------- JSON Schema (optional, for validation in editors) ----------
PROJECTS_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Tinkercad Showcase Projects",
    "type": "object",
    "properties": {
        "meta": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "updated": {"type": "string"},
                "autoplayMs": {"type": "number"}
            },
            "required": ["title"]
        },
        "classes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "grade": {"type": "string"},
                    "count": {"type": "number"},
                    "created": {"type": "string"}
                },
                "required": ["name", "grade"]
            }
        },
        "projects": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "student": {"type": "string"},
                    "klass": {"type": "string"},
                    "grade": {"type": "string"},
                    "thumbnail": {"type": "string"},
                    "embedUrl": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "date": {"type": "string"}
                },
                "required": ["id", "title", "student", "klass", "grade", "embedUrl"]
            }
        }
    },
    "required": ["meta", "classes", "projects"]
}

# ---------- README ----------
README_MD = dedent(f"""
# STEM Tinkercad Showcase

Data-driven, static site to showcase student Tinkercad projects by **grade** and **class**, with an **interactive slideshow**.

## Structure
```
showcase/
├── index.html          # Static site (fetches projects.json)
├── projects.json       # Your data (meta, classes, projects)
├── projects.schema.json# (Optional) JSON schema for validation in editors
├── rosters/            # CSV templates per class
└── images/             # Optional thumbnails
```

## Workflow

1. **Fill rosters** in `rosters/*.csv`:
   - Columns: id, title, student, klass, grade, thumbnail, embedUrl, tags, date
   - Use **first name + last initial** for privacy
   - Paste Tinkercad **embed** URLs (Share → Embed)

2. Build `projects.json` from CSV:
   ```bash
   python setup_showcase.py --build-json
   ```

3. Open `index.html` to preview locally.

4. **Publish on GitHub Pages**:
   - Create a repo and push the `showcase/` contents to it
   - GitHub → **Settings** → **Pages** → Deploy from `main` (root or `/docs`)
   - Share the Pages URL

## Tips
- Thumbnails are optional; use `images/` to store them.
- Slideshow auto-advance default is **9s** (change `meta.autoplayMs` in `projects.json`).
- URL supports a grade filter: `?grade=Grade%203`
""").strip("\n")

# ---------- Utility to write initial files ----------
def write_initial_files(seed_n: int = 0):
    ensure_dirs()

    # Build class list with derived grade
    classes = []
    for c in RAW_CLASSES:
        grade = derive_grade_label(c["name"])
        classes.append({
            "name": c["name"],
            "grade": grade,
            "count": c["count"],
            "created": c["created"]
        })

    # Write index.html
    INDEX_HTML_PATH.write_text(INDEX_HTML, encoding="utf-8")

    # Base projects.json
    base = {
        "meta": {
            "title": "STEM Tinkercad Showcase – 2025",
            "updated": str(date.today()),
            "autoplayMs": 9000
        },
        "classes": classes,
        "projects": []
    }

    # Optionally seed N placeholders per class for quick testing
    if seed_n > 0:
        for c in classes:
            klass = c["name"]
            grade = c["grade"]
            base["projects"].extend([
                {
                    "id": f"{normalize_id(klass)}-placeholder-{i+1}",
                    "title": f"Project {i+1}",
                    "student": f"Student {i+1}",
                    "klass": klass,
                    "grade": grade,
                    "thumbnail": "",
                    "embedUrl": "https://www.tinkercad.com/embed/XXXXXXXXX?autostart=true",
                    "tags": ["placeholder"],
                    "date": str(date.today())
                } for i in range(seed_n)
            ])

    PROJECTS_JSON_PATH.write_text(json.dumps(base, ensure_ascii=False, indent=2), encoding="utf-8")

    # Write schema & readme
    SCHEMA_PATH.write_text(json.dumps(PROJECTS_SCHEMA, ensure_ascii=False, indent=2), encoding="utf-8")
    README_PATH.write_text(README_MD, encoding="utf-8")

    # Write per-class CSV roster templates
    write_roster_templates(classes)

def write_roster_templates(classes):
    headers = ["id","title","student","klass","grade","thumbnail","embedUrl","tags","date"]
    for c in classes:
        path = ROSTERS_DIR / f"{normalize_id(c['name'])}.csv"
        if path.exists():
            # avoid overwriting any filled roster
            continue
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(headers)
            # One example row
            w.writerow([
                f"{normalize_id(c['name'])}-example-1",
                "Treehouse 01",
                "Ava G.",
                c["name"],
                c["grade"],
                "",  # thumbnail (optional)
                "https://www.tinkercad.com/embed/XXXXXXXXX?autostart=true",
                "treehouse;architecture",
                str(date.today())
            ])

# ---------- Build projects.json from rosters/*.csv ----------
def build_json_from_rosters():
    meta = {
        "title": "STEM Tinkercad Showcase – 2025",
        "updated": str(date.today()),
        "autoplayMs": 9000
    }
    # Reload classes with derived grades
    classes = []
    for c in RAW_CLASSES:
        classes.append({
            "name": c["name"],
            "grade": derive_grade_label(c["name"]),
            "count": c["count"],
            "created": c["created"]
        })

    projects = []
    headers = ["id","title","student","klass","grade","thumbnail","embedUrl","tags","date"]
    for csv_path in sorted(ROSTERS_DIR.glob("*.csv")):
        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Validate header
            if reader.fieldnames != headers:
                print(f"[WARN] {csv_path.name} has unexpected columns. Expected {headers} got {reader.fieldnames}")
            for row in reader:
                id_ = (row.get("id") or "").strip()
                title = (row.get("title") or "").strip()
                student = (row.get("student") or "").strip()
                klass = (row.get("klass") or "").strip()
                grade = (row.get("grade") or "").strip() or derive_grade_label(klass)
                thumbnail = (row.get("thumbnail") or "").strip()
                embed = (row.get("embedUrl") or "").strip()
                tags = [t.strip() for t in (row.get("tags") or "").replace(",", ";").split(";") if t.strip()]
                dt = (row.get("date") or "").strip()

                if not (id_ and title and student and klass and embed):
                    # skip incomplete lines
                    continue
                # Basic embed sanity check
                if "tinkercad.com/embed/" not in embed:
                    print(f"[WARN] {csv_path.name} row id={id_}: embedUrl is not an EMBED link.")
                projects.append({
                    "id": id_,
                    "title": title,
                    "student": student,
                    "klass": klass,
                    "grade": grade,
                    "thumbnail": thumbnail,
                    "embedUrl": embed,
                    "tags": tags,
                    "date": dt
                })

    data = {
        "meta": meta,
        "classes": classes,
        "projects": projects
    }
    PROJECTS_JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Wrote {PROJECTS_JSON_PATH} with {len(projects)} projects.")

# ---------- CLI ----------
def main():
    seed_n = 0
    build = False
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--seed", "-s"):
            i += 1
            seed_n = int(args[i])
        elif a in ("--build-json","-b"):
            build = True
        else:
            print(f"Unknown arg: {a}")
        i += 1

    if build:
        ensure_dirs()
        build_json_from_rosters()
        return

    write_initial_files(seed_n=seed_n)
    print(f"[OK] Created scaffold in: {ROOT}\n - index.html\n - projects.json\n - projects.schema.json\n - rosters/*.csv\n - images/ (place thumbnails here)")

if __name__ == "__main__":
    main()
