# 🎯 Example APIs for Genesis Auditor Testing

## 🔴 Intentionally Vulnerable APIs (Recommended for Testing)

### 1. OWASP Juice Shop (BEST OPTION)
**Setup:**
```bash
docker run -d -p 3000:3000 bkimminich/juice-shop
```

**Test in Genesis Auditor:**
- Domain: **API Security** or **OWASP Top 10**
- Name: `OWASP Juice Shop API`
- URL: `http://localhost:3000/rest`

**Known Vulnerabilities:**
- SQL Injection in search
- Broken authentication
- IDOR on user profiles
- XSS vulnerabilities
- Missing rate limiting

**Example Endpoints:**
```
GET  http://localhost:3000/rest/products/search?q=test
POST http://localhost:3000/rest/user/login
GET  http://localhost:3000/api/Users
GET  http://localhost:3000/api/BasketItems
```

---

### 2. DVWA (Damn Vulnerable Web App)
**Setup:**
```bash
docker run -d -p 80:80 vulnerables/web-dvwa
```

**Test in Genesis Auditor:**
- Domain: **API Security**
- Name: `DVWA API`
- URL: `http://localhost/dvwa`

---

### 3. WebGoat
**Setup:**
```bash
docker run -d -p 8080:8080 webgoat/webgoat
```

**Test in Genesis Auditor:**
- Domain: **API Security**
- Name: `WebGoat API`
- URL: `http://localhost:8080/WebGoat`

---

## 🟢 Public Safe APIs (Production APIs - Test Responsibly)

### 4. JSONPlaceholder (No Auth Required)
**Test in Genesis Auditor:**
- Domain: **API Security**
- Name: `JSONPlaceholder Test API`
- URL: `https://jsonplaceholder.typicode.com`

**Endpoints:**
```
GET  https://jsonplaceholder.typicode.com/posts
GET  https://jsonplaceholder.typicode.com/users
POST https://jsonplaceholder.typicode.com/posts
```

**Expected Results:**
- Should show good security practices
- No SQL injection vulnerabilities
- Proper error handling

---

### 5. ReqRes Mock API
**Test in Genesis Auditor:**
- Domain: **API Security**
- Name: `ReqRes Mock API`
- URL: `https://reqres.in/api`

**Endpoints:**
```
GET  https://reqres.in/api/users
POST https://reqres.in/api/login
POST https://reqres.in/api/register
```

---

### 6. HTTPBin (Request Testing Service)
**Test in Genesis Auditor:**
- Domain: **API Security**
- Name: `HTTPBin Test Service`
- URL: `https://httpbin.org`

**Endpoints:**
```
GET  https://httpbin.org/get
POST https://httpbin.org/post
GET  https://httpbin.org/status/500
GET  https://httpbin.org/delay/3
```

---

## 🏥 Healthcare APIs (HIPAA Domain)

### 7. FHIR Test Server
**Test in Genesis Auditor:**
- Domain: **HIPAA Compliance**
- Name: `FHIR Test Server`
- URL: `https://hapi.fhir.org/baseR4`

**Endpoints:**
```
GET https://hapi.fhir.org/baseR4/Patient
GET https://hapi.fhir.org/baseR4/Observation
GET https://hapi.fhir.org/baseR4/Medication
```

---

## 💰 Financial APIs (Financial Fraud Domain)

### 8. ExchangeRate API
**Test in Genesis Auditor:**
- Domain: **Financial Fraud**
- Name: `Exchange Rate API`
- URL: `https://api.exchangerate-api.com/v4/latest/USD`

---

## 🚀 Quick Start Testing Guide

### Option 1: Use OWASP Juice Shop (Best for Demo)

1. **Start Juice Shop:**
   ```bash
   docker run -d -p 3000:3000 bkimminich/juice-shop
   ```

2. **Wait 30 seconds for startup**

3. **Open Genesis Auditor:** http://localhost:3001

4. **Create New Audit:**
   - Click "New Audit"
   - Select domain: **API Security**
   - Name: `OWASP Juice Shop Security Audit`
   - URL: `http://localhost:3000/rest`
   - Click "Start Audit"

5. **Watch Real-Time Results:**
   - Progress bar will show phases
   - Should find 8-15 vulnerabilities
   - Download PDF report when complete

**Expected Results:**
- Compliance Score: 20-40/100 (intentionally vulnerable)
- Vulnerabilities: 8-15 found
- Critical Issues: 3-5
- Risk Level: CRITICAL or HIGH

---

### Option 2: Test with Public API (JSONPlaceholder)

1. **Open Genesis Auditor:** http://localhost:3001

2. **Create New Audit:**
   - Click "New Audit"
   - Select domain: **API Security**
   - Name: `JSONPlaceholder Security Test`
   - URL: `https://jsonplaceholder.typicode.com`
   - Click "Start Audit"

**Expected Results:**
- Compliance Score: 70-85/100 (well-secured)
- Vulnerabilities: 2-4 found
- Risk Level: LOW or MEDIUM

---

### Option 3: Test Without Real API (Demo Mode)

1. **Open Genesis Auditor:** http://localhost:3001

2. **Create New Audit:**
   - Click "New Audit"
   - Select domain: **HIPAA Compliance**
   - Name: `Demo Healthcare API`
   - URL: Leave empty or enter `demo`
   - Click "Start Audit"

**What Happens:**
- System uses intelligent simulation
- Gemini still designs real agent swarm
- Results based on probability simulation
- Perfect for presentations when network is unavailable

---

## 📊 Expected Attack Vectors by Domain

### API Security Domain
- Authentication bypass attempts
- SQL injection tests
- XSS payload injection
- IDOR testing
- Rate limiting checks
- Information disclosure tests
- Verbose error analysis

### HIPAA Domain
- PHI (Protected Health Info) access tests
- Patient record IDOR
- Audit logging verification
- Encryption checks
- Authentication strength

### Financial Fraud Domain
- Transaction manipulation
- Payment bypass attempts
- Account takeover tests
- Privilege escalation
- Rate limiting bypass

### GDPR Domain
- Data deletion endpoint tests
- Data portability checks
- Consent mechanism testing
- Personal data exposure

### PCI-DSS Domain
- Cardholder data protection
- Encryption standard checks
- SQL injection in payment flows
- Network segmentation tests

---

## ⚠️ Important Notes

### For Vulnerable APIs:
- ✅ **Safe to attack** - They're designed for testing
- ✅ Run locally - Full control
- ✅ No legal issues - Intentionally vulnerable
- ✅ Great for demos - Shows real vulnerabilities

### For Public APIs:
- ⚠️ **Test responsibly** - Don't overload servers
- ⚠️ Respect rate limits - Keep requests reasonable
- ⚠️ Read ToS - Ensure testing is allowed
- ✅ Good for showing secure APIs - Most will score high

### For Production APIs:
- ❌ **Get permission first** - Never test without authorization
- ❌ Don't use Genesis Auditor on APIs you don't own
- ❌ Legal consequences - Unauthorized testing is illegal

---

## 🎬 Best Demo Scenario

**For Hackathon Presentation:**

1. **Run OWASP Juice Shop** (shows vulnerabilities)
2. **Run JSONPlaceholder** (shows secure API)
3. **Compare results** side-by-side

**Talking Points:**
- "Watch as Gemini designs different attack strategies for each API"
- "Notice how the vector memory improves on second run"
- "See the real HTTP requests and vulnerability detection"
- "Download professional PDF report in under 60 seconds"

---

## 🔧 Troubleshooting

### Can't reach localhost APIs?
```bash
# Check if container is running
docker ps

# Check logs
docker logs <container-id>

# Restart container
docker restart <container-id>
```

### Genesis backend not responding?
```bash
# Check backend is running
curl http://localhost:8001/

# Restart backend
cd backend && python main.py
```

### Frontend can't connect?
```bash
# Check frontend is running
curl http://localhost:3001/

# Restart frontend
cd frontend && npm run dev
```

---

**Happy Testing! 🚀**

For questions, see main [README.md](README.md)
