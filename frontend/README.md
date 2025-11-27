# Rajniti Frontend 🗳️

Beautiful, India-themed landing page for the Rajniti Election Data API built with Next.js 16, TypeScript, and Tailwind CSS.

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Visit http://localhost:3000
```

### Build for Production

```bash
# Build the application
npm run build

# Start production server
npm start
```

## 🌐 Deploy to Vercel

### Option 1: GitHub Integration (Recommended)

1. Push your code to GitHub
2. Go to [Vercel Dashboard](https://vercel.com)
3. Click "Add New Project"
4. Import your GitHub repository
5. Configure project settings:
    - **Framework Preset**: Next.js (auto-detected)
    - **Root Directory**: `frontend` (if deploying from monorepo)
    - **Build Command**: `npm run build` (auto-detected)
    - **Output Directory**: `.next` (auto-detected)
6. Add environment variables (if needed):
    - `NEXT_PUBLIC_API_URL`: Your backend API URL
7. Click "Deploy"

Vercel will automatically detect Next.js and configure everything!

### Option 2: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Navigate to frontend directory
cd frontend

# Deploy to production
vercel --prod
```

### Option 3: Vercel Dashboard (Manual)

1. Go to [Vercel Dashboard](https://vercel.com/new)
2. Click "Import Project"
3. Select your Git provider and repository
4. Configure settings (auto-detected for Next.js)
5. Deploy

## ⚙️ Configuration

### Environment Variables

Create `.env.local` for local development:

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For Vercel deployment, set environment variables in:
**Project Settings → Environment Variables**

### Backend Integration

If you have a backend API, update `vercel.json`:

```json
{
    "rewrites": [
        {
            "source": "/api/:path*",
            "destination": "https://your-backend-url.run.app/api/v1/:path*"
        }
    ]
}
```

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── dashboard/         # Dashboard page
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/            # React components
│   └── PreambleSection.tsx
├── public/               # Static assets
├── next.config.ts        # Next.js configuration
├── vercel.json            # Vercel deployment config
├── package.json          # Dependencies
└── tsconfig.json         # TypeScript config
```

## 🎨 Features

-   ⚡ Next.js 16 with App Router
-   🎨 Tailwind CSS 4
-   📱 Fully Responsive Design
-   🇮🇳 India-themed Color Scheme (Orange, White, Green)
-   🚀 Optimized for Vercel Deployment
-   🔒 Security Headers Configured
-   ⚡ Static Asset Caching
-   🌐 API Proxy Support

## 🛠️ Tech Stack

-   **Framework**: Next.js 16
-   **Language**: TypeScript
-   **Styling**: Tailwind CSS 4
-   **Deployment**: Vercel (recommended)
-   **Package Manager**: npm

## 📦 Dependencies

```json
{
    "dependencies": {
        "react": "19.2.0",
        "react-dom": "19.2.0",
        "next": "16.0.1"
    },
    "devDependencies": {
        "typescript": "^5",
        "@types/node": "^20",
        "@types/react": "^19",
        "@types/react-dom": "^19",
        "@tailwindcss/postcss": "^4",
        "tailwindcss": "^4",
        "eslint": "^9",
        "eslint-config-next": "16.0.1"
    }
}
```

## 🔍 Available Scripts

```bash
# Development
npm run dev          # Start dev server on http://localhost:3000

# Production
npm run build        # Build for production
npm start           # Start production server

# Linting
npm run lint        # Run ESLint
```

## 🌟 Vercel Configuration

The `vercel.json` file includes:

-   ✅ Next.js framework detection
-   ✅ Security headers (XSS, Frame protection, Content-Type)
-   ✅ Static asset caching
-   ✅ API proxy support (rewrites)
-   ✅ Automatic build optimization

## 🐛 Troubleshooting

### Build Fails on Vercel

1. Check Node.js version (Vercel uses Node.js 20 by default)
2. Verify all dependencies are in `package.json`
3. Check build logs in Vercel Dashboard
4. Ensure `next.config.ts` is properly configured

### 404 Errors After Deployment

1. **Check Root Directory**: If deploying from monorepo, set Root Directory to `frontend` in Vercel project settings
2. **Verify Build Output**: Ensure `.next` folder is generated correctly
3. **Check Routes**: Verify all page files exist in `app/` directory
4. **Review Build Logs**: Check Vercel deployment logs for errors

### API Calls Not Working

1. Verify `NEXT_PUBLIC_API_URL` is set in Vercel environment variables
2. Check CORS settings on backend
3. Verify API proxy in `vercel.json` is configured correctly
4. Ensure backend URL is accessible from Vercel's servers

### Styling Issues

1. Clear `.next` cache: `rm -rf .next`
2. Rebuild: `npm run build`
3. Check Tailwind CSS configuration

## 📚 Resources

-   [Next.js Documentation](https://nextjs.org/docs)
-   [Vercel Documentation](https://vercel.com/docs)
-   [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## 🤝 Contributing

See the main [README.md](../readme.md) for contribution guidelines.

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details.

---

**Built with ❤️ for 🇮🇳 Indian Democracy**
