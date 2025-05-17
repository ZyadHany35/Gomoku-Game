import tkinter as tk
from tkinter import messagebox
from gomoku import GomokuGame
from utils import *
from AIPlayer import *

BOARD_SIZE = 15
CELL_SIZE = 40

class GomokuBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku Game")
        # title
        label = tk.Label(root, text="Gomoku AI Game",font=("Helvetica", 20, "bold"))
        label.pack(padx=10)

        # board
        self.canvas = tk.Canvas(root, width=BOARD_SIZE * CELL_SIZE, height=BOARD_SIZE * CELL_SIZE + 20,background="#d2a77c")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.human_move)


        self.game = GomokuGame(BOARD_SIZE)
        self.human_turn = True
        self.ai_vs_ai_mode = False

        self.draw_board()

        # turns
        self.turn_frame = tk.Frame(root, borderwidth=2, relief="groove", pady=5)
        self.turn_frame.pack(pady=(5, 0))

        self.turn_label = tk.Label(
            self.turn_frame,
            text="Turn: Human",
            font=("Helvetica", 14, "bold"),
            fg="black"
        )
        self.turn_label.pack()


        # dropout 
        self.algorithm_var = tk.IntVar(value=(1,"Minimax"))
        self.create_algorithm_selector()
        
        # buttons
        self.bottom_frame = tk.Frame(root, padx=10, pady=10)
        self.bottom_frame.pack()

        self.reset_btn = HoverButton(
            self.bottom_frame,
            text="Reset",
            command=self.reset_game,
            bg="#7CA7D2",
            fg="black",
            font=("Helvetica", 12, "bold"),
            relief=tk.RAISED,
            borderwidth=3,
            padx=15,
            pady=10,
            activebackground="#495ab6",
            activeforeground="black"
        )
        self.reset_btn.pack(side=tk.LEFT, padx=20)

        self.ai_btn = HoverButton(
            self.bottom_frame,
            text="MiniMax vs Alphabeta",
            command=self.ai_vs_ai,
            bg="#7CA7D2",
            fg="black",
            font=("Helvetica", 12, "bold"),
            relief=tk.RAISED,
            borderwidth=3,
            padx=15,
            pady=10,
            activebackground="#495ab6",
            activeforeground="black"
        )
        self.ai_btn.pack(side=tk.LEFT, padx=20)

        self.canvas.bind("<Motion>", self.hover_highlight)
        self.highlight_id = None

    def update_turn_label(self):
        if self.ai_vs_ai_mode:
            algo = self.algorithm_var.get()
            ai_player = "Minimax" if self.game.current_player == 1 else "AlphaBeta"
            self.turn_label.config(text=f"Turn: {ai_player}")
        else:
            if self.human_turn:
                self.turn_label.config(text="Turn: Human")
            else:
                algo = self.algorithm_var.get()
                self.turn_label.config(text=f"Turn: {algo}")

    def draw_board(self):
        self.canvas.delete("all")
        self.highlight_id = None

        i = 0
        for i in range(BOARD_SIZE):
            self.canvas.create_line(i * CELL_SIZE + 20, 20, i * CELL_SIZE + 20, CELL_SIZE * (BOARD_SIZE - 1) + 20)
            self.canvas.create_line(20, i * CELL_SIZE + 20, CELL_SIZE * (BOARD_SIZE - 1) + 20, i * CELL_SIZE + 20)

        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.game.board[x][y] != 0:
                    color = "black" if self.game.board[x][y] == 1 else "white"
                    cx = x * CELL_SIZE + CELL_SIZE // 2
                    cy = y * CELL_SIZE + CELL_SIZE // 2
                    r = 10

                    self.canvas.create_oval(
                        cx - r, cy - r,
                        cx + r, cy + r,
                        fill = color
                    )

        self.canvas.create_line(
            0, BOARD_SIZE * CELL_SIZE + 20,
            BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE + 20,
            fill="black",
            width=4)



    def create_algorithm_selector(self):
        selector_frame = tk.Frame(self.root)
        selector_frame.pack(pady=10)

        self.algorithm_var = tk.StringVar(value="Minimax")
        tk.Label(selector_frame, text="AI Algorithm:", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=5)

        algo_menu = tk.OptionMenu(
            selector_frame,
            self.algorithm_var,
            "Minimax",
            "AlphaBeta"
        )
        algo_menu.pack(side=tk.LEFT, padx=10)
        algo_menu.config(
            font=("Helvetica", 12, "bold"),
            bg="#7CA7D2",
            relief=tk.RAISED,
            width=10
        )

        self.difficulty_var = tk.StringVar(value="Easy")
        tk.Label(selector_frame, text="Difficulty:", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=5)

        diff_menu = tk.OptionMenu(
            selector_frame,
            self.difficulty_var,
            "Easy",
            "Hard"
        )
        diff_menu.pack(side=tk.LEFT)
        diff_menu.config(
            font=("Helvetica", 12, "bold"),
            bg="#7CA7D2",
            relief=tk.RAISED,
            width=10
        )


    def hover_highlight(self, event):
        if self.highlight_id:
            self.canvas.delete(self.highlight_id)

        x, y = event.y // CELL_SIZE, event.x // CELL_SIZE

        if (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and
            self.game.board[x][y] == 0 and
            self.human_turn and not self.ai_vs_ai_mode):

            cx = y * CELL_SIZE + CELL_SIZE // 2
            cy = x * CELL_SIZE + CELL_SIZE // 2
            r = 10

            self.highlight_id = self.canvas.create_oval(
                cx - r, cy - r,
                cx + r, cy + r,
                outline="gray",
                width=2,
                fill=""
            )

    def human_move(self, event):
        if not self.human_turn or self.ai_vs_ai_mode:
            return
        x, y =  event.y // CELL_SIZE, event.x // CELL_SIZE
        if self.game.make_move(x, y):

            self.draw_board()
            if self.game.check_win():
                messagebox.showinfo("Game Over", f"{'Black (human)' if self.game.current_player == 2 else 'White (ai)'} wins!")
                self.human_turn = False
                return
            self.human_turn = False
            self.update_turn_label()
            self.root.after(500, self.ai_move)

    def ai_move(self):
        depth = 1 if self.difficulty_var.get() == "Easy" else 2
        if self.algorithm_var.get() == "Minimax":
            move = get_best_move_minimax(self.game, depth)
        else:
            move = get_best_move_alphabeta(self.game, depth)

        if move:
            self.game.make_move(*move)
            self.draw_board()
            if self.game.check_win():
                messagebox.showinfo("Game Over", f"{'Black (human)' if self.game.current_player == 2 else 'White (ai)'} wins!")
                return
        self.human_turn = True
        self.update_turn_label()


    def reset_game(self):
        self.game.reset()
        self.human_turn = True
        self.ai_vs_ai_mode = False
        self.update_turn_label()
        self.draw_board()

    def ai_vs_ai(self):
        self.ai_vs_ai_mode = True
        if self.game.check_win():
            messagebox.showinfo("Game Over", f"{'Black (minimax)' if self.game.current_player == 2 else 'White (alphabeta)'} wins!")
            return

        depth = 1 if self.difficulty_var.get() == "Easy" else 2

        if self.game.current_player == 1:
            move = get_best_move_minimax(self.game, depth)
        else:
            move = get_best_move_alphabeta(self.game, depth)

        if move:
            self.game.make_move(*move)
            self.draw_board()

        self.update_turn_label()
        self.root.after(500, self.ai_vs_ai)

