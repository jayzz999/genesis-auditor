# Genesis Auditor - Frontend

The professional web interface for the Genesis Auditor AI-powered security platform.

## Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Shadcn UI** - Beautiful, accessible components
- **WebSocket** - Real-time audit progress updates

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend API running on `http://localhost:8001`

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_WS_URL=ws://localhost:8001
```

## Deployment

### Option 1: Vercel (Recommended)

1. Push your code to GitHub
2. Import the project in Vercel
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL` - Your Railway backend URL
   - `NEXT_PUBLIC_WS_URL` - Your Railway WebSocket URL
4. Deploy!

```bash
# Or use Vercel CLI
npm install -g vercel
vercel --prod
```

### Option 2: Netlify

```bash
npm install -g netlify-cli
netlify deploy --prod
```

## Features

### Landing Page
- Professional hero section
- Feature showcase
- How it works explanation
- Call-to-action sections

### Dashboard
- Overview with stats
- Recent audits list
- Memory system statistics
- Quick actions

### New Audit
- Domain selection (HIPAA, PCI, GDPR, etc.)
- API configuration
- Real-time audit initiation

### Audit Results
- Live progress tracking with WebSocket
- Compliance score visualization
- Vulnerability findings
- Risk level assessment
- PDF report download (future)

### Audit History
- Complete audit history
- Filter by domain
- View past results

### Memory System
- Stored attack patterns
- Domain-specific views
- System statistics

## Project Structure

```
frontend/
├── app/
│   ├── page.tsx                    # Landing page
│   ├── dashboard/
│   │   ├── layout.tsx              # Dashboard layout with sidebar
│   │   ├── page.tsx                # Dashboard overview
│   │   ├── new-audit/page.tsx      # Create new audit
│   │   ├── audit/[id]/page.tsx     # Audit results (dynamic)
│   │   ├── history/page.tsx        # Audit history
│   │   └── memory/page.tsx         # Memory system
├── components/
│   ├── ui/                         # Shadcn UI components
│   └── dashboard/
│       └── Sidebar.tsx             # Dashboard navigation
├── lib/
│   ├── api/
│   │   └── client.ts               # API client & WebSocket
│   └── utils.ts                    # Utility functions
└── public/                         # Static assets
```

## API Integration

The frontend communicates with the FastAPI backend via:

- **REST API** for data fetching and audit initiation
- **WebSocket** for real-time audit progress updates

See [lib/api/client.ts](lib/api/client.ts) for the complete API client.

## Real-time Updates

Audit progress is tracked in real-time using WebSocket:

1. User starts audit
2. Frontend connects to WebSocket endpoint
3. Backend sends progress updates
4. UI updates in real-time
5. Final results are displayed when complete

## Styling

This project uses:
- Tailwind CSS for utility classes
- Shadcn UI for pre-built components
- Custom gradient backgrounds
- Dark theme optimized

## Performance

- Server-side rendering with Next.js 14
- Optimized WebSocket connections
- Lazy loading for routes
- Image optimization

## License

MIT License - See LICENSE file for details
