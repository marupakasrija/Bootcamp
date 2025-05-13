import pickle
import os # To check if the save file exists

class GameState:
    def __init__(self, level=1, score=0, inventory=None, player_pos=(0, 0)):
        self.level = level
        self.score = score
        self.inventory = inventory if inventory is not None else []
        self.player_pos = player_pos
        self.enemies = [] # List of enemy positions, e.g., [(x, y), ...]

    def add_score(self, points):
        self.score += points

    def add_item_to_inventory(self, item):
        self.inventory.append(item)

    def move_player(self, dx, dy):
        self.player_pos = (self.player_pos[0] + dx, self.player_pos[1] + dy)

    def add_enemy(self, pos):
        self.enemies.append(pos)

    def save_state(self, filename="game_save.pkl"):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self, f)
            print(f"Game state saved to {filename}")
        except Exception as e:
            print(f"Error saving game state: {e}")

    @classmethod
    def load_state(cls, filename="game_save.pkl"):
        if not os.path.exists(filename):
            print(f"No save file found at {filename}. Starting a new game.")
            return cls() # Return a new default game state

        try:
            with open(filename, 'rb') as f:
                state = pickle.load(f)
            print(f"Game state loaded from {filename}")
            return state
        except Exception as e:
            print(f"Error loading game state: {e}. Starting a new game.")
            return cls() # Return a new default game state

    def __str__(self):
        return (f"--- Game State ---\n"
                f"Level: {self.level}\n"
                f"Score: {self.score}\n"
                f"Inventory: {self.inventory}\n"
                f"Player Position: {self.player_pos}\n"
                f"Enemies: {self.enemies}\n"
                f"------------------")

# --- Simulation ---

# Option 1: Start a new game
print("Attempting to load game state...")
game = GameState.load_state()
print(game)

# Play the game a bit
if game.score == 0: # Only do this if it's a new game
    print("Starting a new game...")
    game.add_score(100)
    game.add_item_to_inventory("Sword")
    game.move_player(5, 3)
    game.level = 2
    game.add_enemy((10, 10))
    game.add_enemy((12, 8))
    print("\nGame progress made:")
    print(game)

    # Save the game state
    game.save_state()

# Option 2: Load the saved game (run the script again)
print("\nAttempting to load game state again...")
game_loaded = GameState.load_state()
print(game_loaded)

# Clean up the save file (optional)
# if os.path.exists("game_save.pkl"):
#     os.remove("game_save.pkl")
#     print("\nRemoved game_save.pkl")