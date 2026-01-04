#!/usr/bin/env python3
"""
LeetCode README Updater
Automatically scans LeetCode solution files and updates README.md
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


# Topic to Emoji Mapping
TOPIC_EMOJI_MAP = {
    "Arrays": "📦",
    "Strings": "📝",
    "Hash Table": "🔑",
    "Hash Map": "🔑",
    "Linked List": "🔗",
    "Stack": "📚",
    "Queue": "📋",
    "Heap": "⛰️",
    "Priority Queue": "⛰️",
    "Trees": "🌳",
    "Binary Tree": "🌳",
    "Binary Search Tree": "🌳",
    "Trie": "🌲",
    "Graph": "🕸️",
    "Graphs": "🕸️",
    "Breadth-First Search": "🌊",
    "BFS": "🌊",
    "Depth-First Search": "🌊",
    "DFS": "🌊",
    "Dynamic Programming": "⚡",
    "DP": "⚡",
    "Greedy": "👑",
    "Sorting": "🔀",
    "Binary Search": "🔍",
    "Search": "🔍",
    "Math": "🧮",
    "Geometry": "📐",
    "Bit Manipulation": "⚙️",
    "Union Find": "🔗",
    "Disjoint Set": "🔗",
    "Segment Tree": "🌳",
    "Sliding Window": "🪟",
    "Two Pointers": "👉",
    "Backtracking": "🔙",
    "Recursion": "🔄",
    "Design": "🏗️",
    "Database": "💾",
    "Shell": "🐚",
    "Regex": "📖",
    "Simulation": "🎬",
    "Counting": "🔢",
    "Prefix Sum": "➕",
    "Suffix Array": "🔪",
    "Enumeration": "📋",
    "Brute Force": "💪",
    "Divide and Conquer": "✂️",
    "Monotonic Stack": "📈",
    "Monotonic Queue": "📈",
}


class LeetCodeReadmeUpdater:
    """Updates README.md with categorized LeetCode solutions."""

    def __init__(self, root_dir: str = "."):
        """
        Initialize the updater.

        Args:
            root_dir: Root directory of the project (default: current directory)
        """
        self.root_dir = Path(root_dir)
        self.difficulty_dirs = ["Easy", "Medium", "Hard"]
        self.solutions: Dict[str, Dict[str, Set[int]]] = defaultdict(lambda: defaultdict(set))
        self.file_mapping: Dict[int, Tuple[str, str]] = {}  # {id: (slug, path)}

    def extract_metadata(self, file_path: Path) -> Tuple[int, str, List[str]]:
        """
        Extract problem ID, slug, and topics from file header.

        Looks for:
        # Topics: Topic1, Topic2, Topic3  (for Python)
        // Topics: Topic1, Topic2, Topic3 (for JavaScript/Java/C++)

        Args:
            file_path: Path to the solution file

        Returns:
            Tuple of (problem_id, slug, list_of_topics)
        """
        filename = file_path.stem  # Get filename without extension
        match = re.match(r"(\d+)-(.+)", filename)

        if not match:
            return None, None, []

        problem_id = int(match.group(1))
        slug = match.group(2)

        # Read first 20 lines to find Topics comment
        topics = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for _ in range(20):  # Check first 20 lines
                    line = f.readline()
                    if not line:
                        break

                    # Match both Python (#) and other languages (//)
                    topic_match = re.search(
                        r"(?:#|//)?\s*Topics?\s*:\s*(.+?)(?:\n|$)", line, re.IGNORECASE
                    )
                    if topic_match:
                        topics_str = topic_match.group(1)
                        topics = [
                            t.strip() for t in topics_str.split(",") if t.strip()
                        ]
                        break
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

        return problem_id, slug, topics

    def scan_solutions(self) -> None:
        """Scan all solution files and extract metadata."""
        for difficulty in self.difficulty_dirs:
            diff_path = self.root_dir / difficulty
            if not diff_path.exists():
                continue

            for file_path in diff_path.iterdir():
                if file_path.is_file():
                    problem_id, slug, topics = self.extract_metadata(file_path)

                    if problem_id is None:
                        continue

                    # Store file mapping
                    self.file_mapping[problem_id] = (slug, str(file_path.relative_to(self.root_dir)))

                    # If no topics found, skip
                    if not topics:
                        print(f"⚠️  No topics found in {file_path.name}")
                        continue

                    # Add to solutions organized by topic
                    for topic in topics:
                        self.solutions[topic][difficulty].add(problem_id)

    def generate_readme_section(self) -> str:
        """
        Generate the solutions by topic section.

        Returns:
            Formatted markdown string
        """
        if not self.solutions:
            return "No solutions found. Please add solution files with Topics metadata."

        lines = ["## 📊 Solutions by Topic\n"]

        # Sort topics alphabetically
        sorted_topics = sorted(self.solutions.keys())

        for topic in sorted_topics:
            # Get emoji for topic
            emoji = TOPIC_EMOJI_MAP.get(topic, "📌")
            lines.append(f"### {emoji} {topic}\n")

            # Collect all problems for this topic across all difficulties
            all_problems = set()
            for difficulty in self.difficulty_dirs:
                all_problems.update(self.solutions[topic][difficulty])

            # Sort by problem ID and format
            for problem_id in sorted(all_problems):
                slug, file_path = self.file_mapping[problem_id]
                # Format: ID. Slug (converted to title case)
                title = slug.replace("-", " ").title()
                # Convert backslashes to forward slashes for markdown compatibility
                file_path = file_path.replace("\\", "/")
                lines.append(f"- [{problem_id}. {title}](./{file_path})\n")

            lines.append("\n")

        return "".join(lines)

    def update_total_problems(self, content: str) -> str:
        """
        Update the Total Problems Solved count in README.
        
        Looks for pattern: - **Total Problems Solved:** X (Updating...)
        
        Args:
            content: README content
            
        Returns:
            Updated content with new problem count
        """
        total_problems = len(self.file_mapping)
        # Pattern to match the total problems line
        pattern = r"(-\s*\*\*Total Problems Solved:\*\*\s*)(\d+|\?)\s*(\(Updating\.\.\.\))"
        replacement = rf"\g<1>{total_problems} \3"
        updated_content = re.sub(pattern, replacement, content)
        return updated_content

    def update_readme(self) -> None:
        """
        Update README.md with generated solutions section and total problems count.

        The script looks for placeholder markers:
        <!-- LEETCODE_SOLUTIONS_START -->
        <!-- LEETCODE_SOLUTIONS_END -->

        Everything between these markers will be replaced.
        Also updates the Total Problems Solved count.
        """
        readme_path = self.root_dir / "README.md"

        if not readme_path.exists():
            print("❌ README.md not found!")
            return

        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if markers exist
        start_marker = "<!-- LEETCODE_SOLUTIONS_START -->"
        end_marker = "<!-- LEETCODE_SOLUTIONS_END -->"

        if start_marker not in content or end_marker not in content:
            print("⚠️  Markers not found in README.md!")
            print("Please add the following placeholders to your README.md:")
            print(f"\n{start_marker}")
            print(f"{end_marker}\n")
            return

        # Generate new section
        new_section = self.generate_readme_section()

        # Replace content between markers
        pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
        replacement = start_marker + "\n" + new_section + end_marker
        updated_content = re.sub(
            pattern,
            lambda m: replacement,
            content,
            flags=re.DOTALL,
        )
        
        # Update total problems count
        updated_content = self.update_total_problems(updated_content)

        # Write back to file
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

        print(f"✅ README.md updated successfully!")
        print(f"� Total problems solved: {len(self.file_mapping)}")
        print(f"� Total topics: {len(self.solutions)}")

    def run(self) -> None:
        """Run the complete update process."""
        print("🚀 Scanning LeetCode solutions...\n")
        self.scan_solutions()
        print()
        self.update_readme()


def main():
    """Main entry point."""
    # Use current directory as root
    updater = LeetCodeReadmeUpdater(root_dir=".")
    updater.run()


if __name__ == "__main__":
    main()
