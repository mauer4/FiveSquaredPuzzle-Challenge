#!/bin/bash
# Usage: ./run_tests.sh path/to/solution

if [ -z "$1" ]; then
    echo "Usage: $0 path/to/solution"
    exit 1
fi

SOLUTION="$1"

# Determine the directory of this script.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Build the path to the input file relative to the script's location.
INPUT_FILE="${SCRIPT_DIR}/../config/input.json"

# Optional: Check if the input file exists.
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file $INPUT_FILE does not exist."
    exit 1
fi

# Determine the MIME type of the solution file.
FILE_TYPE=$(file --mime-type -b "$SOLUTION")

# If the solution file is a text file, perform CRLF conversion.
if [[ "$FILE_TYPE" == text/* ]]; then
    TEMP_SOLUTION=$(mktemp)
    sed 's/\r//g' "$SOLUTION" > "$TEMP_SOLUTION"
    chmod +x "$TEMP_SOLUTION"
    RUN_CMD="$TEMP_SOLUTION"
else
    RUN_CMD="$SOLUTION"
fi

# Record start time (in nanoseconds)
START_TIME=$(date +%s%N)

# Run the solution with the input file.
# (Assumes your solution reads from STDIN; adjust if needed.)
OUTPUT=$("$RUN_CMD" < "$INPUT_FILE")
EXIT_CODE=$?

# If we created a temporary file, remove it.
if [[ "$FILE_TYPE" == text/* ]]; then
    rm "$TEMP_SOLUTION"
fi

if [ $EXIT_CODE -ne 0 ]; then
    echo "Solution failed to run or timed out."
    exit 1
fi

# Record end time and compute runtime in seconds.
END_TIME=$(date +%s%N)
RUNTIME=$(echo "scale=3; ($END_TIME - $START_TIME) / 1000000000" | bc)

# Call the validation script (which also updates the leaderboard)
# We compute its path relative to the script's location.
VALIDATION_SCRIPT="${SCRIPT_DIR}/../scripts/validate_solution.py"
cd "$SCRIPT_DIR"
python3 "$VALIDATION_SCRIPT" "$OUTPUT" "$RUNTIME" "$SOLUTION"
RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo "Submission successful. Runtime: $RUNTIME seconds."
    exit 0
else
    echo "Submission failed validation."
    exit 1
fi
