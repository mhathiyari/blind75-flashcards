# Blind 75 Flashcard App - Design Document

## Overview
A flashcard application to help revise the Blind 75 LeetCode problems. Each card displays a problem on the front, and when flipped, shows a brief explanation of the approach followed by the solution code.

---

## Features

### Core Features
- Display all 75 Blind 75 LeetCode problems as flashcards
- Flip animation to reveal answer
- Answer shows:
  1. Brief explanation of the approach/algorithm
  2. Solution code (Python)
- Navigate between cards (next/previous)
- Track progress (solved/unsolved)

### Nice-to-Have Features
- Filter by category (Arrays, Binary Search, Trees, etc.)
- Mark cards as "mastered" or "needs review"
- Shuffle mode
- Dark/Light theme
- Keyboard shortcuts for navigation
- Progress persistence (localStorage)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + TypeScript |
| Styling | Tailwind CSS |
| Build Tool | Vite |
| State | React useState/useContext |
| Storage | localStorage |

## Deployment Options

This is a **static web app** - no backend required. All data is bundled with the app.

### Self-Hosting Options

1. **Local Development**
   ```bash
   npm run dev
   # Opens at http://localhost:5173
   ```

2. **Build & Serve Locally**
   ```bash
   npm run build
   npx serve dist
   # Opens at http://localhost:3000
   ```

3. **Docker (Optional)**
   ```bash
   docker build -t blind75-flashcards .
   docker run -p 8080:80 blind75-flashcards
   # Opens at http://localhost:8080
   ```

4. **Free Hosting** (if you want to access from anywhere)
   - Vercel / Netlify / GitHub Pages (all free, one-click deploy)

---

## Data Structure

```typescript
interface Problem {
  id: number;
  title: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  category: string;
  description: string;
  examples: Example[];
  constraints: string[];
  explanation: string;
  code: string;
}

interface Example {
  input: string;
  output: string;
  explanation?: string;
}

interface UserProgress {
  solvedIds: number[];
  masteredIds: number[];
  currentIndex: number;
}
```

---

## Component Structure

```
src/
├── components/
│   ├── Flashcard.tsx        # Main flip card component
│   ├── CardFront.tsx        # Problem display (question side)
│   ├── CardBack.tsx         # Answer display (explanation + code)
│   ├── Navigation.tsx       # Next/Prev buttons
│   ├── ProgressBar.tsx      # Shows completion progress
│   ├── CategoryFilter.tsx   # Filter by problem category
│   └── Header.tsx           # App title and controls
├── data/
│   └── problems.ts          # All 75 problems data
├── hooks/
│   └── useProgress.ts       # Progress tracking hook
├── App.tsx
├── main.tsx
└── index.css
```

---

## Blind 75 Categories

1. **Arrays & Hashing** (9 problems)
2. **Two Pointers** (5 problems)
3. **Sliding Window** (6 problems)
4. **Stack** (7 problems)
5. **Binary Search** (7 problems)
6. **Linked List** (11 problems)
7. **Trees** (15 problems)
8. **Tries** (3 problems)
9. **Heap / Priority Queue** (1 problem)
10. **Backtracking** (4 problems)
11. **Graphs** (6 problems)
12. **Dynamic Programming** (11 problems)
13. **Greedy** (2 problems)
14. **Intervals** (5 problems)
15. **Math & Geometry** (3 problems)
16. **Bit Manipulation** (5 problems)

---

## UI Wireframe

```
┌─────────────────────────────────────────────────────┐
│  Blind 75 Flashcards          [Filter ▼] [Progress] │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │                                               │  │
│  │   1. Two Sum                        [Easy]    │  │
│  │   ─────────────────────────────────────────   │  │
│  │                                               │  │
│  │   Given an array of integers nums and an     │  │
│  │   integer target, return indices of the two  │  │
│  │   numbers such that they add up to target.   │  │
│  │                                               │  │
│  │   Example 1:                                  │  │
│  │   Input: nums = [2,7,11,15], target = 9      │  │
│  │   Output: [0,1]                               │  │
│  │                                               │  │
│  │                    [Click to Flip]            │  │
│  │                                               │  │
│  └───────────────────────────────────────────────┘  │
│                                                     │
│            [◀ Prev]    3/75    [Next ▶]             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Flipped State (Answer Side):**
```
┌───────────────────────────────────────────────┐
│                                               │
│   💡 Approach                                 │
│   ─────────────────────────────────────────   │
│   Use a hash map to store each number and    │
│   its index. For each number, check if       │
│   (target - num) exists in the map.          │
│                                               │
│   Time: O(n) | Space: O(n)                   │
│                                               │
│   📝 Solution                                 │
│   ─────────────────────────────────────────   │
│   ```python                                   │
│   def twoSum(nums, target):                  │
│       seen = {}                               │
│       for i, num in enumerate(nums):         │
│           diff = target - num                │
│           if diff in seen:                   │
│               return [seen[diff], i]         │
│           seen[num] = i                      │
│   ```                                         │
│                                               │
│                    [Click to Flip]            │
│                                               │
└───────────────────────────────────────────────┘
```

---

## Color Scheme

| Element | Color |
|---------|-------|
| Easy | `#00b8a3` (Green) |
| Medium | `#ffc01e` (Yellow) |
| Hard | `#ff375f` (Red) |
| Background | `#1a1a2e` (Dark) |
| Card | `#16213e` |
| Text | `#eaeaea` |
| Accent | `#0f3460` |

---

## Implementation Plan

1. **Setup** - Initialize Vite + React + TypeScript + Tailwind
2. **Data** - Create problems.ts with all 75 problems
3. **Flashcard Component** - Build flip animation card
4. **Navigation** - Add prev/next and progress display
5. **Filtering** - Add category filter
6. **Progress Tracking** - Implement localStorage persistence
7. **Polish** - Keyboard shortcuts, animations, responsive design

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` / `Enter` | Flip card |
| `→` / `j` | Next card |
| `←` / `k` | Previous card |
| `m` | Mark as mastered |
| `r` | Reset progress |
| `s` | Shuffle cards |
