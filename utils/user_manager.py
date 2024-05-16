import os

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def load_users(self):
        if not os.path.exists("data"):
            os.makedirs("data")   
        try:
            with open("data/users.txt", "r") as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def save_users(self):
        with open("data/users.txt", "w") as file:
            for username, password in self.users.items():
                file.write(f"{username},{password}\n")

    def validate_username(self, username):
        if len(username) >= 4 and username not in self.users:
            return True
        return False

    def validate_password(self, password):
        if len(password) >= 8:
            return True
        return False

    def register(self, username, password):
        self.users[username] = password
        self.save_users()

    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            return True
        return False