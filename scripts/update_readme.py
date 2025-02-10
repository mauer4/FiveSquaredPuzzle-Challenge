#!/usr/bin/env python3
import os
import sys

def get_top5_leaderboard(leaderboard_path, top_n=5):
    if not os.path.exists(leaderboard_path):
        print(f"ERROR: Leaderboard file '{leaderboard_path}' does not exist.")
        return None
    with open(leaderboard_path, "r") as f:
        lines = f.readlines()
    # Return at most the top_n lines (strip trailing whitespace)
    return [line.strip() for line in lines[:top_n]]

def parse_leaderboard_line(line):
    """
    Expected line format:
      "1. alice (py) - 5.232 seconds (timestamp: 2025-02-10 01:27:38)"
    This function extracts:
      rank, identifier, runtime, timestamp.
    """
    try:
        # Split on " - " to separate the left and right parts.
        left, right = line.split(" - ", 1)
        # left part: "1. alice (py)"
        left_parts = left.split()
        rank = left_parts[0].rstrip(".")
        identifier = " ".join(left_parts[1:])
        # right part: "5.232 seconds (timestamp: 2025-02-10 01:27:38)"
        right_parts = right.split()
        runtime = right_parts[0]
        # Extract timestamp from the text within parentheses.
        # It is assumed to be in the format: (timestamp: 2025-02-10 01:27:38)
        if "(timestamp:" in right:
            timestamp = right[right.find("(timestamp: ") + len("(timestamp: "):].rstrip(")")
        else:
            timestamp = "N/A"
        return rank, identifier, runtime, timestamp
    except Exception as e:
        print(f"WARNING: Could not parse line: {line} - {e}")
        return None

def build_scoreboard_md(top_lines):
    # Build a markdown table with headers.
    header = "| Rank | Identifier | Runtime (s) | Timestamp |\n| --- | --- | --- | --- |\n"
    table_lines = []
    for line in top_lines:
        parsed = parse_leaderboard_line(line)
        if parsed is None:
            continue
        rank, identifier, runtime, timestamp = parsed
        table_lines.append(f"| {rank} | {identifier} | {runtime} | {timestamp} |")
    return header + "\n".join(table_lines)

def update_readme(scoreboard_md, readme_path="../README.md", marker="## Leaderboard"):
    # Read the existing README.
    if not os.path.exists(readme_path):
        print(f"ERROR: README file '{readme_path}' does not exist.")
        sys.exit(1)
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Check if the marker exists.
    if marker in readme_content:
        # Replace the existing leaderboard section.
        before, _ = readme_content.split(marker, 1)
        new_content = before.strip() + "\n\n" + marker + "\n\n" + scoreboard_md + "\n"
    else:
        # Append the leaderboard section at the end.
        new_content = readme_content.rstrip() + "\n\n" + marker + "\n\n" + scoreboard_md + "\n"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated README.md with the following leaderboard:")
    print(scoreboard_md)

def main():
    # Path to the leaderboard log file.
    leaderboard_path = os.path.join("..", "results", "results.log")
    top_lines = get_top5_leaderboard(leaderboard_path)
    if top_lines is None or len(top_lines) == 0:
        print("No leaderboard entries found.")
        sys.exit(1)
    scoreboard_md = build_scoreboard_md(top_lines)
    update_readme(scoreboard_md)

if __name__ == "__main__":
    main()
