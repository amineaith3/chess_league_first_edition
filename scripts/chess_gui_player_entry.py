import tkinter as tk
import sqlite3
from tkinter import messagebox
import os
import glob

class Player:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.points = 0

class PlayerRegistrationGUI:
    def __init__(self):
        self.players = []
        self.max_players = 12

        if self.are_players_registered():
            messagebox.showinfo("Information", "All players have been registered.")
            return

        self.root = tk.Tk()
        self.root.title("Player Registration")

        self.name_label = tk.Label(self.root, text="Player Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.phone_label = tk.Label(self.root, text="Phone Number:")
        self.phone_label.grid(row=1, column=0, padx=10, pady=10)
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10)

        self.register_button = tk.Button(self.root, text="Register Player", command=self.register_player)
        self.register_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.root.mainloop()

    def are_players_registered(self):
        db_files = glob.glob("*.db")
        return len(db_files) == self.max_players

    def register_player(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()

        if not name or not phone:
            messagebox.showerror("Error", "Please enter both the player name and phone number.")
            return

        if self.is_duplicate_player(name):
            messagebox.showerror("Error", "A player with the same name already exists.")
            return

        if len(self.players) >= self.max_players:
            messagebox.showinfo("Information", "Maximum number of players reached.")
            return

        player = Player(name, phone)
        self.players.append(player)

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

        if len(self.players) == self.max_players:
            self.register_button.config(state=tk.DISABLED)
            messagebox.showinfo("Information", "Maximum number of players reached.")

        self.initialize_player_database(player)

    def is_duplicate_player(self, name):
        for player in self.players:
            if player.name == name:
                return True
        return False

    def initialize_player_database(self, player):
        db_file = f"{player.name}.db"
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS player_stats (league TEXT, wins INTEGER, losses INTEGER, draws INTEGER, points REAL, rank INTEGER)")

        # Initialize columns for each league
        leagues = ["blitz", "rapid", "bullet"]
        for league in leagues:
            c.execute("INSERT INTO player_stats (league, wins, losses, draws, points, rank) VALUES (?, ?, ?, ?, ?, ?)",
                      (league, 0, 0, 0, 0, 0))

        conn.commit()
        conn.close()

        messagebox.showinfo("Information", f"{player.name}'s database has been initialized.")

registration_gui = PlayerRegistrationGUI()

