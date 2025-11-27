# Security Audit Playbook: Web Application Code Review

**Playbook ID:** SA-PB-005  
**Version:** 1.0  
**Last Updated:** 2025-11-10  
**Author:** Artem Khludov

## Overview

This is the methodology I used for auditing a web application's source code, specifically focusing on authentication and password storage. I found and fixed a critical plain text password storage vulnerability.

## My Approach

When I audit code, I start with authentication because it's usually the weakest point. Here's what I do:

1. **Code Review** - Manually go through authentication-related code
2. **Database Check** - Look at the actual database schema and data
3. **Test It** - Create test users to verify what's actually happening
4. **Fix It** - Implement proper security controls
5. **Document** - Write up what I found and how I fixed it

## Tools I Use

- **grep** - Search codebase for password-related code
- **Bandit** - Automated Python security scanner
- **SQL queries** - Direct database inspection
- **Git** - Review code history and changes

## What I Look For

**Red Flags:**
- Passwords inserted directly into database queries
- No hashing libraries imported (bcrypt, argon2, etc.)
- Password column is VARCHAR/TEXT (should be BINARY or store hash)
- Direct string comparison for password verification
- No salt generation

**Good Signs:**
- Password hashing before database insertion
- Hashing libraries imported and used
- Password verification using hash comparison
- Salt included in hash or stored separately

## Common Issues

1. **Plain text storage** - Most critical, easiest to find
2. **Weak hashing** - MD5, SHA1 (not secure)
3. **No salt** - Makes rainbow table attacks possible
4. **Weak passwords** - No complexity requirements
5. **Password in logs** - Information disclosure

## Fix Strategy

When I find plain text passwords:

1. **Implement bcrypt** - Industry standard, well-tested
2. **Force password reset** - Clean slate approach
3. **Add password policy** - Minimum length, complexity
4. **Test thoroughly** - Make sure everything works
5. **Document migration** - Clear steps for client

## Code Examples

**Before (Vulnerable):**
```python
def register_user(username, password):
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, password))  # Plain text!
```

**After (Secure):**
```python
import bcrypt

def register_user(username, password):
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
    cursor.execute(query, (username, hashed))
```

## Lessons Learned

- Always check password storage first - it's the most common issue
- Direct database inspection is the fastest way to confirm
- bcrypt is straightforward to implement
- Migration strategy is important - can't convert plain text to hash
- Force password reset is the cleanest approach

## References

- OWASP Password Storage Cheat Sheet
- NIST SP 800-63B Digital Identity Guidelines
- bcrypt documentation

**Used in Case-005 on 2025-11-10**
