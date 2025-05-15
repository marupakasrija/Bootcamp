# 09_game_state.py
import pickle
import os
import time # For simple timestamp in metadata

class GameState:
    def __init__(self, level=1, score=0, inventory=None, player_position=(0, 0)):
        self.level = level
        self.score = score
        self.inventory = inventory if inventory is not None else []
        self.player_position = player_position
        self.is_game_over = False # Example of another state variable
        self._save_timestamp = None # To track when it was last saved

    def update_state(self, level_change=0, score_change=0, new_item=None, new_position=None):
        self.level += level_change
        self.score += score_change
        if new_item:
            self.inventory.append(new_item)
        if new_position:
            self.player_position = new_position

    def game_over(self):
        self.is_game_over = True

    def __str__(self):
        timestamp_str = time.ctime(self._save_timestamp) if self._save_timestamp else "Never Saved"
        return (f"Game State:\n"
                f"  Level: {self.level}\n"
                f"  Score: {self.score}\n"
                f"  Inventory: {self.inventory}\n"
                f"  Player Position: {self.player_position}\n"
                f"  Game Over: {self.is_game_over}\n"
                f"  Last Saved: {timestamp_str}")

    def __repr__(self):
        return str(self)

class Game:
    def __init__(self, save_file="game_save.pkl"):
        self.save_file = save_file
        self.state = GameState() # Initial state
        self._load_game() # Attempt to load state on startup

    def _load_game(self):
        """Loads the game state from the save file if it exists."""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'rb') as f:
                    self.state = pickle.load(f)
                print(f"Game state loaded successfully from {self.save_file}")
                # Basic validation could be added here, e.g., check type
                if not isinstance(self.state, GameState):
                    print("Warning: Loaded object is not a GameState instance. Starting new game.")
                    self.state = GameState()

            except Exception as e:
                print(f"Error loading game state from {self.save_file}: {e}")
                print("Starting a new game.")
                self.state = GameState() # Start a new game on load failure
        else:
            print(f"No save file found at {self.save_file}. Starting a new game.")
            self.state = GameState() # Start a new game if no file exists

    def save_game(self):
        """Saves the current game state to the save file."""
        try:
            self.state._save_timestamp = time.time() # Update timestamp before saving
            with open(self.save_file, 'wb') as f:
                pickle.dump(self.state, f)
            print(f"Game state saved successfully to {self.save_file}")
        except Exception as e:
            print(f"Error saving game state to {self.save_file}: {e}")

    def play_a_turn(self):
        """Simulates playing a turn and updating state."""
        if self.state.is_game_over:
            print("Game is over. Cannot play.")
            return

        print("\nPlaying a turn...")
        # Simulate some state changes
        self.state.update_state(level_change=0, score_change=10, new_item=f"Item_{len(self.state.inventory) + 1}", new_position=(self.state.player_position[0] + 1, self.state.player_position[1]))
        print(f"Current state:\n{self.state}")

        # Simulate ending the game
        if self.state.score >= 30: # Lower score for quicker game end
            self.state.game_over()
            print("Game Over!")

# --- Simulation ---

# Create a new game instance (this will attempt to load a save)
print("--- Initial Game Start ---")
my_game = Game("my_adventure_save.pkl")
print(f"Initial state:\n{my_game.state}")

# Play a few turns
my_game.play_a_turn()
my_game.play_a_turn()

# Save the game
my_game.save_game()

# --- Simulate closing and restarting the game ---
print("\n--- Simulating game restart ---")

# Create a new game instance (this should load the saved state)
restarted_game = Game("my_adventure_save.pkl")
print(f"State after first restart:\n{restarted_game.state}")

# Continue playing from the loaded state
restarted_game.play_a_turn() # This turn might end the game based on score logic

# Save the game again
restarted_game.save_game()

# --- Simulate another restart to see the latest save ---
print("\n--- Simulating second game restart ---")
final_game = Game("my_adventure_save.pkl")
print(f"Final state after second restart:\n{final_game.state}")

# Clean up the save file (optional)
# import os
# os.remove("my_adventure_save.pkl")
# print("\nRemoved game save file.")