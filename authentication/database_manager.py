import json
import os
import hashlib
import secrets

class DatabaseManager:
    def __init__(self, db_file="players_db.json"):
        self.db_file = db_file
        self._load_db()

    def _load_db(self):
        """Loads the JSON database. If the file doesn't exist, initializes an empty one."""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r") as f:
                    self.users = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.users = {}
        else:
            self.users = {}
            self._save_db()

    def _save_db(self):
        """Saves the current dictionary to the JSON file."""
        try:
            with open(self.db_file, "w") as f:
                json.dump(self.users, f, indent=4)
        except IOError as e:
            print(f"Error saving to database: {e}")

    def _hash_password(self, password, salt=None):
        """Hashes a password with a salt using PBKDF2."""
        if salt is None:
            salt = secrets.token_hex(16)
        
        hash_name = 'sha256'
        iterations = 100000
        key = hashlib.pbkdf2_hmac(
            hash_name, 
            password.encode('utf-8'), 
            salt.encode('utf-8'), 
            iterations
        )
        return salt, key.hex()

    def register(self, username, password):
        """Adds a new user with a hashed password if they don't already exist."""
        if username in self.users:
            return False, "User already exists!"
        
        salt, hashed_pw = self._hash_password(password)
        
        # Initialize with default Level 1 values
        self.users[username] = {
            "salt": salt,
            "password": hashed_pw
        }
        self._save_db()
        return True, "Registered successfully!"

    def authenticate(self, username, password):
        """
        Compares provided credentials against the stored salt and hash.
        Returns True if username exists and password matches, False otherwise.
        """
        user_data = self.users.get(username)
        if not user_data:
            return False
            
        stored_salt = user_data.get("salt")
        stored_hash = user_data.get("password")
        
        if not stored_salt or not stored_hash:
            return False

        _, provided_hash = self._hash_password(password, stored_salt)
        return secrets.compare_digest(stored_hash, provided_hash)