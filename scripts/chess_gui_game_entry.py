import os
import tkinter as tk
import sqlite3
import glob
from tkinter import messagebox, simpledialog
from chess_classes import Game, League

class ChessLeagueGUI:
    def __init__(self, league):
        self.league = league
        self.current_round = None
        self.current_game = 1
        self.games_played = []

        self.root = tk.Tk()
        self.root.title("Chess League")

        self.white_label = tk.Label(self.root, text="White Player:")
        self.white_label.grid(row=0, column=0, padx=10, pady=10)
        self.white_entry = tk.Entry(self.root)
        self.white_entry.grid(row=0, column=1, padx=10, pady=10)

        self.black_label = tk.Label(self.root, text="Black Player:")
        self.black_label.grid(row=1, column=0, padx=10, pady=10)
        self.black_entry = tk.Entry(self.root)
        self.black_entry.grid(row=1, column=1, padx=10, pady=10)

        self.outcome_label = tk.Label(self.root, text="Outcome:")
        self.outcome_label.grid(row=2, column=0, padx=10, pady=10)
        self.outcome_entry = tk.Entry(self.root)
        self.outcome_entry.grid(row=2, column=1, padx=10, pady=10)

        self.link_label = tk.Label(self.root, text="Game Link:")
        self.link_label.grid(row=3, column=0, padx=10, pady=10)
        self.link_entry = tk.Entry(self.root)
        self.link_entry.grid(row=3, column=1, padx=10, pady=10)

        self.next_button = tk.Button(self.root, text="Next Game", command=self.next_game)
        self.next_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.load_previous_round()

        self.root.mainloop()

    def load_previous_round(self):
        round_number = max(self.get_existing_rounds()) + 1 if self.get_existing_rounds() else 1
        prv_round = f"round_{round_number}.db"

        if os.path.exists(prv_round):
            conn = sqlite3.connect(prv_round)
            c = conn.cursor()

            c.execute("SELECT * FROM games")
            data = c.fetchall()
            for row in data:
                white_player, black_player, outcome, link = row
                game = Game(white_player, black_player, outcome, link)
                self.games_played.append(game)

            self.current_round = round_number

            conn.close()

    def get_existing_rounds(self):
        round_files = glob.glob("*_round_*.db")
        return [self.get_round_number_from_db_file(file) for file in round_files]

    def get_round_number_from_db_file(self, db_file):
        return int(db_file.split("_")[2].split(".")[0])

    def next_game(self):
        if self.current_game == 1:
            round_number = simpledialog.askinteger("Round Number", "Enter the round number:")
            if not round_number:
                return
            time_control = simpledialog.askstring("Time Control", "Enter the time control:")
            if not time_control:
                return
            self.current_round = round_number
            self.create_round_database(time_control, round_number)

        white_player = self.white_entry.get()
        black_player = self.black_entry.get()
        outcome = self.outcome_entry.get()
        link = self.link_entry.get()

        if not white_player or not black_player or not outcome or not link:
            messagebox.showerror("Error", "Please enter all fields.")
            return

        if not self.check_player_exists(white_player) or not self.check_player_exists(black_player):
            messagebox.showerror("Error", "One or both players do not exist.")
            return

        game = Game(white_player, black_player, outcome, link)
        self.update_player_stats(game)
        self.games_played.append(game)

        self.white_entry.delete(0, tk.END)
        self.black_entry.delete(0, tk.END)
        self.outcome_entry.delete(0, tk.END)
        self.link_entry.delete(0, tk.END)

        self.current_game += 1

        if self.current_game > 6:
            self.save_round()
            self.root.destroy()

    def check_player_exists(self, player_name):
        db_file = f"{player_name}.db"
        return os.path.exists(db_file)

    def update_player_stats(self, game):
        white_conn = sqlite3.connect(f"{game.white_player}.db")
        white_c = white_conn.cursor()
        black_conn = sqlite3.connect(f"{game.black_player}.db")
        black_c = black_conn.cursor()

        if game.outcome == "Win":
            white_c.execute("UPDATE player_stats SET wins = wins + 1, points = points + 1 WHERE league = ?", (self.league.name,))
            black_c.execute("UPDATE player_stats SET losses = losses + 1 WHERE league = ?", (self.league.name,))
        elif game.outcome == "Loss":
            white_c.execute("UPDATE player_stats SET losses = losses + 1 WHERE league = ?", (self.league.name,))
            black_c.execute("UPDATE player_stats SET wins = wins + 1, points = points + 1 WHERE league = ?", (self.league.name,))
        elif game.outcome == "Draw":
            white_c.execute("UPDATE player_stats SET draws = draws + 1, points = points + 0.5 WHERE league = ?", (self.league.name,))
            black_c.execute("UPDATE player_stats SET draws = draws + 1, points = points + 0.5 WHERE league = ?", (self.league.name,))

        white_conn.commit()
        white_conn.close()
        black_conn.commit()
        black_conn.close()

    def create_round_database(self, time_control, round_number):
        db_file = f"{time_control}_round_{round_number}.db"
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS games (white_player TEXT, black_player TEXT, outcome TEXT, link TEXT)")

        conn.commit()
        conn.close()

    def save_round(self):
        time_control = simpledialog.askstring("Time Control", "Enter the time control:")
        round_number = self.current_round

        db_file = f"{time_control}_round_{round_number}.db"
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        for game in self.games_played:
            c.execute("INSERT INTO games VALUES (?, ?, ?, ?)",
                      (game.white_player, game.black_player, game.outcome, game.link))

        conn.commit()
        conn.close()

        conn = sqlite3.connect("rounds.db")
        c = conn.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS rounds (round_number INTEGER, time_control TEXT, league TEXT)")
        c.execute("INSERT INTO rounds VALUES (?, ?, ?)", (round_number, time_control, self.league.name))

        conn.commit()
        conn.close()

league = League("Blitz League", [])  # Replace with your league instance
league.add_round([])  # Add an empty round to start

gui = ChessLeagueGUI(league)

