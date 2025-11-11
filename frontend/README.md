# Rajniti Landing Page

A beautiful, India-themed landing page for the Rajniti Election Data API built with Next.js 16, TypeScript, and Tailwind CSS.

## 🚀 Features

-   **Server-Side Rendering (SSR)**: Built with Next.js App Router for optimal performance
-   **India-Themed Design**: Orange, white, and green color scheme reflecting Indian heritage
-   **Fully Responsive**: Works seamlessly on desktop, tablet, and mobile devices
-   **SEO Optimized**: Proper metadata and semantic HTML
-   **Fast & Lightweight**: Minimal dependencies, optimized for performance

## 📋 Sections

1. **Hero Section**: Highlights the core mission of making election data accessible
2. **Why Rajniti**: Explains the purpose and benefits of the platform
3. **Join Our Community**: Encourages open-source contributions
4. **API Section**: Marked as "Coming Soon" with future feature highlights
5. **Footer**: Links and copyright information

## 🛠️ Tech Stack

-   **Framework**: Next.js 16 (App Router)
-   **Language**: TypeScript
-   **Styling**: Tailwind CSS
-   **Deployment**: Vercel-ready (also compatible with Netlify, GCP, AWS)

## 🏃‍♂️ Getting Started

### Prerequisites

-   Node.js 18+
-   npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

The application will be available at `http://localhost:3000`

## 📦 Deployment

### Deploy to Vercel (Recommended)

1. Push your code to GitHub
2. Import your repository on [Vercel](https://vercel.com)
3. Set the root directory to `frontend`
4. Deploy! Vercel will auto-detect Next.js configuration

Alternatively, use the Vercel CLI:

```bash
npm install -g vercel
cd frontend
vercel
```

### Deploy to Netlify

1. Push your code to GitHub
2. Import your repository on [Netlify](https://netlify.com)
3. Configure build settings:
    - **Base Directory**: `frontend`
    - **Build Command**: `npm run build`
    - **Publish Directory**: `frontend/.next`
4. Deploy!

### Deploy to GCP (Cloud Run)

Create a `Dockerfile` in the frontend directory:

```dockerfile
FROM node:20-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Build the application
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
ENV PORT 3000
CMD ["node", "server.js"]
```

Then deploy:

```bash
# Build and deploy
gcloud run deploy rajniti-frontend \
  --source . \
  --platform managed \
  --region asia-south2 \
  --allow-unauthenticated
```

## 📁 Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with metadata
│   ├── page.tsx            # Landing page component
│   ├── globals.css         # Global styles
│   └── favicon.ico         # Favicon
├── public/                 # Static assets
├── package.json           # Dependencies
├── tsconfig.json          # TypeScript config
├── postcss.config.mjs     # PostCSS & Tailwind config
└── next.config.ts         # Next.js config
```

## 🎨 Customization

### Colors

The India-themed colors are defined in Tailwind and can be customized in `app/page.tsx`:

-   **Orange**: `orange-500`, `orange-600` (Saffron)
-   **White**: `white`
-   **Green**: `green-500`, `green-600`

### Content

Edit the content directly in `app/page.tsx`:

-   Hero section: Update heading and description
-   About section: Modify the feature cards
-   Contribute section: Change contribution types
-   API section: Update coming soon features

## 🔧 Configuration

### Environment Variables

No environment variables are required for the landing page. If you need to add API endpoints or external services, create a `.env.local` file:

```bash
# Example
NEXT_PUBLIC_API_URL=https://api.rajniti.com
```

## 📄 License

This project is part of the Rajniti platform and is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

Built with ❤️ for 🇮🇳 Democracy
