# FiveSquaredPuzzle-Challenge

Welcome to the Fize Squared Puzzle Solver Competition repository! This is a platform for AMD engineers to submit their solutions to our puzzle challenge.

## Repository Structure

.
├── .github
│   └── workflows
│       └── test_solution.yml    # GitHub Actions workflow
├── config
│   └── input.json               # Puzzle configuration (and optionally expected output)
├── results
│   └── results.log              # Leaderboard/log file updated on each correct submission
├── scripts
│   ├── run_tests.sh             # Script that runs a submission, times it, and invokes validation
│   └── validate_solution.py     # Python script that checks correctness, updates leaderboard, etc.
├── README.md                    # Submission guidelines and instructions
└── (Subdirectories for submitted solutions, e.g. python/, cpp/, etc.)




## Submission Guidelines

1. **Language & File Naming:**  
   - You may implement your solution in **any programming language**.
   - **All solution files must be placed under the `solutions/` directory.**
   - **File naming convention:**  
     Your solution file **must be named** using your **GitHub username** followed by `_solution` and the appropriate extension.  
     For example:  
       - `alice_solution.py`  
       - `bob_solution.cpp`  
       - `charlie_solution.js`  
     
     **Important:** The username in the solution filename must exactly match your GitHub username.  
     If the filename does not follow this format, or the username does not match your GitHub username (as determined by the `GITHUB_ACTOR` environment variable in GitHub Actions), your submission will be rejected.

   - **Allowed Changes:**  
     External contributors may modify **only** files under the `solutions/` directory. Any changes to files outside this folder (such as configuration files or scripts) will cause your submission to be automatically rejected.

2. **Input:**  
   - Your solution must use the provided configuration from [`config/input.json`](config/input.json).  
   - **Example configuration:**
     ```json
     {
         "pieces": [
             [3, 2, 1],
             [4, 3, 5],
             [5, 4, 3],
             [1, 4, 2],
             [5, 1, 4],
             [3, 5, 2],
             [2, 4, 5],
             [1, 2],
             [1, 3]
         ],
         "boardSize": [5, 5]
     }
     ```

3. **Output Format:**  
   Your solution must output a JSON list where each element is an object containing:
   - `"piece"`: an array representing one puzzle piece.
   - `"position"`: an array with the 2D coordinate for the starting cell.
   - `"orientation"`: a string value—either `"h"`, `"hr"`, `"v"`, or `"vr"`.

   **Example output:**
   ```json
   [
       { "piece": [5, 4, 3], "position": [0, 0], "orientation": "h" },
       { "piece": [1, 4, 2], "position": [0, 3], "orientation": "hr" }
   ]


4. **Local Testing:**  
   You can test your solution locally using the provided scripts. For example, if you are using a UNIX-like shell:
   ```bash
   cd scripts
   ./run_tests.sh ../solutions/<your_solution_directory>/<github_username>_solution.py
