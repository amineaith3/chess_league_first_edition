import tkinter as tk
import sqlite3
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
import glob
import os

dl = "Player Data"
rd = "Round Data"

class PlayerDataGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(dl)

        self.player_button = tk.Button(self.root, text=dl, command=self.show_player_data)
        self.player_button.pack(padx=10, pady=10)

        self.round_button = tk.Button(self.root, text=rd, command=self.show_round_data)
        self.round_button.pack(padx=10, pady=10)

        self.data_labels = {
            dl: "Player Data",
            rd: "Round Data"
        }

        self.root.mainloop()

    def show_player_data(self):
        label = self.data_labels[dl]
        player_name = simpledialog.askstring(label, "Enter the player's name:")
        if player_name:
            self.display_player_data(label, player_name)

    def display_player_data(self, label, player_name):
        db_file = f"{player_name}.db"
        if os.path.exists(db_file):
            conn = sqlite3.connect(db_file)
            c = conn.cursor()

            if self.table_exists(c, "player_stats"):
                c.execute("SELECT * FROM player_stats")
                data = c.fetchall()

                if data:
                    formatted_data = self.format_player_data(data)
                    messagebox.showinfo(label, f"Player: {player_name}\n\n{formatted_data}")
                else:
                    messagebox.showinfo(label, "No data found for the requested player.")
            else:
                messagebox.showerror("Error", f"Database table not found for player: {player_name}")

            conn.close()
        else:
            messagebox.showerror("Error", f"Database not found for player: {player_name}")

    def format_player_data(self, data):
        formatted_data = ""
        for row in data:
            league, wins, losses, draws, points, rank = row
            formatted_data += f"{league} games: \n"
            formatted_data += f"wins: {wins} ---- losses: {losses} ---- draws: {draws} ---- points: {points} ---- rank: {rank}\n\n"
        return formatted_data

    def show_round_data(self):
        label = self.data_labels[rd]
        round_number = simpledialog.askinteger(label, "Enter the round number:")
        if round_number:
            self.display_round_data(label, round_number)

    def display_round_data(self, label, round_number):
        db_file = f"round_{round_number}.db"
        if os.path.exists(db_file):
            conn = sqlite3.connect(db_file)
            c = conn.cursor()

            if self.table_exists(c, "games"):
                c.execute("SELECT * FROM games")
                data = c.fetchall()

                if data:
                    messagebox.showinfo(label, f"Round: {round_number}\n\n{data}")
                else:
                    messagebox.showinfo(label, f"No data found for round: {round_number}")
            else:
                messagebox.showerror("Error", f"Database table not found for round: {round_number}")

            conn.close()
        else:
            messagebox.showerror("Error", f"Database not found for round: {round_number}")

    def table_exists(self, cursor, table_name):
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        return cursor.fetchone() is not None

data_gui = PlayerDataGUI()

