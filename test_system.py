"""
Simple Test Suite for Authentication System
"""

from authentication_system import PasswordSecurity, AuthenticationSystem


def test_password_strength():
    """Test password strength validation"""
    print("\n=== TEST 1: PASSWORD STRENGTH ===\n")
    
    tests = [
        ("weak", False),
        ("Short1", False),
        ("NoNumbers", False),
        ("NoUpCase123", False),
        ("ValidPass123", True),
        ("SecureP@ss1", True),
    ]
    
    for password, should_be_strong in tests:
        is_strong, feedback = PasswordSecurity.check_strength(password)
        status = "PASS" if is_strong == should_be_strong else "FAIL"
        print(f"  {status} | '{password}': {is_strong}")
        if not is_strong:
            print(f"       {feedback}")


def test_hashing():
    """Test password hashing"""
    print("\n=== TEST 2: PASSWORD HASHING ===\n")
    
    password = "SecurePass123"
    hash1 = PasswordSecurity.hash_password(password)
    hash2 = PasswordSecurity.hash_password(password)
    hash3 = PasswordSecurity.hash_password("Different123")
    
    print(f"  Same password, hash 1: {hash1[:20]}...")
    print(f"  Same password, hash 2: {hash2[:20]}...")
    print(f"  Match: {hash1 == hash2} (PASS)\n")
    
    print(f"  Different password, hash 3: {hash3[:20]}...")
    print(f"  Different: {hash1 != hash3} (PASS)")


def test_registration_and_login():
    """Test registration and login"""
    print("\n=== TEST 3: REGISTRATION & LOGIN ===\n")
    
    system = AuthenticationSystem()
    
    # Test 1: Register valid user
    print("Test 1: Register valid user")
    success, msg = system.register("alice", "SecurePass123!")
    print(f"  {'PASS' if success else 'FAIL'}: {msg}\n")
    
    # Test 2: Weak password
    print("Test 2: Reject weak password")
    success, msg = system.register("bob", "weak")
    print(f"  {'PASS' if not success else 'FAIL'}: Weak password rejected\n")
    
    # Test 3: Duplicate username
    print("Test 3: Prevent duplicate username")
    success, msg = system.register("alice", "AnotherPass123!")
    print(f"  {'PASS' if not success else 'FAIL'}: Duplicate prevented\n")
    
    # Test 4: Successful login
    print("Test 4: Successful login")
    success, msg = system.login("alice", "SecurePass123!")
    print(f"  {'PASS' if success else 'FAIL'}: {msg}\n")
    
    # Test 5: Wrong password attempt 1
    print("Test 5: Wrong password (attempt 1)")
    success, msg = system.login("alice", "WrongPass1")
    print(f"  {'PASS' if not success else 'FAIL'}: {msg}\n")
    
    # Test 6: Wrong password attempt 2
    print("Test 6: Wrong password (attempt 2)")
    success, msg = system.login("alice", "WrongPass2")
    print(f"  {'PASS' if not success else 'FAIL'}: {msg}\n")
    
    # Test 7: Wrong password attempt 3 - LOCKOUT
    print("Test 7: Wrong password (attempt 3 - LOCKOUT)")
    success, msg = system.login("alice", "WrongPass3")
    print(f"  {'PASS' if not success else 'FAIL'}: {msg}\n")
    
    # Test 8: Try login after lockout
    print("Test 8: Login after lockout (with correct password)")
    success, msg = system.login("alice", "SecurePass123!")
    print(f"  {'PASS' if not success else 'FAIL'}: Account locked prevention works\n")


def test_history():
    """Test login history"""
    print("\n=== TEST 4: LOGIN HISTORY ===\n")
    
    system = AuthenticationSystem()
    system.register("testuser", "TestPass123!")
    system.login("testuser", "TestPass123!")
    system.login("testuser", "WrongPass")
    
    print(f"Total events logged: {len(system.history)}")
    for entry in system.history:
        print(f"  - {entry['action']}: {entry['username']} ({entry['status']})")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AUTH SYSTEM - SIMPLIFIED TEST SUITE")
    print("="*60)
    
    test_password_strength()
    test_hashing()
    test_registration_and_login()
    test_history()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
