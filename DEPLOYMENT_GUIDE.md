# Genesis Auditor - Complete Deployment Guide

This guide will help you deploy the Genesis Auditor platform using **100% FREE** services.

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  FRONTEND (Vercel)                              │
│  Next.js 14 + Tailwind + Shadcn UI              │
│  https://your-app.vercel.app                    │
│                                                 │
└──────────────────┬──────────────────────────────┘
                   │ WebSocket + REST API
                   ▼
┌─────────────────────────────────────────────────┐
│                                                 │
│  BACKEND (Railway/Render)                       │
│  FastAPI + Python                               │
│  https://your-api.railway.app                   │
│                                                 │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│                                                 │
│  MEMORY SYSTEM (Qdrant Cloud)                   │
│  Vector Database - Free Tier                    │
│  https://cloud.qdrant.io                        │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Option 1: Vercel + Railway (RECOMMENDED)

### Total Cost: $0/month
### Setup Time: 10-15 minutes

### Step 1: Deploy Backend to Railway

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub (free)

2. **Deploy Backend**
   ```bash
   # In your project root
   cd backend

   # Create railway.json
   echo '{
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }' > railway.json
   ```

3. **Push to Railway**
   - Click "New Project" in Railway
   - Select "Deploy from GitHub repo"
   - Choose your genesis-auditor repo
   - Select the `backend` folder
   - Railway will auto-detect Python and deploy!

4. **Set Environment Variables in Railway**
   ```
   ANTHROPIC_API_KEY=your_claude_api_key
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_cloud_url
   QDRANT_API_KEY=your_qdrant_api_key
   ```

5. **Get Your Backend URL**
   - Railway will give you a URL like: `https://genesis-auditor.railway.app`
   - Copy this URL for frontend configuration

### Step 2: Deploy Frontend to Vercel

1. **Push Frontend to GitHub**
   ```bash
   cd ..
   git add .
   git commit -m "Add Genesis Auditor Platform"
   git push origin main
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your GitHub repo
   - Set Root Directory to `frontend`
   - Click "Deploy"

3. **Set Environment Variables in Vercel**
   - In Vercel dashboard, go to Settings → Environment Variables
   - Add:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend.railway.app
     NEXT_PUBLIC_WS_URL=wss://your-backend.railway.app
     ```

4. **Redeploy**
   - Trigger a redeploy in Vercel
   - Your app will be live at `https://your-app.vercel.app`

---

## Option 2: All-in-One Vercel

### Total Cost: $0/month
### Setup Time: 5 minutes
### Limitations: No WebSocket support on free tier

1. **Use Vercel for Both**
   - Deploy frontend as above
   - Create `backend/vercel.json`:
     ```json
     {
       "builds": [
         {
           "src": "main.py",
           "use": "@vercel/python"
         }
       ],
       "routes": [
         {
           "src": "/(.*)",
           "dest": "main.py"
         }
       ]
     }
     ```

2. **Note**: WebSocket won't work on Vercel serverless, so real-time updates won't function. Use Railway/Render for backend if you need WebSocket.

---

## Option 3: Netlify + Render

### Total Cost: $0/month
### Setup Time: 15 minutes

### Backend on Render

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Select `backend` directory
   - Set:
     - Name: `genesis-auditor-api`
     - Environment: Python
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables**
   - Same as Railway setup above

### Frontend on Netlify

1. **Deploy to Netlify**
   ```bash
   cd frontend
   npm install -g netlify-cli
   netlify login
   netlify init
   netlify deploy --prod
   ```

2. **Set Environment Variables**
   - In Netlify dashboard → Site Settings → Environment Variables
   - Add your backend URLs

---

## Backend Requirements File

Create `backend/requirements.txt`:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
anthropic==0.7.0
openai==1.3.5
qdrant-client==1.7.0
pydantic==2.5.0
python-dotenv==1.0.0
websockets==12.0
```

---

## Environment Variables Reference

### Backend (.env)
```env
# Required
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=xxxxx

# Optional
PORT=8001
```

### Frontend (.env.local)
```env
# Development
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_WS_URL=ws://localhost:8001

# Production (set in Vercel/Netlify dashboard)
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_WS_URL=wss://your-backend.railway.app
```

---

## Setting Up Qdrant Cloud (Free)

1. **Create Account**
   - Go to [cloud.qdrant.io](https://cloud.qdrant.io)
   - Sign up for free

2. **Create Cluster**
   - Click "Create Cluster"
   - Select "Free" tier (1GB storage)
   - Choose region closest to your backend

3. **Get Credentials**
   - Copy Cluster URL
   - Create API Key
   - Add to backend environment variables

4. **Collection is Auto-Created**
   - Genesis Auditor will automatically create the `genesis_attacks` collection on first run

---

## Testing Your Deployment

### 1. Test Backend
```bash
curl https://your-backend.railway.app/
# Should return: {"status":"online","service":"Genesis Auditor API"}
```

### 2. Test Frontend
- Visit `https://your-app.vercel.app`
- Click "Start Free Audit"
- Select a domain and create an audit
- Watch real-time progress!

### 3. Test WebSocket
- Open browser console
- Start an audit
- You should see WebSocket connection messages

---

## Troubleshooting

### Backend Issues

**Error: "Module not found"**
```bash
# Ensure requirements.txt is complete
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

**Error: "Connection to Qdrant failed"**
- Check QDRANT_URL and QDRANT_API_KEY are correct
- Ensure Qdrant cluster is running
- Check firewall settings

**WebSocket not connecting**
- Verify backend URL uses `wss://` (not `ws://`) in production
- Check CORS settings in backend
- Ensure Railway/Render allows WebSocket connections

### Frontend Issues

**Error: "Failed to fetch"**
- Check API URL in environment variables
- Verify backend is running
- Check CORS configuration

**Real-time updates not working**
- Verify WebSocket URL is correct
- Check browser console for errors
- Ensure backend WebSocket endpoint is accessible

---

## Custom Domain (Optional)

### Frontend Custom Domain
1. In Vercel → Settings → Domains
2. Add your domain (e.g., `genesisauditor.com`)
3. Update DNS records as instructed
4. SSL is automatically configured!

### Backend Custom Domain
1. In Railway → Settings → Domains
2. Add custom domain
3. Update DNS with provided CNAME
4. Update frontend env vars with new backend URL

---

## Cost Breakdown

| Service | Free Tier | Limits |
|---------|-----------|--------|
| **Vercel** | Yes | 100GB bandwidth, unlimited projects |
| **Railway** | $5 credit/month | ~500 hours runtime |
| **Render** | Yes | 750 hours/month |
| **Qdrant Cloud** | Yes | 1GB storage |
| **Total** | **$0/month** | Perfect for demos & testing |

---

## Scaling to Production

When you're ready to scale:

1. **Upgrade Railway** ($5/month) for more resources
2. **Add Monitoring** - Use Railway/Render built-in metrics
3. **Add Redis** - Cache API responses
4. **Add PostgreSQL** - Store audit history permanently
5. **Custom Domain** - Professional branding

---

## Next Steps

1. Deploy backend to Railway
2. Deploy frontend to Vercel
3. Set up Qdrant Cloud
4. Configure environment variables
5. Test the platform
6. Share your deployed URL!

---

## Support

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- Qdrant Docs: https://qdrant.tech/documentation
- Genesis Auditor Issues: https://github.com/your-repo/issues

---

**Congratulations!** You now have a production-ready AI security platform running 100% free!
