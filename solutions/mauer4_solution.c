#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_BOARD_SIZE 10
#define MAX_PIECES 20
#define MAX_PIECE_LENGTH 3

// Data structure for a puzzle piece.
typedef struct {
    int nums[MAX_PIECE_LENGTH];
    int len;  // actual length (2 or 3)
} Piece;

// Orientation enumeration.
typedef enum { H, HR, V, VR } Orientation;

// A placement records which piece was placed at what position and in which orientation.
typedef struct {
    Piece *piece;
    int row;
    int col;
    Orientation orient;
} Placement;

// Global board and configuration variables.
int board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
int boardRows, boardCols;

Piece pieces[MAX_PIECES];
int numPieces;

// For storing the solution (we only need the first valid solution).
Placement currentSolution[MAX_PIECES];
int solutionFound = 0;

// Check winning condition: here we require that the sum of each row and each column is exactly 15.
int winning_condition() {
    for (int i = 0; i < boardRows; i++){
        int sum = 0;
        for (int j = 0; j < boardCols; j++){
            sum += board[i][j];
        }
        if(sum != 15)
            return 0;
    }
    for (int j = 0; j < boardCols; j++){
        int sum = 0;
        for (int i = 0; i < boardRows; i++){
            sum += board[i][j];
        }
        if(sum != 15)
            return 0;
    }
    return 1;
}

// Recursive backtracking solver.
// pieceIndex: index of the piece to place next.
void solve(int pieceIndex) {
    if (solutionFound) return;
    if (pieceIndex == numPieces) {
        if (winning_condition()) {
            solutionFound = 1;
        }
        return;
    }
    Piece *p = &pieces[pieceIndex];
    // Try every cell (i, j) as a potential starting location.
    for (int i = 0; i < boardRows; i++){
        for (int j = 0; j < boardCols; j++){
            // Try horizontal normal placement.
            if (j + p->len <= boardCols) {
                int canPlace = 1;
                // Check that the cells are empty.
                for (int k = 0; k < p->len; k++){
                    if (board[i][j+k] != 0) { canPlace = 0; break; }
                }
                if (canPlace) {
                    // Check that none of the numbers in p appear anywhere in row i.
                    for (int k = 0; k < p->len && canPlace; k++){
                        for (int col = 0; col < boardCols; col++){
                            if (board[i][col] == p->nums[k]) { canPlace = 0; break; }
                        }
                    }
                    // Check that for each cell (i, j+k), p->nums[k] does not already appear in that column.
                    for (int k = 0; k < p->len && canPlace; k++){
                        for (int row = 0; row < boardRows; row++){
                            if (board[row][j+k] == p->nums[k]) { canPlace = 0; break; }
                        }
                    }
                    if (canPlace) {
                        // Place the piece in normal order.
                        for (int k = 0; k < p->len; k++){
                            board[i][j+k] = p->nums[k];
                        }
                        currentSolution[pieceIndex].piece = p;
                        currentSolution[pieceIndex].row = i;
                        currentSolution[pieceIndex].col = j;
                        currentSolution[pieceIndex].orient = H;
                        solve(pieceIndex + 1);
                        if (solutionFound) return;
                        // Backtrack.
                        for (int k = 0; k < p->len; k++){
                            board[i][j+k] = 0;
                        }
                    }
                }
            }
            // Try horizontal reversed placement.
            if (j + p->len <= boardCols) {
                int canPlace = 1;
                for (int k = 0; k < p->len; k++){
                    if (board[i][j+k] != 0) { canPlace = 0; break; }
                }
                if (canPlace) {
                    // Check row constraint with reversed order.
                    for (int k = 0; k < p->len && canPlace; k++){
                        for (int col = 0; col < boardCols; col++){
                            if (board[i][col] == p->nums[p->len - 1 - k]) { canPlace = 0; break; }
                        }
                    }
                    // Check column constraint: for each column j+k, the corresponding number is p->nums[p->len-1-k].
                    for (int k = 0; k < p->len && canPlace; k++){
                        for (int row = 0; row < boardRows; row++){
                            if (board[row][j+k] == p->nums[p->len - 1 - k]) { canPlace = 0; break; }
                        }
                    }
                    if (canPlace) {
                        for (int k = 0; k < p->len; k++){
                            board[i][j+k] = p->nums[p->len - 1 - k];
                        }
                        currentSolution[pieceIndex].piece = p;
                        currentSolution[pieceIndex].row = i;
                        currentSolution[pieceIndex].col = j;
                        currentSolution[pieceIndex].orient = HR;
                        solve(pieceIndex + 1);
                        if (solutionFound) return;
                        for (int k = 0; k < p->len; k++){
                            board[i][j+k] = 0;
                        }
                    }
                }
            }
            // Try vertical normal placement.
            if (i + p->len <= boardRows) {
                int canPlace = 1;
                for (int k = 0; k < p->len; k++){
                    if (board[i+k][j] != 0) { canPlace = 0; break; }
                }
                if (canPlace) {
                    // Check column constraint: ensure none of the piece’s numbers appear in column j.
                    for (int k = 0; k < p->len && canPlace; k++){
                        for (int row = 0; row < boardRows; row++){
                            if (board[row][j] == p->nums[k]) { canPlace = 0; break; }
                        }
                    }
                    // Check row constraint for each cell in vertical order.
                    for (int k = 0; k < p->len && canPlace; k++){
                        for (int col = 0; col < boardCols; col++){
                            if (board[i+k][col] == p->nums[k]) { canPlace = 0; break; }
                        }
                    }
                    if (canPlace) {
                        for (int k = 0; k < p->len; k++){
                            board[i+k][j] = p->nums[k];
                        }
                        currentSolution[pieceIndex].piece = p;
                        currentSolution[pieceIndex].row = i;
                        currentSolution[pieceIndex].col = j;
                        currentSolution[pieceIndex].orient = V;
                        solve(pieceIndex + 1);
                        if (solutionFound) return;
                        for (int k = 0; k < p->len; k++){
                            board[i+k][j] = 0;
                        }
                    }
                }
            }
            // Try vertical reversed placement.
            if (i + p->len <= boardRows) {
                int canPlace = 1;
                for (int k = 0; k < p->len; k++){
                    if (board[i+k][j] != 0) { canPlace = 0; break; }
                }
                if (canPlace) {
                    for (int k = 0; k < p->len && canPlace; k++){
                        for (int row = 0; row < boardRows; row++){
                            if (board[row][j] == p->nums[p->len - 1 - k]) { canPlace = 0; break; }
                        }
                    }
                    for (int k = 0; k < p->len && canPlace; k++){
                        for (int col = 0; col < boardCols; col++){
                            if (board[i+k][col] == p->nums[p->len - 1 - k]) { canPlace = 0; break; }
                        }
                    }
                    if (canPlace) {
                        for (int k = 0; k < p->len; k++){
                            board[i+k][j] = p->nums[p->len - 1 - k];
                        }
                        currentSolution[pieceIndex].piece = p;
                        currentSolution[pieceIndex].row = i;
                        currentSolution[pieceIndex].col = j;
                        currentSolution[pieceIndex].orient = VR;
                        solve(pieceIndex + 1);
                        if (solutionFound) return;
                        for (int k = 0; k < p->len; k++){
                            board[i+k][j] = 0;
                        }
                    }
                }
            }
        }
    }
}

int main() {
    // In a full solution, you would read the input JSON from STDIN.
    // For simplicity, we hardcode the configuration as per the Python version.
    boardRows = 5;
    boardCols = 5;
    numPieces = 9;
    
    // Define pieces:
    pieces[0].len = 3; pieces[0].nums[0] = 3; pieces[0].nums[1] = 2; pieces[0].nums[2] = 1;
    pieces[1].len = 3; pieces[1].nums[0] = 4; pieces[1].nums[1] = 3; pieces[1].nums[2] = 5;
    pieces[2].len = 3; pieces[2].nums[0] = 5; pieces[2].nums[1] = 4; pieces[2].nums[2] = 3;
    pieces[3].len = 3; pieces[3].nums[0] = 1; pieces[3].nums[1] = 4; pieces[3].nums[2] = 2;
    pieces[4].len = 3; pieces[4].nums[0] = 5; pieces[4].nums[1] = 1; pieces[4].nums[2] = 4;
    pieces[5].len = 3; pieces[5].nums[0] = 3; pieces[5].nums[1] = 5; pieces[5].nums[2] = 2;
    pieces[6].len = 3; pieces[6].nums[0] = 2; pieces[6].nums[1] = 4; pieces[6].nums[2] = 5;
    pieces[7].len = 2; pieces[7].nums[0] = 1; pieces[7].nums[1] = 2;
    pieces[8].len = 2; pieces[8].nums[0] = 1; pieces[8].nums[1] = 3;
    
    // Initialize board to zeros.
    for (int i = 0; i < boardRows; i++){
        for (int j = 0; j < boardCols; j++){
            board[i][j] = 0;
        }
    }
    
    // Begin recursive solving.
    solve(0);
    
    if (solutionFound) {
        // Print the first solution in JSON format.
        // Format: [ {"piece": [num, ...], "position": [row, col], "orientation": "h" or "hr" or "v" or "vr"}, ... ]
        printf("[");
        for (int i = 0; i < numPieces; i++) {
            Placement p = currentSolution[i];
            printf("{\"piece\": [");
            for (int k = 0; k < p.piece->len; k++){
                printf("%d", p.piece->nums[k]);
                if (k < p.piece->len - 1)
                    printf(", ");
            }
            printf("], \"position\": [%d, %d], \"orientation\": \"", p.row, p.col);
            switch (p.orient) {
                case H:  printf("h"); break;
                case HR: printf("hr"); break;
                case V:  printf("v"); break;
                case VR: printf("vr"); break;
            }
            printf("\"}");
            if (i < numPieces - 1)
                printf(", ");
        }
        printf("]\n");
    } else {
        printf("{\"error\": \"No valid solution found\"}\n");
    }
    return 0;
}