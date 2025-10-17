import tkinter as tk
import random

class GameOfLife:
    def __init__(self, master, rows, cols, cell_size):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = self.create_initial_grid()
        self.canvas = tk.Canvas(master, width=cols * cell_size, height=rows * cell_size, bg="white")
        self.canvas.pack()
        self.draw_grid()
        self.running = False

        # Add control buttons (e.g., start, stop, reset)
        start_button = tk.Button(master, text="Start", command=self.start_simulation)
        start_button.pack(side=tk.LEFT)
        stop_button = tk.Button(master, text="Stop", command=self.stop_simulation)
        stop_button.pack(side=tk.LEFT)

    def create_initial_grid(self):
        # Initialize grid with random alive/dead cells
        grid = [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]
        return grid

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = "black" if self.grid[r][c] == 1 else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def update_grid(self):
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                live_neighbors = self.count_live_neighbors(r, c)
                if self.grid[r][c] == 1:  # Alive cell
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_grid[r][c] = 0  # Dies
                    else:
                        new_grid[r][c] = 1  # Survives
                else:  # Dead cell
                    if live_neighbors == 3:
                        new_grid[r][c] = 1  # Becomes alive
        self.grid = new_grid
        self.draw_grid()

    def count_live_neighbors(self, r, c):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor_r, neighbor_c = r + i, c + j
                if 0 <= neighbor_r < self.rows and 0 <= neighbor_c < self.cols:
                    count += self.grid[neighbor_r][neighbor_c]
        return count

    def start_simulation(self):
        self.running = True
        self.run_generation()

    def stop_simulation(self):
        self.running = False

    def run_generation(self):
        if self.running:
            self.update_grid()
            self.master.after(100, self.run_generation) # Schedule next update after 100ms

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Conway's Game of Life")
    game = GameOfLife(root, rows=50, cols=50, cell_size=10)
    root.mainloop()