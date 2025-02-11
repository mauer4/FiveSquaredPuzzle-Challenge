#!/usr/bin/env python3
import numpy as np
import json
import sys

# ---------------------------------------------------------------------
# Puzzle Definitions:
# - Each number represents a type of piece (labels are arbitrary):
#   triangle = 1, target = 2, star = 3, pin = 4, spiral = 5
# ---------------------------------------------------------------------

def legit_placements(board_state, piece):
    placements = []
    # For horizontal placements:
    # The loop range depends on whether the board is completely empty or not.
    for i in range(5 if board_state.sum() else 4):
        for j in range(5 if board_state.sum() else 4):
            # Check that the horizontal segment is empty and fits on the board.
            if j + len(piece) <= 5 and not sum(board_state[i, j:j+len(piece)]):
                # Ensure none of the piece's numbers already appear in that row.
                if not any(num in board_state[i] for num in piece):
                    if len(piece) == 3:
                        # Horizontal normal order: left-to-right
                        if (piece[0] not in board_state[:, j] and 
                            piece[1] not in board_state[:, j+1] and 
                            piece[2] not in board_state[:, j+2]):
                            placements.append(([i, j], 'h'))
                        # Horizontal reversed order: right-to-left
                        if board_state.sum() and (
                            piece[2] not in board_state[:, j] and 
                            piece[1] not in board_state[:, j+1] and 
                            piece[0] not in board_state[:, j+2]):
                            placements.append(([i, j], 'hr'))
                    else:
                        # For pieces of length 2:
                        if board_state.sum() and (
                            piece[0] not in board_state[:, j] and 
                            piece[1] not in board_state[:, j+1]):
                            placements.append(([i, j], 'h'))
                        if board_state.sum() and (
                            piece[1] not in board_state[:, j] and 
                            piece[0] not in board_state[:, j+1]):
                            placements.append(([i, j], 'hr'))
            # For vertical placements:
            # Only check vertical placements if the board is not empty.
            if i + len(piece) <= 5 and board_state.sum() and not sum(board_state[i: i+len(piece), j]):
                # Ensure none of the piece's numbers appear in the column.
                if not any(num in board_state[:, j] for num in piece):
                    if len(piece) == 3:
                        # Vertical normal order: top-to-bottom
                        if (piece[0] not in board_state[i] and 
                            piece[1] not in board_state[i+1] and 
                            piece[2] not in board_state[i+2]):
                            placements.append(([i, j], 'v'))
                        # Vertical reversed order: bottom-to-top
                        if (piece[2] not in board_state[i] and 
                            piece[1] not in board_state[i+1] and 
                            piece[0] not in board_state[i+2]):
                            placements.append(([i, j], 'vr'))
                    else:
                        # For pieces of length 2:
                        if piece[0] not in board_state[i] and piece[1] not in board_state[i+1]:
                            placements.append(([i, j], 'v'))
                        if piece[1] not in board_state[i] and piece[0] not in board_state[i+1]:
                            placements.append(([i, j], 'vr'))
    return placements

def add_piece(board_state, option, piece):
    try:
        # Horizontal normal placement: place piece left-to-right.
        if option[1] == 'h':
            for k in range(len(piece)):
                board_state[option[0][0], option[0][1] + k] = piece[k]
        # Horizontal reversed placement: place piece right-to-left.
        elif option[1] == 'hr':
            for k in range(len(piece)):
                board_state[option[0][0], option[0][1] + k] = piece[-(k + 1)]
        # Vertical normal placement: place piece top-to-bottom.
        elif option[1] == 'v':
            for k in range(len(piece)):
                board_state[option[0][0] + k, option[0][1]] = piece[k]
        # Vertical reversed placement: place piece bottom-to-top.
        elif option[1] == 'vr':
            for k in range(len(piece)):
                board_state[option[0][0] + k, option[0][1]] = piece[-(k + 1)]
    except Exception as e:
        print("Error encountered while placing piece:")
        print("Board state:", board_state)
        print("Option:", option)
        print("Piece:", piece)
        print("Error:", e)
        raise
    return board_state

def find_options(current_board, remaining, path, solutions):
    # If no remaining pieces, check if the solution meets the winning condition.
    if not remaining:
        # Winning condition: each row and each column should average to 15.
        if current_board.sum(0).mean() == 15 and current_board.sum(1).mean() == 15:
            solutions.append(path)
        return
    cur_piece = remaining[0]
    legit_options = legit_placements(current_board, cur_piece)
    remaining_next = remaining[1:]
    
    if not legit_options:
        return
    
    for option in legit_options:
        new_path = list(path)
        new_path.append((cur_piece, option))
        temp_board = current_board.copy()
        temp_board = add_piece(temp_board, option, cur_piece)
        find_options(temp_board, remaining_next, new_path, solutions)

def main():
    # Read input from STDIN (redirected from config/input.json)
    try:
        input_data = json.load(sys.stdin)
    except Exception as e:
        print(json.dumps({"error": "Failed to load input configuration", "details": str(e)}))
        sys.exit(1)
    
    # The input JSON is expected to have "pieces" and "boardSize" keys.
    configuration = input_data.get("pieces")
    board_size = input_data.get("boardSize", [5, 5])
    
    # Initialize the board based on boardSize.
    board = np.zeros((board_size[0], board_size[1]), dtype=int)
    
    solutions = []
    find_options(board, configuration, [], solutions)
    
    # If no solution was found, output an error JSON.
    if not solutions:
        print(json.dumps({"error": "No valid solution found"}))
        return

    # Take the first solution found.
    sol = solutions[0]

    # Convert the solution path to the required JSON format.
    # Each element becomes an object with keys: "piece", "position", and "orientation".
    result = []
    for placement in sol:
        piece, option = placement  # option is a tuple: ([row, col], orientation)
        result.append({
            "piece": piece,
            "position": option[0],
            "orientation": option[1]
        })

    # Output the solution as JSON.
    print(json.dumps(result))

if __name__ == "__main__":
    main()
