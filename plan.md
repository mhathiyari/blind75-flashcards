# Blind 75 Flashcard App - Implementation Plan

## Tech Stack (Final)

| Component | Technology |
|-----------|------------|
| Package Manager | `uv` |
| Backend | FastAPI |
| Templating | Jinja2 |
| Interactivity | HTMX |
| Styling | Tailwind CSS (CDN) |
| Flip Animation | Pure CSS |
| Data Storage | JSON file + localStorage |

---

## Project Structure

```
experimental_cluade/
├── pyproject.toml          # uv project config
├── main.py                 # FastAPI app (single file)
├── data/
│   └── problems.json       # All 75 problems
├── templates/
│   ├── base.html           # Base layout
│   ├── index.html          # Main flashcard page
│   └── partials/
│       ├── card.html       # Flashcard component
│       ├── progress.html   # Progress bar
│       └── filters.html    # Category filter
└── static/
    └── styles.css          # Custom CSS (flip animation)
```

---

## Implementation Steps

### Step 1: Project Setup
- [x] Initialize uv project: `uv init`
- [x] Add dependencies: `uv add fastapi uvicorn jinja2 python-multipart`
- [x] Create folder structure

### Step 2: Create Problem Data
- [x] Create `data/problems.json` with 49 Blind 75 problems (from GitHub repo)
- [x] Each problem includes:
  - id, title, difficulty, category
  - description, examples, constraints
  - explanation (approach)
  - code (Python solution)

### Step 3: Build FastAPI Backend
- [x] Create `main.py` with routes:
  - `GET /` - Main page with first flashcard
  - `GET /card/{id}` - Get specific card (HTMX partial)
  - `GET /card/{id}/answer` - Get flipped card content (HTMX partial)
  - `GET /next/{id}` - Get next card (HTMX partial)
  - `GET /prev/{id}` - Get previous card (HTMX partial)
  - `GET /filter?category=X` - Filter by category (HTMX partial)
- [x] Setup Jinja2 templates
- [x] Mount static files

### Step 4: Create Base Template
- [x] `templates/base.html`:
  - Include Tailwind CSS (CDN)
  - Include HTMX (CDN)
  - Dark theme styling
  - Header with title

### Step 5: Build Flashcard Component
- [x] `templates/partials/card.html`:
  - Front: problem title, difficulty badge, description, examples
  - Back: explanation, code display
  - Click triggers HTMX swap (no CSS flip, direct swap)
  - Navigation button updates via inline script

### Step 6: Add Navigation
- [ ] Previous/Next buttons
- [ ] Current position indicator (e.g., "3/75")
- [ ] HTMX loads next/prev card without page reload

### Step 7: Add Category Filter
- [ ] Dropdown with all 16 categories
- [ ] "All" option to show everything
- [ ] HTMX updates card list on filter change

### Step 8: Add Progress Tracking
- [ ] Mark card as "mastered" button
- [ ] Progress bar showing mastered/total
- [ ] Store progress in localStorage (client-side)
- [ ] Small JS snippet to handle localStorage

### Step 9: Keyboard Shortcuts
- [ ] Small vanilla JS for:
  - Space/Enter: flip card
  - Arrow keys: navigate
  - 'm': mark mastered

### Step 10: Polish & Test
- [ ] Test all 75 cards load correctly
- [ ] Test flip animation smooth
- [ ] Test navigation works
- [ ] Test filters work
- [ ] Mobile responsive check

---

## Route Details

```python
# main.py routes

@app.get("/")
# Returns: full page with first card

@app.get("/card/{card_id}")
# Returns: card partial (front side)
# HTMX: hx-get, swaps card container

@app.get("/card/{card_id}/answer")
# Returns: card partial (back side with explanation + code)
# HTMX: hx-get, swaps card inner content

@app.get("/next/{current_id}")
# Returns: next card partial
# HTMX: hx-get, swaps card container

@app.get("/prev/{current_id}")
# Returns: previous card partial
# HTMX: hx-get, swaps card container

@app.get("/filter")
# Query param: ?category=Arrays
# Returns: card partial for first card in filtered set
# HTMX: hx-get, swaps card container
```

---

## HTMX Flow

```
User clicks card → hx-get="/card/1/answer" → Server returns back side → HTMX swaps content

User clicks "Next" → hx-get="/next/1" → Server returns card 2 → HTMX swaps card

User selects filter → hx-get="/filter?category=Trees" → Server returns first Trees card
```

---

## CSS Flip Animation

```css
.flashcard {
  perspective: 1000px;
}

.flashcard-inner {
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.flashcard.flipped .flashcard-inner {
  transform: rotateY(180deg);
}

.flashcard-front, .flashcard-back {
  backface-visibility: hidden;
}

.flashcard-back {
  transform: rotateY(180deg);
}
```

---

## Sample Problem JSON

```json
{
  "id": 1,
  "title": "Two Sum",
  "difficulty": "Easy",
  "category": "Arrays & Hashing",
  "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.",
  "examples": [
    {
      "input": "nums = [2,7,11,15], target = 9",
      "output": "[0,1]",
      "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
    }
  ],
  "constraints": [
    "2 <= nums.length <= 10^4",
    "-10^9 <= nums[i] <= 10^9",
    "Only one valid answer exists."
  ],
  "explanation": "Use a hash map to store each number and its index as you iterate. For each number, check if (target - current number) already exists in the map. If yes, return both indices. This gives O(n) time complexity.",
  "code": "def twoSum(nums: List[int], target: int) -> List[int]:\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i"
}
```

---

## Commands to Run

```bash
# Setup
cd experimental_cluade
uv init
uv add fastapi uvicorn jinja2

# Run development server
uv run uvicorn main:app --reload

# Opens at http://localhost:8000
```

---

## Questions Before Starting

1. Do you want syntax highlighting for code? (adds highlight.js CDN)
2. Do you want all 75 problems included immediately, or start with a few for testing?
3. Any specific color theme preference beyond the LeetCode-inspired dark theme?
