import sqlite3
from trueskill import Rating, rate_1vs1, rate

# Existing player ratings
players = {
    "Alexandre":Rating(1000, 1000/3),
    "Antoine":Rating(1000, 1000/3),
    "Martin":Rating(1000, 1000/3),
    "Noémie":Rating(1000, 1000/3),
    "Romain":Rating(1000, 1000/3),
    "Adrien":Rating(1000, 1000/3),
    "Malik":Rating(1000, 1000/3),
    "Arthur":Rating(1000, 1000/3),
    "Gaspard":Rating(1000, 1000/3),
    "Samuel":Rating(1000, 1000/3),
    "Gaetan":Rating(1000, 1000/3),
    "Rodolphe":Rating(1000, 1000/3),
}

class Player_ratings:
    def __init__(self):
        self.conn = sqlite3.connect('player_ratings.db')
        self.cursor = self.conn.cursor()
        
    def create_player(self, name):
        self.cursor.execute('''
            INSERT OR REPLACE INTO player_ratings (name, mu, sigma)
            VALUES (?, ?, ?)
        ''', (name, 1000, 1000/3))
        self.conn.commit()
    
    def get_rating(self, name):
        self.cursor.execute('''SELECT mu, sigma FROM player_ratings WHERE name = ?''', (name,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return Rating(row[0], row[1])
    
    def store_rating(self, name, rating):
        self.cursor.execute('''INSERT OR REPLACE INTO player_ratings (name, mu, sigma) VALUES (?, ?, ?)''', (name, rating.mu, rating.sigma))
        self.conn.commit()
        
    def display_ratings(self):
        self.cursor.execute('''SELECT name, mu, sigma FROM player_ratings ORDER BY mu DESC''')
        for row in self.cursor.fetchall():
            print(f"{row[0]}: {row[1]:.2f} ± {row[2]:.2f}")
            
    def update_ratings_1v1(self, winner_name, loser_name):
        winner = self.get_rating(winner_name)
        loser = self.get_rating(loser_name)
        
        new_winner, new_loser = rate_1vs1(winner, loser, drawn=False)
        
        self.store_rating(winner_name, new_winner)
        self.store_rating(loser_name, new_loser)
    
    def update_ratings_2v2(self, winner_names, loser_names):
        winners = [self.get_rating(name) for name in winner_names]
        losers = [self.get_rating(name) for name in loser_names]
        new_winners, new_losers = rate([winners, losers])
        
        for name, new_rating in zip(winner_names, new_winners):
            self.store_rating(name, new_rating)
        
        for name, new_rating in zip(loser_names, new_losers):
            self.store_rating(name, new_rating)
    
    def __exit__(self):
        self.conn.commit()
        self.conn.close()
        

player_ratings = Player_ratings()
for player in players:
    player_ratings.create_player(player)

# Example usage

# Session 1
player_ratings.update_ratings_2v2(["Martin", "Antoine"], ["Alexandre", "Noémie"])
player_ratings.update_ratings_2v2(["Noémie", "Antoine"], ["Alexandre", "Romain"])
player_ratings.update_ratings_2v2(["Martin", "Alexandre"], ["Romain", "Noémie"])
player_ratings.update_ratings_2v2(["Alexandre", "Antoine"], ["Romain", "Martin"])
player_ratings.update_ratings_2v2(["Romain", "Antoine"], ["Martin", "Noémie"])
player_ratings.update_ratings_2v2(["Alexandre", "Antoine"], ["Martin", "Noémie"])
player_ratings.update_ratings_2v2(["Romain", "Antoine"], ["Alexandre", "Noémie"])
player_ratings.update_ratings_2v2(["Romain", "Alexandre"], ["Martin", "Noémie"])
player_ratings.update_ratings_2v2(["Martin", "Alexandre"], ["Romain", "Antoine"])
player_ratings.update_ratings_2v2(["Martin", "Romain"], ["Antoine", "Noémie"])
player_ratings.update_ratings_2v2(["Martin", "Alexandre"], ["Antoine", "Noémie"])
player_ratings.update_ratings_2v2(["Alexandre", "Antoine"], ["Romain", "Noémie"])
player_ratings.update_ratings_2v2(["Alexandre", "Noémie"], ["Martin", "Romain"])
player_ratings.update_ratings_2v2(["Romain", "Alexandre"], ["Martin", "Antoine"])
player_ratings.update_ratings_2v2(["Romain", "Noémie"], ["Martin", "Antoine"])

# Session 2
player_ratings.update_ratings_1v1("Adrien", "Antoine")
player_ratings.update_ratings_1v1("Alexandre", "Antoine")
player_ratings.update_ratings_1v1("Adrien", "Alexandre")
player_ratings.update_ratings_2v2(["Adrien", "Antoine"], ["Alexandre", "Martin"])
player_ratings.update_ratings_2v2(["Adrien", "Martin"], ["Alexandre", "Antoine"])
player_ratings.update_ratings_2v2(["Adrien", "Noémie"], ["Antoine", "Martin"])
player_ratings.update_ratings_2v2(["Alexandre", "Noémie"], ["Adrien", "Malik"])
player_ratings.update_ratings_2v2(["Alexandre", "Adrien"], ["Antoine", "Martin"])
player_ratings.update_ratings_2v2(["Alexandre", "Antoine"], ["Noémie", "Martin"])
player_ratings.update_ratings_2v2(["Adrien", "Noémie"], ["Antoine", "Malik"])
player_ratings.update_ratings_2v2(["Antoine", "Noémie"], ["Adrien", "Martin"])
player_ratings.update_ratings_2v2(["Adrien", "Noémie"], ["Alexandre", "Martin"])

# Session 3
player_ratings.update_ratings_2v2(["Antoine", "Romain"], ["Noémie", "Samuel"])
player_ratings.update_ratings_2v2(["Arthur", "Alexandre"], ["Martin", "Gaspard"])
player_ratings.update_ratings_2v2(["Romain", "Arthur"], ["Noémie", "Martin"])
player_ratings.update_ratings_2v2(["Alexandre", "Samuel"], ["Antoine", "Gaspard"])
player_ratings.update_ratings_2v2(["Antoine", "Noémie"], ["Martin", "Samuel"])
player_ratings.update_ratings_2v2(["Alexandre", "Romain"], ["Gaspard", "Arthur"])
player_ratings.update_ratings_2v2(["Romain", "Martin"], ["Antoine", "Samuel"])
player_ratings.update_ratings_2v2(["Alexandre", "Gaspard"], ["Arthur", "Malik"])
player_ratings.update_ratings_2v2(["Romain", "Noémie"], ["Samuel", "Gaspard"])
player_ratings.update_ratings_2v2(["Arthur", "Martin"], ["Alexandre", "Antoine"])
player_ratings.update_ratings_2v2(["Alexandre", "Noémie"], ["Romain", "Samuel"])
player_ratings.update_ratings_2v2(["Arthur", "Gaspard"], ["Martin", "Antoine"])
player_ratings.update_ratings_2v2(["Alexandre", "Martin"], ["Noémie", "Romain"])
player_ratings.update_ratings_2v2(["Antoine", "Noémie"], ["Arthur", "Samuel"])

# Session 4
player_ratings.update_ratings_1v1("Antoine", "Romain")
player_ratings.update_ratings_2v2(["Alexandre", "Antoine"], ["Malik", "Romain"])
player_ratings.update_ratings_2v2(["Alexandre", "Romain"], ["Antoine", "Malik"])
player_ratings.update_ratings_2v2(["Alexandre", "Malik"], ["Antoine", "Romain"])
player_ratings.update_ratings_2v2(["Alexandre", "Romain"], ["Antoine", "Malik"])
player_ratings.update_ratings_2v2(["Alexandre", "Antoine"], ["Romain", "Malik"])
player_ratings.update_ratings_2v2(["Antoine", "Romain"], ["Alexandre", "Malik"])
player_ratings.update_ratings_1v1("Alexandre", "Antoine")
player_ratings.update_ratings_1v1("Alexandre", "Romain")
player_ratings.update_ratings_1v1("Romain", "Antoine")
player_ratings.update_ratings_1v1("Alexandre", "Antoine")

# Session 5
player_ratings.update_ratings_1v1("Alexandre", "Gaetan")
player_ratings.update_ratings_2v2(["Alexandre", "Antoine"], ["Gaetan", "Samuel"])
player_ratings.update_ratings_2v2(["Gaetan", "Romain"], ["Antoine", "Samuel"])
player_ratings.update_ratings_2v2(["Antoine", "Romain"], ["Alexandre", "Gaetan"])
player_ratings.update_ratings_2v2(["Antoine", "Alexandre"], ["Romain", "Samuel"])
player_ratings.update_ratings_2v2(["Alexandre", "Romain"], ["Gaetan", "Samuel"])
player_ratings.update_ratings_2v2(["Antoine", "Gaetan"], ["Alexandre", "Samuel"])
player_ratings.update_ratings_2v2(["Antoine", "Gaetan"], ["Romain", "Samuel"])
player_ratings.update_ratings_2v2(["Antoine", "Alexandre"], ["Romain", "Gaetan"])
player_ratings.update_ratings_2v2(["Alexandre", "Samuel"], ["Romain", "Noémie"])
player_ratings.update_ratings_2v2(["Antoine", "Samuel"], ["Gaetan", "Noémie"])
player_ratings.update_ratings_2v2(["Alexandre", "Romain"], ["Gaetan", "Antoine"])
player_ratings.update_ratings_2v2(["Alexandre", "Romain"], ["Antoine", "Samuel"])
player_ratings.update_ratings_2v2(["Alexandre", "Gaetan"], ["Romain", "Samuel"])

# Session 6
player_ratings.update_ratings_1v1("Alexandre", "Martin")
player_ratings.update_ratings_1v1("Antoine", "Rodolphe")
player_ratings.update_ratings_2v2(["Antoine", "Alexandre"], ["Samuel", "Martin"])
player_ratings.update_ratings_2v2(["Antoine", "Martin"], ["Romain", "Samuel"])
player_ratings.update_ratings_2v2(["Alexandre", "Samuel"], ["Romain", "Martin"])
player_ratings.update_ratings_2v2(["Alexandre", "Romain"], ["Antoine", "Samuel"])
player_ratings.update_ratings_2v2(["Alexandre", "Samuel"], ["Antoine", "Romain"])
player_ratings.update_ratings_2v2(["Alexandre", "Antoine"], ["Samuel", "Romain"])
player_ratings.update_ratings_2v2(["Alexandre", "Romain"], ["Antoine", "Samuel"])
player_ratings.update_ratings_2v2(["Alexandre", "Samuel"], ["Romain", "Antoine"])
player_ratings.update_ratings_2v2(["Alexandre", "Antoine"], ["Romain", "Samuel"])
player_ratings.update_ratings_2v2(["Alexandre", "Romain"], ["Antoine", "Samuel"])
player_ratings.update_ratings_2v2(["Alexandre", "Samuel"], ["Antoine", "Romain"])
player_ratings.update_ratings_2v2(["Alexandre", "Antoine"], ["Romain", "Samuel"])

# Session 7
player_ratings.update_ratings_2v2(["Alexandre", "Gaetan"], ["Samuel", "Martin"])
player_ratings.update_ratings_2v2(["Arthur", "Samuel"], ["Romain", "Antoine"])
player_ratings.update_ratings_2v2(["Alexandre", "Antoine"], ["Arthur", "Gaetan"])
player_ratings.update_ratings_2v2(["Alexandre", "Romain"], ["Gaetan", "Samuel"])
player_ratings.update_ratings_2v2(["Romain", "Arthur"], ["Antoine", "Samuel"])
player_ratings.update_ratings_2v2(["Arthur", "Alexandre"], ["Antoine", "Gaetan"])
player_ratings.update_ratings_2v2(["Alexandre", "Samuel"], ["Antoine", "Romain"])
player_ratings.update_ratings_2v2(["Gaetan", "Martin"], ["Arthur", "Samuel"])
player_ratings.update_ratings_2v2(["Alexandre", "Romain"], ["Arthur", "Martin"])
player_ratings.update_ratings_2v2(["Alexandre", "Gaetan"], ["Antoine", "Samuel"])
player_ratings.update_ratings_2v2(["Arthur", "Martin"], ["Alexandre", "Romain"])
player_ratings.update_ratings_2v2(["Antoine", "Gaetan"], ["Alexandre", "Samuel"])
player_ratings.update_ratings_2v2(["Alexandre", "Martin"], ["Romain", "Arthur"])
player_ratings.update_ratings_2v2(["Antoine", "Gaetan"], ["Romain", "Samuel"])
player_ratings.update_ratings_2v2(["Alexandre", "Martin"], ["Gaetan", "Arthur"])

# Session 8
player_ratings.update_ratings_1v1("Antoine", "Samuel")
player_ratings.update_ratings_1v1("Arthur", "Antoine")
player_ratings.update_ratings_1v1("Arthur", "Samuel")
player_ratings.update_ratings_2v2(["Antoine", "Martin"], ["Arthur", "Samuel"])
player_ratings.update_ratings_2v2(["Antoine", "Samuel"], ["Gaetan", "Martin"])
player_ratings.update_ratings_2v2(["Gaetan", "Arthur"], ["Samuel", "Martin"])
player_ratings.update_ratings_2v2(["Arthur", "Martin"], ["Antoine", "Gaetan"])
player_ratings.update_ratings_2v2(["Antoine", "Arthur"], ["Gaetan", "Samuel"])
player_ratings.update_ratings_2v2(["Arthur", "Martin"], ["Samuel", "Antoine"])
player_ratings.update_ratings_2v2(["Antoine", "Gaetan"], ["Samuel", "Martin"])
player_ratings.update_ratings_2v2(["Gaetan", "Samuel"], ["Arthur", "Martin"])

# Session 9
player_ratings.update_ratings_2v2(["Adrien", "Martin"], ["Antoine", "Gaetan"])
player_ratings.update_ratings_2v2(["Adrien", "Antoine"], ["Martin", "Romain"])
player_ratings.update_ratings_2v2(["Gaetan", "Martin"], ["Adrien", "Romain"])
player_ratings.update_ratings_2v2(["Adrien", "Gaetan"], ["Antoine", "Romain"])
player_ratings.update_ratings_2v2(["Romain", "Gaetan"], ["Martin", "Antoine"])
player_ratings.update_ratings_2v2(["Adrien", "Antoine"], ["Martin", "Gaetan"])
player_ratings.update_ratings_2v2(["Adrien", "Martin"], ["Antoine", "Romain"])
player_ratings.update_ratings_2v2(["Adrien", "Gaetan"], ["Romain", "Martin"])
player_ratings.update_ratings_2v2(["Adrien", "Romain"], ["Antoine", "Gaetan"])
player_ratings.update_ratings_2v2(["Gaetan", "Martin"], ["Antoine", "Romain"])
player_ratings.update_ratings_2v2(["Adrien", "Gaetan"], ["Antoine", "Martin"])
player_ratings.update_ratings_2v2(["Romain", "Adrien"], ["Antoine", "Martin"])
player_ratings.update_ratings_2v2(["Adrien", "Martin"], ["Romain", "Gaetan"])
player_ratings.update_ratings_2v2(["Antoine", "Samuel"], ["Noémie", "Romain"])
player_ratings.update_ratings_2v2(["Antoine", "Noémie"], ["Romain", "Samuel"])
player_ratings.update_ratings_2v2(["Antoine", "Romain"], ["Samuel", "Noémie"])


# Display ratings
player_ratings.display_ratings()

# Close connection
player_ratings.__exit__()
