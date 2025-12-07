import json
import os
import re
from pathlib import Path

def parse_readme(readme_path):
    """Parse a readme.md file to extract problem information"""
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title (first heading)
    title_match = re.search(r'^###?\s+\d+\.\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Unknown"

    # Extract description (everything before first Example)
    desc_match = re.search(r'^###.*?\n\n(.*?)(?=Example|Constraints)', content, re.DOTALL | re.MULTILINE)
    description = desc_match.group(1).strip() if desc_match else ""

    # Extract examples
    examples = []
    example_pattern = r'Example \d+:\s*```(.*?)```'
    for match in re.finditer(example_pattern, content, re.DOTALL):
        examples.append(match.group(1).strip())

    # Extract constraints
    constraints = []
    constraints_match = re.search(r'Constraints:(.*?)(?=<details>|$)', content, re.DOTALL)
    if constraints_match:
        constraint_text = constraints_match.group(1).strip()
        constraints = [line.strip('- ').strip() for line in constraint_text.split('\n') if line.strip().startswith('-')]

    # Extract hints for explanation
    hints = []
    hint_pattern = r'<summary><h3>Show Hint \d+</h3></summary>\s*<p>(.*?)</p>'
    for match in re.finditer(hint_pattern, content, re.DOTALL):
        hints.append(match.group(1).strip())

    explanation = " ".join(hints) if hints else "Use optimal algorithm approach."

    return {
        'title': title,
        'description': description,
        'examples': examples,
        'constraints': constraints,
        'explanation': explanation
    }

def parse_python_solution(py_path):
    """Extract the solution code from Python file"""
    if not os.path.exists(py_path):
        return "# Solution not available"

    with open(py_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the main Solution class (non-commented version)
    class_match = re.search(r'(class Solution:.*?)(?=\n(?:class|print|$))', content, re.DOTALL)
    if class_match:
        return class_match.group(1).strip()

    return content.strip()

def determine_difficulty(title, category):
    """Determine difficulty based on problem characteristics"""
    # Simple heuristic - can be improved
    easy_keywords = ['two sum', 'contains duplicate', 'valid', 'reverse']
    hard_keywords = ['median', 'serialize', 'trap', 'word ladder']

    title_lower = title.lower()
    if any(kw in title_lower for kw in hard_keywords):
        return 'Hard'
    elif any(kw in title_lower for kw in easy_keywords):
        return 'Easy'
    else:
        return 'Medium'

def get_category_from_path(path):
    """Extract category from file path"""
    path_parts = Path(path).parts
    category_map = {
        'Arrays': 'Arrays',
        'String': 'String',
        'LinkedList': 'Linked List',
        'Trees': 'Trees',
        'DynamicProgramming': 'Dynamic Programming',
        'Graph': 'Graphs',
        'Intervals': 'Intervals',
        'Binary_bitManipulation': 'Binary & Bit Manipulation',
        'matrix': 'Matrix'
    }

    for part in path_parts:
        if part in category_map:
            return category_map[part]

    return 'General'

def main():
    repo_path = Path('temp_blind75')
    problems = []
    problem_id = 1

    # Find all readme.md files
    readme_files = list(repo_path.rglob('*/readme.md'))

    for readme_path in sorted(readme_files):
        # Skip root readme
        if readme_path.parent == repo_path:
            continue

        print(f"Parsing: {readme_path}")

        # Parse readme
        problem_data = parse_readme(readme_path)

        # Get category from path
        category = get_category_from_path(str(readme_path))

        # Find corresponding Python file
        py_files = list(readme_path.parent.glob('*.py'))
        py_code = parse_python_solution(py_files[0]) if py_files else "# Solution not available"

        # Determine difficulty
        difficulty = determine_difficulty(problem_data['title'], category)

        # Create problem entry
        problem = {
            'id': problem_id,
            'title': problem_data['title'],
            'difficulty': difficulty,
            'category': category,
            'description': problem_data['description'],
            'examples': problem_data['examples'],
            'constraints': problem_data['constraints'],
            'explanation': problem_data['explanation'],
            'code': py_code
        }

        problems.append(problem)
        problem_id += 1

    # Write to JSON file
    output_path = Path('data/problems.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(problems, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Successfully created {output_path} with {len(problems)} problems!")

if __name__ == '__main__':
    main()
