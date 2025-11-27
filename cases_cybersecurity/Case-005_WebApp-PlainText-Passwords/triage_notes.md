# Case 005: Web Application Code Audit - Plain Text Password Storage

**Date:** November 10, 2025  
**Analyst:** Artem Khludov  
**Company:** EnergyLogic AI (Client: Upwork Project)  
**Severity:** CRITICAL  
**Status:** Resolved

## Executive Summary

I was doing a security audit for a client on Upwork. They wanted me to review their web application's source code. I found a critical issue right away - all user passwords were stored in the database as plain text, no hashing at all. I fixed it by implementing bcrypt for password hashing, wrote a migration script, and gave them recommendations on how to handle this going forward.

## Timeline

| Date | Event | Status |
|------|-------|--------|
| Nov 8, 2025 | Client asked for security audit | Started |
| Nov 8, 2025 | Got access to repo, cloned it | Setup |
| Nov 9, 2025 | Started reviewing code, checked authentication | Review |
| Nov 9, 2025 | Found plain text passwords in database | **Found issue** |
| Nov 9, 2025 | Tested it to confirm | Confirmed |
| Nov 10, 2025 | Planned the fix with bcrypt | Planning |
| Nov 10, 2025 | Updated registration and login code | Fixed |
| Nov 10, 2025 | Created migration script | Done |
| Nov 10, 2025 | Sent report and code changes to client | Delivered |

## How I Found It

I focused on checking how authentication and password storage worked. Started by manually going through the code, searching for where passwords get saved to the database. Then I checked the users table structure and actually looked at what was stored there. Created a test user and confirmed the password was saved in plain text. Used grep to search the codebase, Bandit for automated scanning, and direct SQL queries to check the database.

## What I Found

### 1. Plain Text Password Storage

**Location:** `src/auth/user_service.py` - registration function

**The Problem:**
```python
def register_user(username, email, password):
    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, email, password))  # Storing plain text!
    db.commit()
```

The password was being inserted directly into the database without any hashing.

**Database Proof:**
```sql
SELECT id, username, password FROM users LIMIT 5;

+----+----------+------------------+
| id | username | password         |
+----+----------+------------------+
|  1 | admin    | Admin123!        |
|  2 | john     | MyPassword2024   |
|  3 | jane     | Jane@2024        |
+----+----------+------------------+
```

You could literally read everyone's passwords from the database.

### 2. Authentication Logic

**Location:** `src/auth/auth_service.py` - login function

```python
def authenticate_user(username, password):
    query = "SELECT id, username, password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    
    if result and result[2] == password:  # Direct string comparison
        return {"authenticated": True, "user_id": result[0]}
    return {"authenticated": False}
```

The code was doing direct string comparison, which confirmed passwords were stored in plain text.

## Proof of Concept

I tested it to make sure:

1. Registered a test user with password "TestPassword123!"
2. Checked the database directly - saw the password in plain text
3. Logged in with the same password - it worked

This confirmed the vulnerability. If someone got database access, they'd have all passwords immediately.

## Impact

This was critical. If the database got compromised (SQL injection, backup theft, insider access), all user passwords would be exposed instantly. That's about 1,000+ user accounts. Also violates GDPR, PCI-DSS if they handle payments, and OWASP Top 10 guidelines.

## What I Fixed

### 1. Password Hashing

I replaced the registration function to use bcrypt:

```python
import bcrypt

def register_user(username, email, password):
    # Hash password before storing
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, email, hashed_password))
    db.commit()
```

### 2. Updated Authentication

Changed the login function to verify against the hash:

```python
def authenticate_user(username, password):
    query = "SELECT id, username, password_hash FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    
    if result:
        stored_hash = result[2]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return {"authenticated": True, "user_id": result[0]}
    return {"authenticated": False}
```

### 3. Database Migration

Added a migration script to handle existing users:

```sql
-- Add new column for hashed passwords
ALTER TABLE users ADD COLUMN password_hash VARCHAR(60) AFTER password;

-- Mark all users as needing password reset
ALTER TABLE users ADD COLUMN password_reset_required BOOLEAN DEFAULT TRUE;
```

### 4. Password Policy

Added password strength validation - minimum 12 characters, uppercase, lowercase, digit, special character.

## Migration Plan

I recommended forcing all users to reset their passwords. This way we get a clean slate - all new passwords are properly hashed from the start. No risk of trying to convert existing plain text passwords (which you can't do anyway since you can't reverse a hash).

The plan:
1. Add password_hash column to database
2. Send password reset emails to all users
3. When users reset, hash the new password with bcrypt
4. After 30 days, remove the old password column

## Testing

I wrote tests to make sure everything worked:
- Passwords are hashed, not stored in plain text
- Login works with correct password
- Login fails with wrong password
- Hash format is correct (bcrypt)

All tests passed.

## Why This Happened

The developer probably just didn't know about password hashing best practices. No security code review process, no security requirements documented. They built the feature quickly without thinking about security.

## What I Learned

Plain text password storage is still way too common. Many developers don't realize this is a problem. Code reviews should always check for security issues like this. Automated tools like Bandit can catch this early.

The fix was straightforward - bcrypt is well-documented and easy to implement. The tricky part was the migration strategy for existing users.

## Recommendations I Gave

**Immediate:**
- Force password reset for all users (done)
- Implement bcrypt hashing (done)
- Remove plain text column after migration (scheduled)

**Short-term:**
- Add security code review process
- Use automated security scanning in CI/CD
- Security training for developers

**Long-term:**
- Regular security audits
- Add MFA
- Implement account lockout mechanisms

## MITRE ATT&CK Mapping

- **T1552.001:** Unsecured Credentials - Passwords stored in database
- **T1078:** Valid Accounts - Weak storage enables account takeover
- **T1110.003:** Password Spraying - Plain text makes attacks easier

## Results

- Fixed the vulnerability - all passwords now hashed
- Migration process in place
- Tests written and passing
- Client has clear path forward

**Status:** Fixed and delivered to client. Migration in progress.

_Last updated: 2025-11-10_
