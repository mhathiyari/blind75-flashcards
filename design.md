# Blind 75 Flashcard App - Design Document

## Overview
A flashcard application to help revise the Blind 75 LeetCode problems. Each card displays a problem on the front with collapsible hints, and when flipped, shows a brief explanation of the approach followed by the solution code.

**Philosophy: Python-First** - This is a pure Python web application. JavaScript and CSS are used minimally (HTMX for interactivity, basic CSS for styling).

---

## Features Implemented

### Core Features ✅
- **49 LeetCode problems** from Blind 75 list with complete documentation
- Interactive flashcard interface with instant flip
- **Collapsible hints** on problem side (native HTML `<details>` elements)
- **Pseudocode sections** where available
- Answer side shows:
  1. Explanation of the approach/algorithm
  2. Solution code (Python)
- Navigate between cards (next/previous with wraparound)
- **Randomized problem order** on each server restart
- Progress tracking (X/49 counter)
- Category-based filtering (Arrays, Dynamic Programming, Trees, etc.)

### Additional Features ✅
- Dark theme UI optimized for extended study
- Responsive design for desktop and mobile
- Auto-updating navigation buttons (HTMX swaps)
- Clean, minimal interface

---

## Tech Stack (Final Implementation)

| Layer | Technology | Purpose |
|-------|------------|---------|
| Package Manager | `uv` | Modern Python package manager |
| Backend | FastAPI | Pure Python web framework |
| Templating | Jinja2 | Python-based templating engine |
| Interactivity | HTMX (CDN) | Declarative AJAX, no custom JS needed |
| Styling | Tailwind CSS (CDN) | Utility-first CSS, no build step |
| Animations | Pure CSS | Card hover effects, transitions |
| Data Storage | JSON file | All 49 problems with metadata |
| Data Parsing | Python script | Extracts problems from source repo |

**JavaScript Usage**: Only HTMX library (~14KB, declarative HTML attributes). Zero custom JavaScript written.

**CSS Usage**: Tailwind CSS via CDN + minimal custom CSS for card styling (~50 lines)

---

## Deployment

### Running Locally

**Development Mode:**
```bash
export PATH="$HOME/.local/bin:$PATH"
uv run uvicorn main:app --reload
# Opens at http://localhost:8000
```

**Production Mode:**
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Hosting Options
- **Railway** / **Render** / **Fly.io** (free tiers support Python/FastAPI)
- **Docker** containerization supported
- Self-hosted on any Linux/macOS server

---

## Data Structure

```python
# problems.json structure
{
  "id": int,
  "title": str,
  "difficulty": "Easy" | "Medium" | "Hard",
  "category": str,
  "description": str,
  "examples": list[str],
  "constraints": list[str],
  "hints": list[str],           # NEW: Collapsible hints
  "pseudocode": str,             # NEW: Algorithm pseudocode
  "explanation": str,
  "code": str                    # Python solution
}
```

---

## Project Structure (Actual)

```
experimental_cluade/
├── main.py                     # FastAPI app with all routes
├── parse_problems.py           # Script to generate problems.json
├── data/
│   └── problems.json           # All 49 problems
├── templates/
│   ├── base.html               # Base layout with Tailwind + HTMX
│   ├── index.html              # Main page with category filter
│   └── partials/
│       └── card.html           # Flashcard component (front/back)
├── static/                     # Empty (using CDN for styles)
├── blind_75_flashcard_app/     # Git submodule (source problems)
├── pyproject.toml              # uv dependencies
├── uv.lock                     # Locked dependencies
└── README.md                   # Installation & usage
```

---

## Problem Categories (Available)

Based on the 49 problems currently in the app:

1. **Arrays** (10 problems)
2. **Binary & Bit Manipulation** (4 problems)
3. **Dynamic Programming** (11 problems)
4. **Graphs** (1 problem)
5. **Intervals** (3 problems)
6. **Linked List** (5 problems)
7. **Matrix** (3 problems)
8. **String** (9 problems)
9. **Trees** (3 problems)

---

## API Routes

All routes implemented in `main.py`:

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Main page with first flashcard and category filter |
| `/card/{id}` | GET | Get specific card (front side) - HTMX partial |
| `/card/{id}/answer` | GET | Get card with solution (back side) - HTMX partial |
| `/next/{id}` | GET | Navigate to next card - HTMX partial |
| `/prev/{id}` | GET | Navigate to previous card - HTMX partial |
| `/filter?category=X` | GET | Filter cards by category - HTMX partial |

---

## HTMX Flow

```
User clicks card → hx-get="/card/1/answer" → Server returns back side → HTMX swaps content

User clicks "Next" → hx-get="/next/1" → Server returns card 2 → HTMX swaps card + buttons

User selects filter → hx-get="/filter?category=Trees" → Server returns first Trees card
```

**Key Feature**: Navigation buttons are included in the card partial, so they update automatically with the correct IDs when HTMX swaps content.

---

## UI Layout

**Front Side (Problem):**
- Title and difficulty badge
- Category tag
- Problem description
- Examples (in code blocks)
- Constraints (bullet list)
- **💡 Hints** (collapsible details elements)
- **Pseudocode** (collapsible, if available)
- Progress counter (top right)
- Navigation buttons (bottom)

**Back Side (Solution):**
- Title and difficulty badge
- Category tag
- 💡 Approach explanation
- 📝 Solution code (Python)
- Progress counter
- Navigation buttons

---

## Color Scheme (Implemented)

| Element | Color Code |
|---------|-----------|
| Easy | `#00b8a3` (Green) |
| Medium | `#ffc01e` (Yellow) |
| Hard | `#ff375f` (Red) |
| Background | `#1a1a2e` (Dark Navy) |
| Card | `#16213e` (Dark Blue) |
| Text | `#eaeaea` (Light Gray) |
| Accent/Buttons | `#0f3460` (Blue) |
| Code Blocks | `#0f3460` (Blue) |
| Hints | `#ffc01e` (Yellow) - collapsible |

---

## Key Implementation Details

### Randomization
Problems are shuffled using `random.shuffle()` when the server starts. Each restart gives a new random order for varied practice.

### Collapsible Hints
Uses native HTML `<details>` and `<summary>` elements - no JavaScript required. Hints are extracted from the source repo's readme files.

### Progress Tracking
Simple counter showing current position (e.g., "3/49"). Updates automatically via HTMX swaps.

### Category Filtering
Dropdown filter re-renders the first card in the selected category. Backend handles the filtering logic.

---

## Data Source

Problems extracted from: [Sugapriyan-P-K/blind75](https://github.com/Sugapriyan-P-K/blind75/)

The `parse_problems.py` script:
1. Scans the `blind_75_flashcard_app/` submodule
2. Extracts from each `readme.md`:
   - Title, description, examples, constraints
   - Hints (from `<details>` tags)
   - Pseudocode (if present)
3. Pairs with corresponding `.py` solution files
4. Generates `data/problems.json`

**Note**: Only 49 of the 75 Blind problems have complete documentation in the source repo. The app includes all available documented problems.

---

## Future Enhancements (Not Implemented)

- Spaced repetition system
- Mark problems as "mastered"
- Progress persistence (cookies/session)
- Keyboard shortcuts for navigation
- Search functionality
- Filter by difficulty
- Export progress/notes
- Add remaining 26 problems as they become available

---

## Design Principles

1. **Python-First**: Minimize JS/CSS, maximize Python
2. **Simplicity**: No build tools, no npm, no bundlers
3. **Fast Iteration**: Live reload, simple architecture
4. **Self-Contained**: All dependencies via CDN or uv
5. **Accessibility**: Semantic HTML, native elements
