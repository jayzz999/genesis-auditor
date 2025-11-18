# 🚀 Genesis Auditor - Quick Reference Card

## One-Page Cheat Sheet

---

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Start everything
./start.sh

# 2. Open browser
# Frontend: http://localhost:3000
# Backend:  http://localhost:8001/docs

# 3. Create audit
# Click "Start Free Audit" → Select HIPAA → Enter API name → Start
```

---

## 📍 URLs

| Service | Development | Production |
|---------|-------------|------------|
| Frontend | http://localhost:3000 | https://your-app.vercel.app |
| Backend | http://localhost:8001 | https://your-api.railway.app |
| API Docs | http://localhost:8001/docs | https://your-api.railway.app/docs |

---

## 🗺️ Page Routes

| Page | URL | Purpose |
|------|-----|---------|
| Landing | `/` | Marketing homepage |
| Dashboard | `/dashboard` | Main control center |
| New Audit | `/dashboard/new-audit` | Create audit |
| Results | `/dashboard/audit/{id}` | View results |
| History | `/dashboard/history` | Past audits |
| Memory | `/dashboard/memory` | Attack patterns |

---

## 🔌 API Endpoints

```bash
# Health Check
GET /

# Domains
GET /api/domains

# Audits
POST /api/audit/start
GET /api/audit/{id}
GET /api/audits/recent?limit=10

# Memory
GET /api/memory/stats
GET /api/memory/patterns/{domain}?limit=10

# WebSocket
WS /ws/audit/{id}
```

---

## 🎨 Components Location

```
frontend/
├── app/page.tsx                 → Landing page
├── app/dashboard/page.tsx       → Dashboard
├── app/dashboard/new-audit/     → New audit
├── app/dashboard/audit/[id]/    → Results
├── components/ui/               → Shadcn UI
├── components/dashboard/        → Custom components
└── lib/api/client.ts            → API client
```

---

## 🛠️ Common Commands

```bash
# Frontend
cd frontend
npm install          # Install dependencies
npm run dev          # Development server
npm run build        # Production build
npm start            # Production server

# Backend
cd backend
source ../venv/bin/activate
python main.py       # Start API server

# Both
./start.sh          # Start frontend + backend
```

---

## 🌍 Environment Variables

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_WS_URL=ws://localhost:8001
```

**Backend (.env):**
```env
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
QDRANT_URL=https://xxxxx.qdrant.io
QDRANT_API_KEY=xxxxx
```

---

## 🚀 Deploy in 3 Steps

### 1. Backend to Railway
```bash
1. Go to railway.app
2. New Project → Deploy from GitHub
3. Select backend folder
4. Add environment variables
5. Deploy!
```

### 2. Frontend to Vercel
```bash
1. Go to vercel.com
2. Import GitHub repo
3. Set root to `frontend/`
4. Add environment variables
5. Deploy!
```

### 3. Update URLs
```bash
1. Copy Railway backend URL
2. Update Vercel env vars:
   - NEXT_PUBLIC_API_URL=https://your-backend.railway.app
   - NEXT_PUBLIC_WS_URL=wss://your-backend.railway.app
3. Redeploy Vercel
```

---

## 🎯 Domain IDs

| Domain | ID | Icon |
|--------|-----|------|
| HIPAA | `hipaa` | 🏥 |
| Financial | `financial` | 💰 |
| GDPR | `gdpr` | 🇪🇺 |
| PCI-DSS | `pci` | 💳 |
| API Security | `api` | 🔌 |

---

## 📊 Risk Levels

| Score | Level | Badge Color |
|-------|-------|-------------|
| 80-100 | Low Risk | 🟢 Green |
| 50-79 | Medium | 🟡 Yellow |
| 0-49 | Critical | 🔴 Red |
| Pending | Pending | ⚪ Gray |

---

## 🐛 Troubleshooting

### Frontend won't start
```bash
cd frontend
rm -rf node_modules .next
npm install
npm run dev
```

### Backend won't connect
```bash
# Check backend is running
curl http://localhost:8001/

# Check environment variables
cat .env

# Restart backend
cd backend
python main.py
```

### WebSocket not connecting
```bash
# Development
ws://localhost:8001/ws/audit/{id}

# Production
wss://your-backend.railway.app/ws/audit/{id}
```

### Build errors
```bash
# Clear cache
cd frontend
rm -rf .next
npm run build
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `start.sh` | Start both servers |
| `frontend/.env.local` | Frontend config |
| `backend/main.py` | API server |
| `.env` | Backend config |
| `DEPLOYMENT_GUIDE.md` | Deploy instructions |
| `WHAT_WAS_BUILT.md` | Complete summary |

---

## 🎨 Color Palette

```css
Background: slate-950, slate-900, slate-800
Accent: purple-600, purple-700
Success: green-600
Warning: yellow-600
Error: red-600
Text: white, gray-400, gray-300
Border: gray-800, gray-700
```

---

## 🔗 Useful Links

- [Next.js Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Shadcn UI](https://ui.shadcn.com/)
- [Vercel Deploy](https://vercel.com/new)
- [Railway Deploy](https://railway.app/new)

---

## 🎯 Testing Checklist

- [ ] Landing page loads
- [ ] Dashboard shows stats
- [ ] Can create new audit
- [ ] Real-time progress works
- [ ] Results display correctly
- [ ] History shows past audits
- [ ] Memory shows patterns
- [ ] WebSocket connects
- [ ] API responds
- [ ] Builds successfully

---

## 💡 Pro Tips

1. **Use ./start.sh** for local development
2. **Check browser console** for errors
3. **Watch API logs** in terminal
4. **Test WebSocket** with browser DevTools
5. **Use localhost:8001/docs** to test API
6. **Deploy backend first**, then frontend
7. **Update env vars** after deploying backend
8. **Check CORS settings** if API fails

---

## 🆘 Quick Help

```bash
# Can't start frontend?
cd frontend && npm install && npm run dev

# Can't start backend?
source venv/bin/activate && cd backend && python main.py

# Environment not working?
cp .env.example .env  # Then edit .env

# Build failing?
cd frontend && rm -rf .next && npm run build

# WebSocket not working?
# Check URL uses ws:// (dev) or wss:// (prod)
```

---

## 📊 Project Stats

- **Total Pages:** 7
- **API Endpoints:** 11
- **Components:** 15+
- **Documentation:** 10,000+ words
- **Build Time:** ~3 seconds
- **Deploy Time:** ~10 minutes

---

## 🎉 Success Indicators

✅ `npm run build` succeeds
✅ All pages load without errors
✅ WebSocket connects on audit page
✅ API returns 200 on health check
✅ Dashboard shows real data
✅ Can create and view audits

---

**Keep this handy while developing!** 📋
