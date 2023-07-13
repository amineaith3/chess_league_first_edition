class Player:
    def __init__(self, name):
        self.name = name
        self.games_played = 0
        self.games_won = 0
        self.games_lost = 0
        self.games_drawn = 0
        self.points = 0
        self.ranks = {'blitz': 0, 'rapid': 0, 'bullet': 0}

    def update_stats(self, outcome):
        self.games_played += 1
        if outcome == 'win':
            self.games_won += 1
            self.points += 1
        elif outcome == 'loss':
            self.games_lost += 1
        elif outcome == 'draw':
            self.games_drawn += 1
            self.points += 0.5

    def set_rank(self, league, rank):
        self.ranks[league] = rank

    def get_rank(self, league):
        return self.ranks[league]


class Game:
    def __init__(self, white_player, black_player, outcome, link):
        self.white_player = white_player
        self.black_player = black_player
        self.outcome = outcome
        self.link = link


class League:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.rounds = []

    def add_round(self, games):
        self.rounds.append(games)

    def get_player_by_name(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return None

