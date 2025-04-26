from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Inisialisasi grid kosong 4x4
def initialize_grid():
    grid = [[0] * 4 for _ in range(4)]
    add_random_tile(grid)
    add_random_tile(grid)
    return grid

# Fungsi untuk menambahkan tile baru secara acak
def add_random_tile(grid):
    empty_cells = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = random.choice([2, 4])

# Fungsi untuk menggeser grid ke kiri
def slide_left(row):
    new_row = [i for i in row if i != 0]
    for i in range(len(new_row) - 1):
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            new_row[i + 1] = 0
    new_row = [i for i in new_row if i != 0]
    return new_row + [0] * (4 - len(new_row))

# Fungsi untuk menggerakkan grid berdasarkan arah
def move(grid, direction):
    if direction == 'left':
        grid = [slide_left(row) for row in grid]
    elif direction == 'right':
        grid = [slide_left(row[::-1])[::-1] for row in grid]
    elif direction == 'up':
        grid = list(map(list, zip(*grid)))
        grid = [slide_left(row) for row in grid]
        grid = list(map(list, zip(*grid)))
    elif direction == 'down':
        grid = list(map(list, zip(*grid)))
        grid = [slide_left(row[::-1])[::-1] for row in grid]
        grid = list(map(list, zip(*grid)))
    return grid

# Fungsi untuk memeriksa apakah tidak ada gerakan yang mungkin
def is_game_over(grid):
    if any(0 in row for row in grid):
        return False
    for row in grid:
        for i in range(3):
            if row[i] == row[i + 1]:
                return False
    for col in range(4):
        for row in range(3):
            if grid[row][col] == grid[row + 1][col]:
                return False
    return True

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk mengambil grid dalam bentuk JSON
@app.route('/get_grid')
def get_grid():
    grid = initialize_grid()
    return jsonify(grid)

# Route untuk memproses pergerakan
@app.route('/move', methods=['POST'])
def move_tiles():
    data = request.json
    grid = data['grid']
    direction = data['direction']
    grid = move(grid, direction)
    
    if any(any(cell == 0 for cell in row) for row in grid):
        add_random_tile(grid)

    game_over = is_game_over(grid)
    
    return jsonify({"grid": grid, "game_over": game_over})

# Route untuk mereset game
@app.route('/reset', methods=['POST'])
def reset_game():
    grid = initialize_grid()
    return jsonify({"grid": grid})

if __name__ == '__main__':
    app.run(debug=True)
