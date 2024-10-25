import tkinter as tk
from tkinter import messagebox
from random import shuffle

# Memory Game Class
class MemoryGame:
    def __init__(self, root, grid_size):
        self.root = root
        self.grid_size = grid_size
        self.buttons = []
        self.values = []
        self.revealed_buttons = []
        
        # Setting up window styles
        self.root.title("Memory Game")
        self.root.config(bg="#ADD8E6")  # Light blue background

        # Reset Button
        self.reset_button = tk.Button(self.root, text="Reset Game", font=("Helvetica", 14), bg="#FF6347", fg="white", command=self.reset_game)
        self.reset_button.grid(row=0, column=0, columnspan=self.grid_size, pady=(10, 20))

        # Setup game values and UI grid
        self.setup_game()
        self.create_grid()

    def setup_game(self):
        # Creating number pairs for the grid and shuffling them
        num_pairs = (self.grid_size * self.grid_size) // 2
        numbers = list(range(1, num_pairs + 1)) * 2
        shuffle(numbers)
        self.values = [numbers[i * self.grid_size:(i + 1) * self.grid_size] for i in range(self.grid_size)]

    def create_grid(self):
        # Creating grid of buttons with styling
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                btn = tk.Button(self.root, text="?", font=("Helvetica", 20, "bold"), width=6, height=3,
                                bg="#87CEEB", fg="#FFFFFF", relief="raised", 
                                command=lambda i=i, j=j: self.reveal_number(i, j))
                btn.grid(row=i + 1, column=j, padx=5, pady=5)  # Adjust row index by +1 for reset button
                row.append(btn)
            self.buttons.append(row)

    def reveal_number(self, i, j):
        # Reveal the button's number if only two are selected
        if len(self.revealed_buttons) < 2 and self.buttons[i][j]["text"] == "?":
            self.buttons[i][j]["text"] = str(self.values[i][j])
            self.buttons[i][j]["bg"] = "#FFD700"  # Gold color on reveal
            self.revealed_buttons.append((i, j))

            # Check for match if two buttons are revealed
            if len(self.revealed_buttons) == 2:
                self.root.after(800, self.check_match)

    def check_match(self):
        # Check if the revealed numbers are a match
        (i1, j1), (i2, j2) = self.revealed_buttons

        if self.values[i1][j1] == self.values[i2][j2]:
            # If they match, disable buttons and change color
            self.buttons[i1][j1]["state"] = "disabled"
            self.buttons[i2][j2]["state"] = "disabled"
            self.buttons[i1][j1]["bg"] = "#32CD32"  # Green for matched
            self.buttons[i2][j2]["bg"] = "#32CD32"
        else:
            # If they don't match, reset after a short delay
            self.buttons[i1][j1]["text"] = "?"
            self.buttons[i2][j2]["text"] = "?"
            self.buttons[i1][j1]["bg"] = "#87CEEB"  # Reset to default
            self.buttons[i2][j2]["bg"] = "#87CEEB"

        # Reset revealed buttons list
        self.revealed_buttons = []

        # Check if all buttons are matched
        if all(btn["state"] == "disabled" for row in self.buttons for btn in row):
            messagebox.showinfo("Congratulations!", "You've matched all pairs!")
            self.root.quit()

    def reset_game(self):
        # Reset the game state: shuffle values and reset buttons
        shuffle([num for sublist in self.values for num in sublist])  # Shuffle flat list of values
        self.setup_game()  # Re-setup values
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                btn = self.buttons[i][j]
                btn["text"] = "?"
                btn["bg"] = "#87CEEB"
                btn["state"] = "normal"  # Enable all buttons

        self.revealed_buttons = []

# Game Initialization Function
def start_game(grid_size):
    root = tk.Tk()
    MemoryGame(root, grid_size)
    root.mainloop()

# Main Menu for Grid Size Selection
def main():
    # Main menu window for selecting grid size
    root = tk.Tk()
    root.title("Select Grid Size")
    root.geometry("300x200")
    root.config(bg="#FFDEAD")  # Light coral background
    
    # Title label
    tk.Label(root, text="Choose a grid size:", font=("Helvetica", 16, "bold"), bg="#FFDEAD").pack(pady=20)

    # Buttons for each grid size
    for label, size in [("4x4", 4), ("6x6", 6), ("8x8", 8)]:
        tk.Button(root, text=label, font=("Helvetica", 14), bg="#FF7F50", fg="white", width=10,
                  command=lambda size=size: [root.destroy(), start_game(size)]).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
