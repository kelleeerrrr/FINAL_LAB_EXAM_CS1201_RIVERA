import os
from utils.dice_game import DiceGame
from utils.user_manager import UserManager

def main():
    user_manager = UserManager ()
    dice_game = DiceGame(user_manager)
    while True:
        dice_game.main_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            dice_game.register()
        elif choice == "2":
            dice_game.login()
        elif choice == "3":
            print("Exiting the game. Goodbye!")
        else:
            print("Invalid choice. Please try again.")
            

if __name__ == "__main__":
    main()