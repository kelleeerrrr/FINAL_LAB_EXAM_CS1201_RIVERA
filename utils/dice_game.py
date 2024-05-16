import os
from random import randint
from datetime import datetime
from utils.user_manager import UserManager

class DiceGame:
    def __init__(self, user_manager):
        self.user_manager = (user_manager)
        self.top_scores = []
        self.current_user = None
        self.load_top_scores()
        
    def load_top_scores(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists("data/rankings.txt"):
            with open("data/rankings.txt", "w"):
                pass  
        else:
            with open("data/rankings.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(',')
                    username = parts[0]
                    total_points = int(parts[1])
                    stages_won = int(parts[2])
                    date_time = datetime.fromisoformat(parts[3])
                    self.top_scores.append((username, total_points, stages_won, date_time))
    def main_menu(self):
        print("\nWelcome to the Dice Game!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

    def register(self):
        username = input("Enter username (at least 4 characters): ")
        password = input("Enter password (at least 8 characters): ")
        if self.user_manager.validate_username(username) and self.user_manager.validate_password(password):
            self.user_manager.register(username, password)
            print("\nRegistration successful.")
        else:
            print("Invalid username or password.")

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if self.user_manager.login(username, password):
            print("\nLogin successful. Welcome back,", username + "!")
            self.current_user = username
            self.game_menu()
        else:
            print("Invalid username or password.")

    def game_menu(self):
        print("\n--- Game Menu ---")
        print("1. Start Game")
        print("2. Top Scores")
        print("3. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            self.start_game()
        elif choice == "2":
            self.display_top_scores()
        elif choice == "3":
            print("Logging out. Goodbye, " + self.current_user + "!")
            self.current_user = None
        else:
            print("Invalid choice. Please try again.")
            self.game_menu()

    def roll_dice(self):
        return randint(1, 6)

    def update_top_scores(self, username, total_points, stages_won):
        now = datetime.now()
        self.top_scores.append((username, total_points, stages_won, now))
        self.top_scores.sort(key=lambda x: (-x[1], x[2], x[3])) 
        if len(self.top_scores) > 10:
            self.top_scores.pop()

    def display_top_scores(self):
        if not self.top_scores:
            print("No scores yet.")
        else:
            print("--- Top 10 Scores ---")
            print("Username | Total Points | Stages Won | Date & Time")
            for i, score in enumerate(self.top_scores, start=1):
                print(f"{i}. {score[0]} | {score[1]} | {score[2]} | {score[3]}")

        input("Press Enter to continue to the game menu...")
        self.game_menu()

    def start_game(self):
        print("\n--- Game Started ---")
        total_points = 0
        stages_won = 0
        continue_game = True

        while continue_game:
            print(f"\n--- Stage {stages_won + 1} ---")
            stage_wins = 0

            for _ in range(3):
                print("\n--- Round", _ + 1, "---")
                user_roll = self.roll_dice()
                computer_roll = self.roll_dice()

                print("You rolled:", user_roll)
                print("CPU rolled:", computer_roll)

                if user_roll >= computer_roll:
                    print("You win this round!")
                    total_points += 1
                    stage_wins += 1
                else:
                    print("You lose this round!")

            if stage_wins >= 2:
                print("Congratulations! You won this stage!")
                stages_won += 1
            else:
                print("Sorry, you lost this stage.")
                continue_game = False  

            print("Total points:", total_points)
            print("Stages won:", stages_won)

            if not continue_game:
                print("Game over.")
                self.update_top_scores(self.current_user, total_points, stages_won)
                self.game_menu() 
            else:
                proceed_next_stage = input("Do you want to continue to the next stage? (1 for Yes, 0 for No): ")
                if proceed_next_stage == "0":
                    print("Game over.")
                    self.update_top_scores(self.current_user, total_points, stages_won)
                    self.game_menu() 
