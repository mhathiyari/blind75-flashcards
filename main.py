from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import random
from pathlib import Path

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Load problems data
def load_problems():
    with open("data/problems.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        random.shuffle(data)  # Randomize the order
        return data

problems = load_problems()

# Helper functions
def get_problem_by_id(problem_id: int):
    """Get a problem by its ID"""
    for problem in problems:
        if problem["id"] == problem_id:
            return problem
    return None

def get_next_problem_id(current_id: int, category: str = None):
    """Get the next problem ID, optionally filtered by category"""
    filtered = problems if not category else [p for p in problems if p["category"] == category]

    for i, p in enumerate(filtered):
        if p["id"] == current_id:
            if i + 1 < len(filtered):
                return filtered[i + 1]["id"]
            else:
                return filtered[0]["id"]  # Loop back to first
    return filtered[0]["id"] if filtered else 1

def get_prev_problem_id(current_id: int, category: str = None):
    """Get the previous problem ID, optionally filtered by category"""
    filtered = problems if not category else [p for p in problems if p["category"] == category]

    for i, p in enumerate(filtered):
        if p["id"] == current_id:
            if i - 1 >= 0:
                return filtered[i - 1]["id"]
            else:
                return filtered[-1]["id"]  # Loop back to last
    return filtered[0]["id"] if filtered else 1

def get_categories():
    """Get unique list of categories"""
    categories = list(set(p["category"] for p in problems))
    return sorted(categories)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page with first flashcard"""
    first_problem = problems[0] if problems else None
    categories = get_categories()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "problem": first_problem,
            "total": len(problems),
            "current_index": 1,
            "categories": categories,
            "flipped": False
        }
    )

@app.get("/card/{card_id}", response_class=HTMLResponse)
async def get_card(request: Request, card_id: int):
    """Get specific card (front side) - HTMX partial"""
    problem = get_problem_by_id(card_id)
    if not problem:
        problem = problems[0]

    # Find index for display
    current_index = next((i + 1 for i, p in enumerate(problems) if p["id"] == card_id), 1)

    return templates.TemplateResponse(
        "partials/card.html",
        {
            "request": request,
            "problem": problem,
            "total": len(problems),
            "current_index": current_index,
            "flipped": False
        }
    )

@app.get("/card/{card_id}/answer", response_class=HTMLResponse)
async def get_card_answer(request: Request, card_id: int):
    """Get flipped card content (back side with explanation + code) - HTMX partial"""
    problem = get_problem_by_id(card_id)
    if not problem:
        problem = problems[0]

    # Find index for display
    current_index = next((i + 1 for i, p in enumerate(problems) if p["id"] == card_id), 1)

    return templates.TemplateResponse(
        "partials/card.html",
        {
            "request": request,
            "problem": problem,
            "total": len(problems),
            "current_index": current_index,
            "flipped": True
        }
    )

@app.get("/next/{current_id}", response_class=HTMLResponse)
async def next_card(request: Request, current_id: int, category: str = None):
    """Get next card - HTMX partial"""
    next_id = get_next_problem_id(current_id, category)
    problem = get_problem_by_id(next_id)

    current_index = next((i + 1 for i, p in enumerate(problems) if p["id"] == next_id), 1)

    return templates.TemplateResponse(
        "partials/card.html",
        {
            "request": request,
            "problem": problem,
            "total": len(problems),
            "current_index": current_index,
            "flipped": False
        }
    )

@app.get("/prev/{current_id}", response_class=HTMLResponse)
async def prev_card(request: Request, current_id: int, category: str = None):
    """Get previous card - HTMX partial"""
    prev_id = get_prev_problem_id(current_id, category)
    problem = get_problem_by_id(prev_id)

    current_index = next((i + 1 for i, p in enumerate(problems) if p["id"] == prev_id), 1)

    return templates.TemplateResponse(
        "partials/card.html",
        {
            "request": request,
            "problem": problem,
            "total": len(problems),
            "current_index": current_index,
            "flipped": False
        }
    )

@app.get("/filter", response_class=HTMLResponse)
async def filter_by_category(request: Request, category: str = None):
    """Filter cards by category - HTMX partial"""
    if category and category != "All":
        filtered = [p for p in problems if p["category"] == category]
        problem = filtered[0] if filtered else problems[0]
    else:
        problem = problems[0]

    current_index = 1

    return templates.TemplateResponse(
        "partials/card.html",
        {
            "request": request,
            "problem": problem,
            "total": len(problems),
            "current_index": current_index,
            "flipped": False
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
