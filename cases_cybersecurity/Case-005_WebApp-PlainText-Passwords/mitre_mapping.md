# MITRE ATT&CK Mapping - Case 005: Plain Text Password Storage

## Vulnerability Overview

```
Credential Storage  Authentication  Account Compromise
     T1552.001         T1078           T1110.003
```

## Detailed Technique Mapping

### TA0006: Credential Access

#### T1552.001 - Unsecured Credentials: Credentials in Files

**Sub-technique:** T1552.001 - Credentials in Files

**Vulnerability:**
- Passwords stored in database in plain text format
- No encryption or hashing applied to stored credentials
- Database accessible to multiple system components
- Backup files contain plain text passwords

**Evidence:**
```sql
-- Database query showing plain text passwords
SELECT id, username, password FROM users;

+----+----------+------------------+
| id | username | password         |
+----+----------+------------------+
|  1 | admin    | Admin123!        |  -- Plain text
|  2 | john     | MyPassword2024   |  -- Plain text
+----+----------+------------------+
```

**Code Evidence:**
```python
# Vulnerable code storing plain text
def register_user(username, password):
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, password))  # Plain text stored
```

**Impact:**
- **Confidentiality:** HIGH - All passwords immediately readable
- **Attack Vector:** Database compromise, SQL injection, backup theft
- **Affected Users:** All registered users (1,000+ accounts)

**Detection:**
- Code review: Search for password storage without hashing
- Database inspection: Check password column data type and content
- Static analysis: Automated tools (Bandit, ESLint security)

**Prevention:**
- Implement password hashing (bcrypt, argon2, scrypt)
- Never store passwords in plain text
- Use parameterized queries to prevent SQL injection
- Encrypt database backups
- Implement access controls for database

---

### TA0001: Initial Access

#### T1078 - Valid Accounts

**Sub-technique:** T1078.004 - Cloud Accounts

**How Vulnerability Enables Attack:**
- Plain text passwords enable credential theft
- Stolen credentials can be used for account takeover
- No additional authentication factors required
- Weak password storage makes attacks easier

**Attack Scenario:**
1. Attacker compromises database (SQL injection, backup theft, insider)
2. Extracts all plain text passwords
3. Uses credentials for account takeover
4. Accesses user accounts and sensitive data

**Evidence:**
```python
# Vulnerable authentication allows easy credential verification
def authenticate_user(username, password):
    query = "SELECT password FROM users WHERE username = %s"
    result = cursor.fetchone()
    if result[0] == password:  # Direct comparison confirms plain text
        return True
```

**Detection:**
- Monitor for unusual login patterns
- Alert on multiple failed login attempts
- Track account access from new locations
- Monitor database access patterns

**Prevention:**
- Hash passwords with bcrypt/argon2
- Implement multi-factor authentication (MFA)
- Use account lockout mechanisms
- Monitor and alert on suspicious authentication attempts

---

### TA0006: Credential Access

#### T1110.003 - Brute Force: Password Spraying

**How Vulnerability Enables Attack:**
- Plain text passwords make credential verification trivial
- No computational cost for password checking
- Enables rapid password spraying attacks
- Weak passwords easily identified in database

**Attack Scenario:**
1. Attacker gains database access
2. Extracts all plain text passwords
3. Identifies common/weak passwords
4. Uses credentials across multiple platforms (credential stuffing)

**Evidence:**
```sql
-- Common passwords easily identifiable
SELECT username, password FROM users 
WHERE password IN ('password', '123456', 'admin', 'Password123');

-- Results show multiple users with weak passwords
```

**Impact:**
- Rapid credential compromise
- Account takeover at scale
- Credential stuffing attacks enabled
- No protection against offline attacks

**Detection:**
- Monitor for database access anomalies
- Alert on bulk password queries
- Track failed authentication attempts
- Monitor for credential stuffing patterns

**Prevention:**
- Hash passwords (prevents offline attacks)
- Implement password complexity requirements
- Use account lockout after failed attempts
- Monitor and block credential stuffing attempts

---

## Detection Coverage Matrix

| Technique | Coverage | Tool | Status |
|-----------|----------|------|--------|
| T1552.001 | **Full** | Code Review, Database Inspection | **Vulnerability Found** |
| T1078 | **Partial** | Authentication Monitoring | **Risk Identified** |
| T1110.003 | **Partial** | Brute Force Detection | **Risk Identified** |

---

## Defensive Recommendations

### Per Technique:

**T1552.001 (Unsecured Credentials):**
- ✅ **Implement password hashing** - Use bcrypt with cost factor 12+
- ✅ **Remove plain text storage** - Migrate all passwords to hashed format
- ✅ **Encrypt database backups** - Prevent credential exposure in backups
- ✅ **Implement access controls** - Limit database access to authorized personnel
- ✅ **Regular security audits** - Identify and fix credential storage issues

**T1078 (Valid Accounts):**
- ✅ **Multi-factor authentication** - Add MFA to prevent account takeover
- ✅ **Account lockout mechanisms** - Prevent brute force attacks
- ✅ **Password strength requirements** - Enforce strong passwords
- ✅ **Session management** - Implement secure session handling
- ✅ **Monitoring and alerting** - Detect suspicious account activity

**T1110.003 (Password Spraying):**
- ✅ **Password hashing** - Prevent offline password attacks
- ✅ **Rate limiting** - Limit authentication attempts
- ✅ **Account lockout** - Lock accounts after failed attempts
- ✅ **Password complexity** - Require strong, unique passwords
- ✅ **Credential monitoring** - Detect and block credential stuffing

---

## Attack Chain Visualization

```
Initial Access          Credential Access        Impact
     ↓                        ↓                    ↓
Database Compromise  →  Extract Plain Text  →  Account Takeover
  (SQL Injection)         Passwords              (Data Theft)
     ↓                        ↓                    ↓
Backup Theft         →  Identify Weak      →  Credential Stuffing
  (Physical/Cloud)        Passwords              (Other Platforms)
     ↓                        ↓                    ↓
Insider Threat       →  Use Credentials     →  Lateral Movement
  (Admin Access)         for Access              (Network Compromise)
```

---

## Remediation Mapping

### Before (Vulnerable)

```python
# T1552.001 - Credentials stored insecurely
def register_user(username, password):
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, password))  # Plain text
```

**MITRE Techniques Enabled:**
- T1552.001 - Unsecured Credentials
- T1078 - Valid Accounts (via credential theft)
- T1110.003 - Password Spraying (enabled by plain text)

### After (Secure)

```python
# T1552.001 - Credentials properly secured
import bcrypt

def register_user(username, password):
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
    cursor.execute(query, (username, hashed))  # Hashed
```

**MITRE Techniques Mitigated:**
- ✅ T1552.001 - Credentials now securely hashed
- ✅ T1078 - Account takeover prevented (passwords not readable)
- ✅ T1110.003 - Password spraying prevented (offline attacks blocked)

---

## MITRE Navigator Layer

```json
{
  "name": "Case-005_PlainText_Passwords",
  "versions": {
    "attack": "14",
    "navigator": "4.9.1"
  },
  "techniques": [
    {
      "techniqueID": "T1552.001",
      "color": "#ff6666",
      "comment": "CRITICAL: Passwords stored in plain text",
      "score": 9
    },
    {
      "techniqueID": "T1078",
      "color": "#ffaa00",
      "comment": "HIGH: Account takeover enabled by credential theft",
      "score": 7
    },
    {
      "techniqueID": "T1110.003",
      "color": "#ffaa00",
      "comment": "HIGH: Password spraying enabled by plain text storage",
      "score": 7
    }
  ]
}
```

---

## Detection Signals

### Code-Level Indicators

**Vulnerable Patterns:**
- Direct password insertion into database queries
- No hashing libraries imported (bcrypt, argon2, scrypt)
- Password column is VARCHAR/TEXT type
- Password comparison using `==` operator
- No salt generation or storage

**Secure Patterns:**
- Password hashing before database insertion
- Hashing libraries imported and used
- Password column is BINARY or stores hash
- Password verification using hash comparison functions
- Salt generation and storage

### Database Indicators

**Vulnerable:**
- Password column contains readable text
- Password length matches typical user passwords (8-20 chars)
- No salt column present
- Password field allows NULL values

**Secure:**
- Password column contains hash strings (60+ chars for bcrypt)
- Hash format matches hashing algorithm (e.g., `$2b$` for bcrypt)
- Salt column present or salt included in hash
- Password field properly constrained

### Application Indicators

**Vulnerable:**
- Passwords visible in application logs
- Password in error messages
- Password returned in API responses
- No password strength validation

**Secure:**
- Passwords never logged
- Generic error messages (no password hints)
- Password never returned in responses
- Password strength validation enforced

---

## Response Actions by Technique

### T1552.001 (Unsecured Credentials)

1. **Immediate:**
   - Implement password hashing (bcrypt recommended)
   - Update all password storage functions
   - Add password_hash column to database

2. **Short-term:**
   - Force password reset for all users
   - Remove plain text password column
   - Encrypt database backups

3. **Long-term:**
   - Regular security audits
   - Automated security scanning
   - Security code review process

### T1078 (Valid Accounts)

1. **Immediate:**
   - Implement MFA for sensitive accounts
   - Add account lockout mechanisms
   - Monitor authentication attempts

2. **Short-term:**
   - Password strength requirements
   - Session management improvements
   - Security event logging

3. **Long-term:**
   - Zero Trust architecture
   - Privileged Access Management (PAM)
   - Continuous security monitoring

### T1110.003 (Password Spraying)

1. **Immediate:**
   - Rate limiting on authentication endpoints
   - Account lockout after failed attempts
   - Password complexity enforcement

2. **Short-term:**
   - Credential stuffing detection
   - IP reputation checking
   - Behavioral analysis

3. **Long-term:**
   - Advanced threat detection
   - Machine learning for anomaly detection
   - Threat intelligence integration

---

## References

- [MITRE ATT&CK - T1552.001](https://attack.mitre.org/techniques/T1552/001/)
- [MITRE ATT&CK - T1078](https://attack.mitre.org/techniques/T1078/)
- [MITRE ATT&CK - T1110.003](https://attack.mitre.org/techniques/T1110/003/)
- [OWASP Top 10 - A07:2021](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
- [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html)

_Mapped by: Artem Khludov, Security Auditor_  
_Date: 2025-11-10_

