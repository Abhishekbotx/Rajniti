# 🗳️ Rajniti - Simple Election Data API

> **A clean, lightweight Flask API for Indian election data with a beautiful landing page**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16-black.svg)](https://nextjs.org/)
[![API Version](https://img.shields.io/badge/API-v1.0-orange.svg)](#api-documentation)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Data Coverage](https://img.shields.io/badge/Data-50K%2B_Records-purple.svg)](#data-coverage)

A simple, clean REST API serving Indian Election Commission data from JSON files. Built with minimal Flask setup for easy deployment and scraping capabilities. Includes a beautiful, India-themed landing page built with Next.js.

## 🚢 Quick Deployment

| Platform | Type | Command | Status |
|----------|------|---------|--------|
| **Netlify** | Frontend | `netlify deploy --prod` | ✅ Ready |
| **GCP Cloud Run** | Backend | `gcloud builds submit` | ✅ Ready |
| **Docker** | Full Stack | `docker-compose up -d` | ✅ Ready |
| **Vercel** | Frontend | `vercel --prod` | ✅ Ready |

👉 **Jump to**: [Netlify Deployment Guide](#deploy-to-netlify-) • [Backend Deployment](#deployment) • [Docker Setup](#option-1-docker-recommended)

---

## 🌟 **Key Features**

<div align="center">

| Feature                     | Description                                               |
| --------------------------- | --------------------------------------------------------- |
| 🚀 **Simple Flask API**     | Clean RESTful endpoints serving JSON data                 |
| 💾 **Database Support**     | PostgreSQL/Supabase support with easy migration           |
| 🌐 **Landing Page**         | Beautiful Next.js landing page with India-themed design   |
| 📊 **Election Data**        | 50,000+ records across Lok Sabha & Assembly elections     |
| 🔍 **Search & Filter**      | Basic search and filtering capabilities                   |
| 🕸️ **Intelligent Scraping** | Advanced scraping system with retry logic & rate limiting |
| 📸 **Image Downloads**      | Candidate photos and party symbols extraction             |
| ⚡ **Lightweight**          | Minimal dependencies, fast startup                        |
| 🐳 **Docker Ready**         | Single container deployment                               |

</div>

---

## 📊 **Data Coverage**

<div align="center">

| Election                | Candidates  | Constituencies | Parties  | Status               |
| ----------------------- | ----------- | -------------- | -------- | -------------------- |
| **Lok Sabha 2024**      | 3,802+      | 543            | 211+     | ✅ Complete          |
| **Delhi Assembly 2025** | 6,922+      | 70             | 11+      | ✅ Complete          |
| **Maharashtra 2024**    | 39,817+     | 288            | 76+      | ✅ Complete          |
| **Total Coverage**      | **50,541+** | **901**        | **298+** | **🎯 Comprehensive** |

</div>

---

## 🚀 **Quick Start**

### **Option 1: Docker (Recommended)**

```bash
# Clone the repository
git clone https://github.com/your-username/rajniti.git
cd rajniti

# Start with Docker Compose
docker-compose up -d

# API available at http://localhost:8080
# Health check: http://localhost:8080/api/v1/health
```

### **Option 2: Local Installation (Automated)**

```bash
# Clone and setup
git clone https://github.com/your-username/rajniti.git
cd rajniti

# Automated setup (recommended)
make setup

# Start development server
make dev

# Or run directly
python run.py
```

### **Option 3: Manual Setup**

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run development server
python run.py
```

---

## 💾 **Database Support**

Rajniti now supports PostgreSQL database storage in addition to JSON files! Perfect for production deployments and works seamlessly with both local PostgreSQL and Supabase.

### **🎯 Features**

-   **Dual Storage**: Use JSON files or PostgreSQL database
-   **Supabase Ready**: Works out-of-the-box with Supabase
-   **Local PostgreSQL**: Full support for local development
-   **CRUD Operations**: Complete Create, Read, Update, Delete operations
-   **Easy Migration**: Script to migrate existing JSON data to database
-   **Alembic Migrations**: Database schema version control

### **Quick Database Setup**

#### **Option 1: Local PostgreSQL**

```bash
# Install PostgreSQL (if not already installed)
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS (with Homebrew)
brew install postgresql

# Create database
createdb rajniti

# Set environment variable
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/rajniti"

# Initialize database (create tables)
python scripts/db.py init

# Migrate JSON data to database
python scripts/db.py migrate
```

#### **Option 2: Supabase (Recommended for Production)**

```bash
# 1. Create a Supabase project at https://supabase.com
# 2. Get your database connection string from Project Settings → Database (URI format)
# 3. Set environment variable
export DATABASE_URL="postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres"

# Initialize database (create tables)
python scripts/db.py init

# Migrate JSON data to database
python scripts/db.py migrate
```

### **Database Management Commands**

```bash
# Initialize database (create tables)
python scripts/db.py init

# Migrate JSON data to database
python scripts/db.py migrate

# Preview migration without changes
python scripts/db.py migrate --dry-run

# Reset database (⚠️ deletes all data)
python scripts/db.py reset
```

### **Database Models**

Three main models with full CRUD operations:

-   **Party**: Political parties (id, name, short_name, symbol)
-   **Constituency**: Electoral districts (id, name, state_id)
-   **Candidate**: Election candidates (id, name, party_id, constituency_id, state_id, status, type, image_url)

### **Using Database in Code**

```python
from app.database import get_db_session
from app.database.models import Party, Constituency, Candidate

# Create a party
with get_db_session() as session:
    party = Party.create(session, "123", "Example Party", "EP", "Lotus")

# Get all parties
with get_db_session() as session:
    parties = Party.get_all(session)

# Search candidates
with get_db_session() as session:
    candidates = Candidate.search_by_name(session, "Modi")
```

### **Configuration**

Set the `DATABASE_URL` environment variable to your PostgreSQL connection string:

```bash
# Local PostgreSQL
export DATABASE_URL="postgresql://user:password@localhost:5432/rajniti"

# Supabase
export DATABASE_URL="postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres"
```

📚 **Full documentation**: See [app/database/README.md](app/database/README.md) for detailed usage, migrations, and troubleshooting.

---

## 🌐 **Landing Page**

The Rajniti landing page is a beautiful, India-themed website built with Next.js 16, TypeScript, and Tailwind CSS.

### **Features**

-   🎨 **India-Themed Design**: Orange, white, and green color scheme
-   ⚡ **Server-Side Rendering**: Built with Next.js App Router for optimal performance
-   📱 **Fully Responsive**: Works seamlessly on all devices
-   🚀 **Easy Deployment**: Compatible with Vercel, Netlify, GCP, and AWS

### **Quick Start (Frontend)**

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Visit http://localhost:3000
```

### **Deploy to Netlify** 🚀

Deploy the Rajniti frontend to Netlify in just a few minutes!

#### **Step 1: Push to Git Repository**

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/your-username/rajniti.git
git push -u origin main
```

#### **Step 2: Deploy via Netlify Dashboard**

1. **Sign up** at [netlify.com](https://app.netlify.com/signup)
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect your **GitHub/GitLab/Bitbucket** account
4. Select your **rajniti repository**
5. Configure build settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `.next`
   - **Framework**: Next.js (auto-detected)
6. Click **"Deploy site"**

#### **Step 3: Add Environment Variables (Optional)**

If you have a backend API, add this environment variable in Netlify:

1. Go to **Site settings** → **Environment variables**
2. Add variable:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://your-backend-api.com`

#### **Step 4: Update Backend URL (If applicable)**

If using a separate backend, edit `frontend/netlify.toml`:

```toml
[[redirects]]
  from = "/api/*"
  to = "https://your-backend-url.run.app/api/:splat"
  status = 200
  force = false
```

#### **Deploy via Netlify CLI**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Navigate to frontend
cd frontend

# Deploy (follow prompts)
netlify deploy --prod
```

#### **Continuous Deployment**

Once connected to GitHub, Netlify automatically deploys when you push to `main`:

```bash
git add .
git commit -m "Update frontend"
git push origin main
# ✅ Netlify automatically rebuilds and deploys!
```

#### **Custom Domain (Optional)**

1. Go to **Domain settings** in Netlify Dashboard
2. Click **"Add custom domain"**
3. Follow DNS configuration instructions

---

### **Alternative Deployment Options**

**Vercel (Alternative to Netlify):**

```bash
cd frontend
npx vercel --prod
```

**GCP Cloud Run:**

```bash
gcloud run deploy rajniti-frontend --source ./frontend
```

**Docker (Self-hosted):**

```bash
cd frontend
docker build -t rajniti-frontend .
docker run -p 3000:3000 rajniti-frontend
```

---

## 🕸️ **Data Scraping**

### **🎯 Overview**

Rajniti includes powerful scraping capabilities to collect fresh election data from the Election Commission of India (ECI) website. The scraping system is modular and supports both Lok Sabha and Assembly elections.

### **🚀 Quick Start Scraping**

#### **✨ NEW: Interactive Scraper (Recommended)**

The easiest way to scrape election data - just provide the URL!

```bash
# Activate virtual environment
source venv/bin/activate

# Run interactive scraper (auto-detects everything!)
python scripts/scrape_interactive.py

# You'll be prompted for:
# 1. Election Results URL (e.g., https://results.eci.gov.in/ResultAcGenFeb2025)
# 2. Election Type (LOK_SABHA or VIDHAN_SABHA)
# Everything else is auto-discovered!
```

#### **Legacy Scraping Methods**

```bash
# Direct URL scraping (no hardcoded values!)
python scripts/scrape_lok_sabha.py --url https://results.eci.gov.in/PcResultGenJune2024/index.htm
python scripts/scrape_vidhan_sabha.py --url https://results.eci.gov.in/ResultAcGenFeb2025

# Legacy: State/Year based (constructs URLs automatically)
python scripts/scrape_lok_sabha.py --year 2024
python scripts/scrape_vidhan_sabha.py --state DL --year 2025

# Using Make commands
make setup  # Setup environment first
make scrape-help # Show scraping help
```

### **📋 Available Scrapers**

<div align="center">

| Scraper                  | Description                     | Command                            | Data Output                  |
| ------------------------ | ------------------------------- | ---------------------------------- | ---------------------------- |
| **✨ Interactive (NEW)** | URL-based, auto-discovery       | `scrape_interactive.py`            | Complete election data       |
| **🏛️ Lok Sabha**         | Parliamentary elections         | `scrape_lok_sabha.py --url URL`    | Candidates, Parties, Results |
| **🏛️ Vidhan Sabha**      | State assembly elections        | `scrape_vidhan_sabha.py --url URL` | Assembly candidates, Results |
| **🎯 Complete**          | All elections combined (legacy) | `scrape_all.py --year 2024`        | Comprehensive dataset        |

</div>

### **⚙️ Scraping Commands**

#### **✨ Interactive Scraper (Recommended)**

```bash
# Interactive mode - easiest way!
python scripts/scrape_interactive.py

# The script will guide you through:
# 1. Enter the ECI results URL
# 2. Confirm or select election type (auto-detected)
# 3. Review configuration
# 4. Start scraping with full auto-discovery!

# Example URLs you can use:
# - https://results.eci.gov.in/PcResultGenJune2024/index.htm         (Lok Sabha 2024)
# - https://results.eci.gov.in/ResultAcGenFeb2025     (Delhi 2025)
# - https://results.eci.gov.in/ResultAcGenOct2024     (Maharashtra 2024)
```

#### **Direct URL Scraping**

```bash
# Lok Sabha Elections (URL-based)
python scripts/scrape_lok_sabha.py --url https://results.eci.gov.in/PcResultGenJune2024/index.htm

# Vidhan Sabha Elections (URL-based)
python scripts/scrape_vidhan_sabha.py --url https://results.eci.gov.in/ResultAcGenFeb2025

# Custom output directory
python scripts/scrape_lok_sabha.py --url URL --output-dir data/custom
python scripts/scrape_vidhan_sabha.py --url URL --output-dir data/custom
```

### **🏗️ Scraper Architecture (Simplified)**

```
app/scrapers/
├── base.py                    # 🔧 Utility functions (no classes)
│   ├── get_with_retry()       # HTTP requests with retry logic
│   ├── save_json()            # Save data to JSON files
│   ├── clean_votes()          # Clean vote count strings
│   └── clean_margin()         # Clean margin strings
├── lok_sabha.py              # 🏛️ Single Lok Sabha scraper
│   └── LokSabhaScraper       # One class that does everything
│       ├── scrape()          # Main orchestrator
│       ├── _scrape_parties() # Party data extraction
│       ├── _scrape_constituencies()  # Constituency discovery
│       ├── _scrape_candidates()      # Candidate data extraction
│       └── _extract_metadata()       # Election metadata
└── vidhan_sabha.py           # 🏛️ Single Vidhan Sabha scraper
    └── VidhanSabhaScraper    # One class that does everything
        ├── scrape()          # Main orchestrator
        ├── _detect_state_info()      # Auto-detect state & year
        ├── _scrape_parties()         # Party data extraction
        ├── _scrape_constituencies()  # Constituency discovery
        ├── _scrape_candidates()      # Candidate data extraction
        └── _save_all_data()          # Save all 4 JSON files

scripts/
└── scripts/scrape_interactive.py     # ✨ Interactive URL-based scraper
```

**Key Principles:**

-   ✅ No hardcoded state names, constituencies, or candidates
-   ✅ Everything scraped and auto-detected from ECI website
-   ✅ Auto-generates folder names from scraped data
-   ✅ Each scraper is self-contained - one URL input → 4 JSON outputs
-   ✅ Simple, linear flow: URL → Scrape → Save

### **📊 Data Sources & URLs**

The scrapers automatically fetch data from:

-   **Lok Sabha 2024**: `https://results.eci.gov.in/PcResultGenJune2024/index.htm/`
-   **Assembly Elections**: State-specific ECI result pages
-   **Party Results**: Party-wise winner lists
-   **Candidate Data**: Complete candidate profiles with photos
-   **Constituency Info**: Constituency-wise detailed results

### **⚡ Scraping Features**

-   **✨ Auto-Discovery**: Automatically finds constituencies and parties (NEW!)
-   **🌐 URL-Based**: No hardcoded values - works with any ECI URL (NEW!)
-   **🤖 Interactive Mode**: Guided scraping with smart defaults (NEW!)
-   **🔄 Retry Logic**: Automatic retry with exponential backoff
-   **🛡️ Rate Limiting**: Respectful scraping with delays
-   **📸 Image Downloads**: Candidate photos and party symbols
-   **🧹 Data Cleaning**: Automatic data normalization
-   **📁 JSON Output**: Clean, structured data files
-   **🔍 Error Handling**: Comprehensive error reporting
-   **📈 Progress Tracking**: Real-time scraping progress
-   **🎯 Flexible Scraping**: URL-based or legacy state/year modes

### **🛠️ Advanced Usage**

#### **Custom Scraping Configuration**

```python
from app.scrapers import LokSabhaScraper, VidhanSabhaScraper

# Simple URL-based scraping - everything auto-detected!
lok_sabha_scraper = LokSabhaScraper(
    url="https://results.eci.gov.in/PcResultGenJune2024/index.htm"
)

vidhan_sabha_scraper = VidhanSabhaScraper(
    url="https://results.eci.gov.in/ResultAcGenFeb2025"
)

# Run scraping - automatically:
# 1. Detects state/year from URL and page
# 2. Scrapes parties, constituencies, candidates
# 3. Generates folder name (e.g., "DL_2025_ASSEMBLY")
# 4. Saves 4 JSON files in proper structure
lok_sabha_scraper.scrape()
vidhan_sabha_scraper.scrape()

# Data is saved to:
# - app/data/lok_sabha/lok-sabha-{year}/
# - app/data/vidhan_sabha/{STATE}_{YEAR}_ASSEMBLY/
# - app/data/elections/ (metadata files)
```

#### **Environment Variables**

```bash
# Configure scraping behavior
export ECI_BASE_URL="https://results.eci.gov.in"
export SCRAPER_RETRY_ATTEMPTS=3
export SCRAPER_RETRY_DELAY=2
export SCRAPER_TIMEOUT=30
```

### **🎭 Supported Elections**

<div align="center">

| Election Type      | Years Available  | States Supported | Status        |
| ------------------ | ---------------- | ---------------- | ------------- |
| **Lok Sabha**      | 2024, 2019, 2014 | All India        | ✅ Active     |
| **Delhi Assembly** | 2025, 2020, 2015 | Delhi            | ✅ Active     |
| **Maharashtra**    | 2024, 2019       | Maharashtra      | ✅ Active     |
| **Other States**   | Various          | Generic Support  | 🔄 On Request |

</div>

### **📋 Output Data Structure**

Each scraper produces 4 JSON files:

#### **1. parties.json**

```json
[
    {
        "party_name": "Bharatiya Janata Party",
        "symbol": "Lotus",
        "total_seats": 240
    }
]
```

#### **2. constituencies.json**

```json
[
    {
        "constituency_id": "1",
        "constituency_name": "Constituency Name",
        "state_id": "DL"
    }
]
```

#### **3. candidates.json**

**Lok Sabha format:**

```json
[
    {
        "party_id": 369,
        "constituency": "Varanasi(77)",
        "candidate_name": "NARENDRA MODI",
        "votes": "612970",
        "margin": "152513"
    }
]
```

**Vidhan Sabha format:**

```json
[
    {
        "Constituency Code": "U051",
        "Name": "Candidate Name",
        "Party": "Party Name",
        "Status": "WON",
        "Votes": "12345",
        "Margin": "1234",
        "Image URL": "https://..."
    }
]
```

#### **4. Election Metadata (elections/\*.json)**

**Lok Sabha:**

```json
{
    "election_id": "lok-sabha-2024",
    "name": "Lok Sabha General Election 2024",
    "type": "LOK_SABHA",
    "year": 2024,
    "total_constituencies": 543,
    "total_candidates": 3802,
    "total_parties": 211,
    "result_status": "DECLARED",
    "winning_party": "Bharatiya Janata Party",
    "winning_party_seats": 240
}
```

**Vidhan Sabha:**

```json
{
    "election_id": "DL_2025_ASSEMBLY",
    "name": "Delhi Assembly Election 2025",
    "type": "VIDHANSABHA",
    "year": 2025,
    "state_id": "DL",
    "state_name": "Delhi",
    "total_constituencies": 70,
    "total_candidates": 6914,
    "total_parties": 3,
    "result_status": "DECLARED",
    "winning_party": "Bharatiya Janata Party",
    "winning_party_seats": 48,
    "runner_up_party": "Aam Aadmi Party",
    "runner_up_seats": 22
}
```

### **🚨 Important Notes**

-   **⏰ Respectful Scraping**: Built-in delays to avoid overwhelming ECI servers
-   **🔄 Data Updates**: Re-run scrapers to get latest results
-   **💾 Storage**: Large datasets may require significant disk space
-   **🌐 Internet Required**: Active internet connection needed for scraping
-   **📅 Election Timing**: Best results during and after election declaration

### **🐛 Troubleshooting Scraping**

```bash
# Common issues and solutions

# 1. Connection timeout
python scripts/scrape_all.py --year 2024  # Increase timeout in config

# 2. Missing dependencies
pip install -r requirements.txt

# 3. Permission errors
chmod +x scripts/scrape_all.py

# 4. Rate limiting
# Wait and retry - scrapers include automatic rate limiting

# 5. Incomplete data
# Check network connection and ECI website availability
```

---

## 📚 **API Documentation**

### **🎯 Simple API Documentation**

-   **API Base URL**: `http://localhost:8080/api/v1/`
-   **Health Check**: `http://localhost:8080/api/v1/health`

### **🔥 Core Endpoints**

#### **Elections API**

```bash
GET /api/v1/elections                             # All elections
GET /api/v1/elections/{election-id}               # Election details
GET /api/v1/elections/{election-id}/results       # Election results
GET /api/v1/elections/{election-id}/winners       # Winners only
```

#### **Candidates API**

```bash
GET /api/v1/candidates/search?q=modi              # Search candidates
GET /api/v1/candidates/winners                    # All winners
GET /api/v1/candidates/party/{party-name}         # Party candidates
GET /api/v1/elections/{id}/candidates/{id}        # Candidate details
```

#### **Constituencies API**

```bash
GET /api/v1/elections/{id}/constituencies          # Election constituencies
GET /api/v1/elections/{id}/constituencies/{id}     # Constituency details
GET /api/v1/constituencies/state/{state-code}      # State constituencies
```

#### **Parties API**

```bash
GET /api/v1/elections/{id}/parties                 # Election parties
GET /api/v1/elections/{id}/parties/{name}          # Party details
GET /api/v1/parties                               # All parties
GET /api/v1/parties/{name}/performance            # Party performance
```

---

## 💡 **Usage Examples**

### **Basic Queries**

```bash
# Get all elections
curl "http://localhost:8080/api/v1/elections"

# Search for candidates named "Modi"
curl "http://localhost:8080/api/v1/candidates/search?q=modi"

# Get Lok Sabha 2024 winners
curl "http://localhost:8080/api/v1/elections/lok-sabha-2024/winners"

# Get all parties
curl "http://localhost:8080/api/v1/parties"
```

### **Filtering Examples**

```bash
# Get candidates by party
curl "http://localhost:8080/api/v1/candidates/party/Bharatiya%20Janata%20Party"

# Get constituency candidates
curl "http://localhost:8080/api/v1/elections/delhi-assembly-2025/constituencies/DL-1/candidates"

# Get party performance
curl "http://localhost:8080/api/v1/parties/Bharatiya%20Janata%20Party/performance"
```

### **Python Integration**

```python
import requests

# Simple API client
BASE_URL = "http://localhost:8080/api/v1"

# Search for candidates
response = requests.get(f"{BASE_URL}/candidates/search", params={"q": "modi"})
data = response.json()

if data['success']:
    for candidate in data['data']['candidates']:
        name = candidate.get('Name') or candidate.get('candidate_name', '')
        party = candidate.get('Party', '')
        print(f"{name} - {party}")

# Get election details
response = requests.get(f"{BASE_URL}/elections/lok-sabha-2024")
election = response.json()
print(f"Election: {election['data']['name']}")
print(f"Total candidates: {election['data']['statistics']['total_candidates']}")
```

---

## 🏗️ **Architecture**

```
rajniti/
├── app/
│   ├── controllers/            # 🎯 MVC Controllers (business logic)
│   ├── core/                   # 🔧 Simple utilities & exceptions
│   ├── data/                   # 📊 Election data (JSON files)
│   │   ├── lok_sabha/          # Lok Sabha election data
│   │   └── vidhan_sabha/       # Assembly election data
│   ├── models/                 # 📋 Pydantic models
│   ├── routes/                 # 🌐 Flask API routes
│   ├── services/               # 💾 Data access layer
│   └── __init__.py             # Flask app factory
├── tests/                      # Test files
├── requirements.in             # 📦 Direct dependencies
├── requirements.txt            # 📦 Compiled dependencies (pip-compile)
├── docker-compose.yml          # 🐳 Docker setup
├── dockerfile                  # 🐳 Container config
└── run.py                      # 🚀 Development server
```

---

## 🔧 **Configuration**

### **Environment Variables**

```bash
# Application (minimal configuration)
SECRET_KEY=your-secret-key              # Flask secret key
FLASK_ENV=production                    # Environment (development/production)

# Database (optional)
DATABASE_URL=postgresql://user:password@localhost:5432/rajniti  # PostgreSQL connection
# Perplexity AI API (for search functionality)
PERPLEXITY_API_KEY=your-perplexity-api-key-here
```

#### Common Errors

1. **"Perplexity API key not provided"**
   - Solution: Set `PERPLEXITY_API_KEY` environment variable or add to `.env` file

2. **"Module not found: perplexityai"**
   - Solution: Run `pip install -r requirements.txt`

3. **Rate limit exceeded**
   - Solution: Wait a moment and retry, or upgrade your Perplexity API plan

### **📚 Resources**

- [Perplexity API Documentation](https://docs.perplexity.ai/)
- [API Quickstart Guide](https://docs.perplexity.ai/guides/perplexity-sdk)
- [Search API Guide](https://docs.perplexity.ai/guides/search-guide)
- [Location Filter Guide](https://docs.perplexity.ai/guides/user-location-filter-guide)

---

## 🗄️ **Database**

Rajniti now includes PostgreSQL support for future data storage needs.

### **Setup with Docker**

```bash
# Start both API and PostgreSQL
docker-compose up -d

# PostgreSQL will be available at:
# - Host: localhost
# - Port: 5432
# - Database: rajniti
# - User: rajniti
# - Password: rajniti_dev_password
```

### **Local Development**

```bash
# Install PostgreSQL locally or use Docker
docker run -d \
  --name rajniti-postgres \
  -e POSTGRES_USER=rajniti \
  -e POSTGRES_PASSWORD=rajniti_dev_password \
  -e POSTGRES_DB=rajniti \
  -p 5432:5432 \
  postgres:16-alpine

# Set DATABASE_URL in your environment
export DATABASE_URL="postgresql://rajniti:rajniti_dev_password@localhost:5432/rajniti"

# Start the app
python run.py
```

### **Database Health Check**

Check database connectivity via the health endpoint:

```bash
curl http://localhost:8080/api/v1/health
```

Response with database connected:

```json
{
    "success": true,
    "message": "Rajniti API is healthy",
    "version": "1.0.0",
    "database": {
        "connected": true,
        "status": "healthy"
    }
}
```

**Note:** The application works perfectly fine without a database configured. Database support is optional and ready for future schema implementation.

## 🔍 **Perplexity AI Search Integration**

Rajniti integrates with Perplexity AI API to provide powerful, India-focused search capabilities for political information, election data, and news.

### **🚀 Quick Setup**

1. **Get Your API Key**

    - Sign up at [Perplexity AI](https://www.perplexity.ai/)
    - Navigate to API settings and generate your API key
    - Free tier available for testing

2. **Configure Environment**

    ```bash
    # Copy example env file
    cp .env.example .env

    # Edit .env and add your API key
    PERPLEXITY_API_KEY=your-actual-api-key-here
    ```

3. **Install Dependencies**
    ```bash
    # Install/update requirements
    pip install -r requirements.txt
    ```

### **✨ Features**

-   🇮🇳 **India-Focused**: Automatically filters search results for Indian context
-   🎯 **Region-Specific**: Support for state/city-level searches (e.g., Delhi, Maharashtra)
-   🔍 **Real-time Search**: Access latest political news and election information
-   🌐 **Web Search**: Leverages Perplexity's AI-powered web search
-   📚 **Citations**: Returns sources for all information
-   ⚡ **Fast & Reliable**: Built-in error handling and retries

### **💻 Usage Examples**

#### **Basic Python Usage**

```python
from app.services.perplexity_service import PerplexityService

# Initialize service (reads PERPLEXITY_API_KEY from environment)
service = PerplexityService()

# Simple search with India filter
results = service.search("Latest election results in India 2025")
print(results['answer'])
print(results['citations'])

# Region-specific search
results = service.search_india(
    query="political news today",
    region="Delhi",
    city="New Delhi"
)

# Multiple queries at once
queries = [
    "Lok Sabha election 2024 results",
    "Delhi Assembly election 2025 results"
]
results = service.search_multiple_queries(queries)
```

#### **Test the Integration**

Run the included test script to verify your setup:

```bash
# Set your API key
export PERPLEXITY_API_KEY='your-api-key-here'

# Run test script
python scripts/test_perplexity.py
```

Expected output:

```
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
Perplexity API Integration Test
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀

🔍 Testing Basic India Search...
✅ Perplexity service initialized successfully
📝 Query: Latest election results in India 2025
✅ Search completed successfully!
```

### **⚙️ Advanced Configuration**

#### **Custom Location Filters**

```python
# Specific location with coordinates
location = {
    "country": "IN",
    "region": "Maharashtra",
    "city": "Mumbai",
    "latitude": 19.0760,
    "longitude": 72.8777
}
results = service.search("local political events", location=location)
```

#### **Multiple Regions**

```python
# Search across different regions
regions = ["Delhi", "Maharashtra", "Karnataka"]
for region in regions:
    results = service.search_india(
        "election updates",
        region=region
    )
    print(f"{region}: {results['answer'][:200]}...")
```

### **🔌 API Models**

Perplexity supports different models:

-   **sonar**: Standard model, optimized for search (default, recommended)
-   **sonar-pro**: Advanced model with higher accuracy (requires pro plan)

### **📝 Response Format**

```python
{
    "query": "Your search query",
    "answer": "AI-generated answer based on search results",
    "citations": ["https://source1.com", "https://source2.com", ...],
    "model": "sonar",
    "location": {"country": "IN"}
}
```

### **🔐 Security Notes**

-   **Never commit** your API key to git
-   Use `.env` files for local development
-   Use environment variables for production deployment
-   The `.env.example` file shows the format but doesn't contain real keys

### **💡 Use Cases**

-   **Election Research**: Search for latest election results and analysis
-   **Political News**: Get India-focused political news and updates
-   **Candidate Information**: Research candidates across different elections
-   **Party Performance**: Analyze party performance in different regions
-   **Policy Updates**: Track government policy changes and announcements

### **🐛 Troubleshooting**

#### API Key Issues

```bash
# Check if API key is set
echo $PERPLEXITY_API_KEY

# Verify .env file exists and has correct format
cat .env | grep PERPLEXITY_API_KEY
```

#### Common Errors

1. **"Perplexity API key not provided"**

    - Solution: Set `PERPLEXITY_API_KEY` environment variable or add to `.env` file

2. **"Module not found: perplexityai"**

    - Solution: Run `pip install -r requirements.txt`

3. **Rate limit exceeded**
    - Solution: Wait a moment and retry, or upgrade your Perplexity API plan

### **📚 Resources**

-   [Perplexity API Documentation](https://docs.perplexity.ai/)
-   [API Quickstart Guide](https://docs.perplexity.ai/guides/perplexity-sdk)
-   [Search API Guide](https://docs.perplexity.ai/guides/search-guide)
-   [Location Filter Guide](https://docs.perplexity.ai/guides/user-location-filter-guide)

---

## 🚢 **Deployment**

### **Docker Deployment**

```yaml
# docker-compose.yml
version: "3.8"
services:
    postgres:
        image: postgres:16-alpine
        environment:
            - POSTGRES_USER=rajniti
            - POSTGRES_PASSWORD=rajniti_dev_password
            - POSTGRES_DB=rajniti
        ports:
            - "5432:5432"
        volumes:
            - postgres_data:/var/lib/postgresql/data

    rajniti-api:
        build: .
        ports:
            - "8080:8080"
        environment:
            - FLASK_ENV=production
            - SECRET_KEY=${SECRET_KEY}
            - DATABASE_URL=postgresql://rajniti:rajniti_dev_password@postgres:5432/rajniti
        volumes:
            - ./app/data:/app/app/data:ro
        depends_on:
            - postgres

volumes:
    postgres_data:
```

```bash
# Deploy to production
docker-compose -f docker-compose.prod.yml up -d
```

### **Cloud Deployment**

#### **Heroku**

```bash
# Install Heroku CLI and login
heroku create your-rajniti-api
git push heroku main
```

#### **AWS/Digital Ocean**

```bash
# Build and push to container registry
docker build -t rajniti-api .
docker tag rajniti-api your-registry/rajniti-api
docker push your-registry/rajniti-api
```

---

## 🧪 **Testing & Development**

### **Dependency Management (pip-compile)**

```bash
# Install pip-tools
pip install pip-tools

# Add new dependency to requirements.in
echo "new-package==1.0.0" >> requirements.in

# Compile dependencies
pip-compile requirements.in

# Install compiled dependencies
pip-sync requirements.txt

# Or upgrade all
pip-compile --upgrade requirements.in
```

### **Running Tests**

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Format code
black app/
isort app/
flake8 app/
```

## 📈 **Performance & Scalability**

### **Performance Features**

-   **Fast Startup**: Minimal dependencies, quick boot time
-   **JSON Serving**: Direct file-based data serving
-   **Simple Search**: Basic filtering and search capabilities
-   **Memory Efficient**: Low memory footprint
-   **Stateless**: No database dependencies

---

## 🤝 **Contributing**

We welcome contributions! Here's how to get started:

### **Development Setup**

```bash
# Fork and clone
git clone https://github.com/your-username/rajniti.git
cd rajniti

# Create feature branch
git checkout -b feature/amazing-feature

# Install dependencies using pip-compile
pip install pip-tools
pip-sync requirements.txt

# Make your changes and test
pytest tests/

# Submit pull request
git push origin feature/amazing-feature
```

### **Contribution Guidelines**

-   🐛 **Bug Reports**: Use GitHub issues with detailed descriptions
-   ✨ **Feature Requests**: Discuss in issues before implementing
-   📝 **Documentation**: Update docs for any API changes
-   ✅ **Testing**: Ensure tests pass and add new tests
-   🎨 **Code Style**: Follow Black formatting and PEP 8

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

-   **Election Commission of India** for providing comprehensive election data
-   **Flask Community** for the excellent web framework
-   **Contributors** who helped make this project possible

---

## 📞 **Support & Community**

<div align="center">

[![GitHub Issues](https://img.shields.io/badge/Issues-GitHub-red.svg)](https://github.com/your-username/rajniti/issues)
[![Discussions](https://img.shields.io/badge/Discussions-GitHub-blue.svg)](https://github.com/your-username/rajniti/discussions)
[![Email](https://img.shields.io/badge/Email-Contact-green.svg)](mailto:rajniti@example.com)

**⭐ Star this repository if you find it helpful!**

</div>

---

<div align="center">

**Built with ❤️ for 🇮🇳 Democracy**

_Empowering citizens, researchers, and developers with accessible election data_

</div>
