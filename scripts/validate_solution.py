#!/usr/bin/env python3
import json
import sys
import os
from datetime import datetime

def load_config(input_file):
    try:
        with open(input_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load configuration from {input_file}: {e}")
        sys.exit(1)

def validate_output(output, config):
    # Attempt to parse JSON.
    try:
        data = json.loads(output)
    except json.JSONDecodeError as e:
        print("ERROR: Output is not valid JSON.")
        print("JSONDecodeError:", e)
        print("Received output:")
        print(output)
        return False

    # Check that the top-level JSON is a list.
    if not isinstance(data, list):
        print("ERROR: Output JSON is not a list.")
        print("Type received:", type(data).__name__)
        print("Received JSON content:", data)
        return False

    required_keys = ["piece", "position", "orientation"]
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            print(f"ERROR: Output item {idx} is not an object (dict). Found type: {type(item).__name__}")
            print("Item content:", item)
            return False
        # Check that all required keys are present.
        for key in required_keys:
            if key not in item:
                print(f"ERROR: Output item {idx} is missing required key '{key}'.")
                print("Item content:", item)
                return False
        # Verify that "piece" is a list.
        if not isinstance(item["piece"], list):
            print(f"ERROR: Output item {idx} key 'piece' is not a list. Found type: {type(item['piece']).__name__}")
            print("Item content:", item)
            return False
        # Verify that "position" is a list of exactly two elements.
        if not (isinstance(item["position"], list) and len(item["position"]) == 2):
            print(f"ERROR: Output item {idx} key 'position' is not a list of two elements.")
            print("Item content:", item)
            return False
        # Verify that "orientation" is one of the allowed values.
        if item["orientation"] not in ["h", "hr", "v", "vr"]:
            print(f"ERROR: Output item {idx} key 'orientation' has invalid value '{item['orientation']}'.")
            print("Allowed values: h, hr, v, vr")
            print("Item content:", item)
            return False

    return True

def update_leaderboard(runtime, identifier):
    leaderboard_file = os.path.join("..", "results", "results.log")
    entries = []

    # Read existing leaderboard entries.
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, 'r') as f:
            for line in f:
                try:
                    # Expected format:
                    # "1. alice (py) - 5.232 seconds (timestamp: 2025-02-10 01:27:38)"
                    left, right = line.split(" - ", 1)
                    # Left part: "1. alice (py)"
                    left_parts = left.split()
                    entry_ident = " ".join(left_parts[1:])
                    # Right part: "5.232 seconds (timestamp: ...)"
                    right_parts = right.split()
                    entry_runtime = float(right_parts[0])
                    entries.append((entry_runtime, entry_ident))
                except Exception as e:
                    print(f"WARNING: Failed to parse leaderboard line: {line.strip()} - {e}")
                    continue

    # Check if an entry from the same identifier already exists.
    existing_index = None
    existing_runtime = None
    for i, (rtime, ident) in enumerate(entries):
        if ident == identifier:
            existing_index = i
            existing_runtime = rtime
            break

    if existing_index is not None:
        if runtime < existing_runtime:
            print(f"Your new result ({runtime} seconds) is better than your previous result ({existing_runtime} seconds). Overwriting the old result.")
            # Remove the old result.
            del entries[existing_index]
            entries.append((runtime, identifier))
        else:
            print(f"Your new result ({runtime} seconds) is worse than your previous result ({existing_runtime} seconds). Discarding the new result.")
            # Use the existing (better) runtime.
            runtime = existing_runtime
    else:
        # No existing entry, so add the new one.
        entries.append((runtime, identifier))

    # Sort entries by runtime (smaller is better).
    entries.sort(key=lambda x: x[0])

    # Get a formatted datetime string.
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write updated leaderboard.
    with open(leaderboard_file, 'w') as f:
        for rank, (rtime, ident) in enumerate(entries, start=1):
            f.write(f"{rank}. {ident} - {rtime} seconds (timestamp: {timestamp_str})\n")

    # Find and return the ranking for the current submission.
    for rank, (rtime, ident) in enumerate(entries, start=1):
        if ident == identifier and abs(rtime - runtime) < 1e-6:
            return rank
    return None

def main():
    # Updated usage: now expects 3 arguments:
    #   1. The solution's output (from STDOUT)
    #   2. The runtime (passed in by run_tests.sh)
    #   3. The solution filename (e.g., "solutions/alice_solution.py")
    if len(sys.argv) < 4:
        print("Usage: validate_solution.py <output> <runtime> <solution_filename>")
        sys.exit(1)

    output = sys.argv[1]
    runtime = sys.argv[2]
    solution_filename = sys.argv[3]

    try:
        runtime = float(runtime)
    except ValueError:
        print("ERROR: Invalid runtime value. Provided value:", runtime)
        sys.exit(1)

    # Always load the configuration from the fixed file.
    config = load_config("../config/input.json")
    if not validate_output(output, config):
        print("Validation failed: output did not meet requirements.")
        sys.exit(1)

    # Extract username and language from the solution file's name.
    # Expected format: "solutions/<username>_solution.<ext>"
    base = os.path.basename(solution_filename)
    name_part, ext = os.path.splitext(base)
    username = name_part.replace("_solution", "")
    language = ext.lstrip(".")
    identifier = f"{username} ({language})"

    rank = update_leaderboard(runtime, identifier)
    if rank is not None:
        print(f"Submission accepted! Your runtime: {runtime} seconds. You are ranked #{rank} on the leaderboard.")
        sys.exit(0)
    else:
        print("Failed to update leaderboard.")
        sys.exit(1)

if __name__ == "__main__":
    main()
