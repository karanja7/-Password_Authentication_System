"""
Password Strength Checker and Authentication System
Demonstrates: Authentication, Password Hashing, Input Validation, Access Control
"""

import hashlib


class PasswordSecurity:
    """Handles password hashing and strength validation"""
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256 (one-way encryption)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def check_strength(password):
        """
        Check if password is strong.
        Requirements: 8+ chars, uppercase, lowercase, numbers
        Returns: (is_strong, feedback_message)
        """
        issues = []
        
        if len(password) < 8:
            issues.append("✗ Must be at least 8 characters long")
        if not any(c.isupper() for c in password):
            issues.append("✗ Must contain uppercase letters (A-Z)")
        if not any(c.islower() for c in password):
            issues.append("✗ Must contain lowercase letters (a-z)")
        if not any(c.isdigit() for c in password):
            issues.append("✗ Must contain numbers (0-9)")
        
        if issues:
            return False, "Password is WEAK:\n" + "\n".join(issues)
        
        return True, "✓ Password is STRONG"


class User:
    """Stores user data with hashed password (no plain-text passwords!)"""
    
    def __init__(self, username, hashed_password):
        """Create a user with username and hashed password"""
        self.username = username
        self._hashed_password = hashed_password  # Private - never expose!
        self.account_locked = False
        self.failed_attempts = 0
    
    def check_password(self, password):
        """Check if provided password matches (using hash comparison)"""
        hashed = PasswordSecurity.hash_password(password)
        return hashed == self._hashed_password
    
    def add_failed_attempt(self):
        """Record a failed login attempt"""
        self.failed_attempts += 1
        if self.failed_attempts >= 3:
            self.account_locked = True
    
    def reset_failed_attempts(self):
        """Reset attempts on successful login"""
        self.failed_attempts = 0


class AuthenticationSystem:
    """Manages user registration, login, and authentication"""
    
    def __init__(self):
        """Initialize the authentication system"""
        self.users = {}  # Store registered users
        self.history = []  # Log all login attempts
    
    def register(self, username, password):
        """
        Register a new user with username and password.
        Returns: (success, message)
        """
        # Validate inputs
        if not username or not password:
            return False, "Error: Username and password required"
        
        # Check if user already exists
        if username in self.users:
            return False, f"Error: User '{username}' already exists"
        
        # Check password strength
        is_strong, feedback = PasswordSecurity.check_strength(password)
        if not is_strong:
            return False, feedback
        
        # Hash password and create user
        hashed = PasswordSecurity.hash_password(password)
        self.users[username] = User(username, hashed)
        
        self.history.append({'action': 'REGISTER', 'username': username, 'status': 'SUCCESS'})
        return True, f"✓ User '{username}' registered successfully!"
    
    def login(self, username, password):
        """
        Authenticate a user.
        Returns: (success, message)
        """
        # Validate inputs
        if not username or not password:
            return False, "Error: Username and password required"
        
        # Check if user exists
        if username not in self.users:
            self.history.append({'action': 'LOGIN', 'username': username, 'status': 'FAILED - User not found'})
            return False, f"Error: User '{username}' not found"
        
        user = self.users[username]
        
        # Check if account is locked
        if user.account_locked:
            self.history.append({'action': 'LOGIN', 'username': username, 'status': 'FAILED - Account locked'})
            return False, f"Error: Account '{username}' is locked (3 failed attempts)"
        
        # Check password
        if user.check_password(password):
            user.reset_failed_attempts()
            self.history.append({'action': 'LOGIN', 'username': username, 'status': 'SUCCESS'})
            return True, f"✓ Login successful! Welcome, {username}"
        else:
            user.add_failed_attempt()
            remaining = 3 - user.failed_attempts
            
            self.history.append({'action': 'LOGIN', 'username': username, 'status': 'FAILED - Wrong password'})
            
            if user.account_locked:
                return False, f"Error: Account locked after 3 failed attempts"
            
            return False, f"Error: Wrong password. Attempts remaining: {remaining}"
    
    def show_users(self):
        """Display all registered users"""
        if not self.users:
            print("No users registered yet.\n")
            return
        
        print("\n" + "="*50)
        print("Registered Users:")
        print("="*50)
        for username, user in self.users.items():
            status = "🔒 LOCKED" if user.account_locked else "✓ ACTIVE"
            print(f"  {username:20} | {status}")
        print("="*50 + "\n")
    
    def show_history(self):
        """Display login history"""
        if not self.history:
            print("No history yet.\n")
            return
        
        print("\n" + "="*50)
        print(f"Authentication History ({len(self.history)} events):")
        print("="*50)
        for i, entry in enumerate(self.history, 1):
            print(f"{i}. {entry['action']:10} | {entry['username']:15} | {entry['status']}")
        print("="*50 + "\n")


def main():
    """Simple menu-driven interface for the authentication system"""
    system = AuthenticationSystem()
    
    print("\n" + "="*60)
    print("PASSWORD STRENGTH CHECKER & AUTHENTICATION SYSTEM")
    print("="*60 + "\n")
    
    while True:
        print("\nMENU:")
        print("1. Register new user")
        print("2. Login")
        print("3. Check password strength")
        print("4. View registered users")
        print("5. View login history")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            print("\n--- REGISTER ---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            success, msg = system.register(username, password)
            print(f"\n{msg}\n")
        
        elif choice == "2":
            print("\n--- LOGIN ---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            success, msg = system.login(username, password)
            print(f"\n{msg}\n")
        
        elif choice == "3":
            print("\n--- PASSWORD STRENGTH CHECK ---")
            password = input("Password: ").strip()
            is_strong, feedback = PasswordSecurity.check_strength(password)
            print(f"\n{feedback}\n")
        
        elif choice == "4":
            system.show_users()
        
        elif choice == "5":
            system.show_history()
        
        elif choice == "6":
            print("\nThank you for using the system!\n")
            break
        
        else:
            print("\nInvalid choice. Please try again.\n")


if __name__ == "__main__":
    main()
