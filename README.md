# Blind 75 Flashcards

Interactive flashcard application for mastering the Blind 75 LeetCode problems. Built with FastAPI, HTMX, and Tailwind CSS.

## Features

- **75 LeetCode problems** — the complete Blind 75 list
- Interactive flashcard interface with flip animation
- Solutions in **Python and C++** (toggle on the solution side; your choice is remembered)
- Collapsible hints on every problem
- Dark theme UI optimized for extended study sessions
- Category-based filtering (Arrays, Dynamic Programming, Trees, etc.)
- Navigation through problems with Previous/Next buttons
- **Randomized problem order** on each server restart for varied practice
- Progress tracking (X/75 counter)
- Responsive design for desktop and mobile

> **Note**: The 75 problems are the standard Blind 75 list. 49 come from the [source repository](https://github.com/Sugapriyan-P-K/blind75/), which only documented those; the other 26 (graphs, trees, tries, heaps, etc.) were written separately, with solutions tested.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Templating**: Jinja2
- **Interactivity**: HTMX (minimal JavaScript)
- **Styling**: Tailwind CSS (via CDN)
- **Package Manager**: uv

## Prerequisites

- Python 3.8 or higher
- `uv` package manager

## Installation

### On macOS

1. **Install uv package manager:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Add uv to PATH:**
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

3. **Clone the repository:**
   ```bash
   git clone https://github.com/mhathiyari/blind75-flashcards.git
   cd blind75-flashcards
   ```

4. **Install dependencies:**
   ```bash
   uv sync
   ```

### On Ubuntu/Debian Linux

1. **Install uv package manager:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Add uv to PATH:**
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   # Add to ~/.bashrc or ~/.zshrc to make permanent
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Clone the repository:**
   ```bash
   git clone https://github.com/mhathiyari/blind75-flashcards.git
   cd blind75-flashcards
   ```

4. **Install dependencies:**
   ```bash
   uv sync
   ```

## Running the Application

### Development Mode (with auto-reload)

```bash
export PATH="$HOME/.local/bin:$PATH"
uv run uvicorn main:app --reload
```

The application will be available at: **http://localhost:8000**

### Production Mode

```bash
export PATH="$HOME/.local/bin:$PATH"
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Running on a Custom Port

```bash
uv run uvicorn main:app --port 5000
```

## Usage

1. **Start the server** using one of the commands above
2. **Open your browser** and navigate to `http://localhost:8000`
3. **Click on a card** to flip and see the solution
4. **Use Previous/Next buttons** to navigate through problems
5. **Filter by category** using the dropdown menu at the top

## Project Structure

```
blind75-flashcards/
├── main.py                     # FastAPI application with routes
├── data/
│   └── problems.json           # All 75 problems with solutions
├── templates/
│   ├── base.html               # Base template with styles
│   ├── index.html              # Main page
│   └── partials/
│       └── card.html           # Flashcard component
├── static/                     # Static files (currently empty)
├── parse_problems.py           # Script to parse problems from source
├── pyproject.toml              # Project dependencies
└── uv.lock                     # Locked dependencies
```

## API Endpoints

- `GET /` - Main page with first flashcard
- `GET /card/{id}` - Get specific card (front side)
- `GET /card/{id}/answer` - Get card with solution (back side)
- `GET /next/{id}` - Navigate to next card
- `GET /prev/{id}` - Navigate to previous card
- `GET /filter?category=X` - Filter cards by category

## Contributing

Contributions are welcome! Feel free to:
- Add more problems from the Blind 75 list
- Improve the UI/UX
- Add new features (e.g., spaced repetition, bookmark problems)
- Fix bugs

## License

MIT License - feel free to use this project for your own learning or modify it as needed.

## Acknowledgments

- Problem data sourced from [Sugapriyan-P-K/blind75](https://github.com/Sugapriyan-P-K/blind75/)
- Inspired by the Blind 75 list curated by the tech community
