# User Authentication & Onboarding

This document describes the user authentication and onboarding system implemented in Rajniti.

## Overview

Rajniti now includes a complete user authentication system with:

-   **Google OAuth** for secure sign-in
-   **User profiles** with basic details
-   **Political preferences** collection
-   **Onboarding flow** for new users

## Features

### Authentication

-   ✅ Google OAuth integration
-   ✅ Secure JWT token-based authentication
-   ✅ Session management with NextAuth.js
-   ✅ Protected routes and API endpoints

### User Profile

Users can provide:

-   Basic information (name, email, phone)
-   Location (state, city)
-   Demographics (age group)
-   Political interest level
-   Preferred political parties
-   Topics of interest

## Backend Setup

### 1. Environment Variables

Add the following to your `.env` file:

```bash
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Frontend URL (for OAuth redirects)
FRONTEND_URL=http://localhost:3000

# Secret key for JWT tokens
SECRET_KEY=your-secret-key-change-in-production
```

### 2. Get Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Configure the consent screen
6. Set authorized redirect URIs:
    - `http://localhost:3000/api/auth/callback/google` (development)
    - `https://yourdomain.com/api/auth/callback/google` (production)
7. Copy the **Client ID** and **Client Secret**

### 3. Database Migration

The user table is created automatically when you start the server. The migration includes:

-   User authentication fields (id, email)
-   Profile information (name, profile_picture, phone, state, city, age_group)
-   Political preferences (political_interest, preferred_parties, topics_of_interest)
-   Onboarding status tracking
-   Timestamps (created_at, updated_at, last_login)

To manually run migrations:

```bash
# Set DATABASE_URL if not already set
export DATABASE_URL="postgresql://user:password@localhost:5432/rajniti"

# Run migrations
alembic upgrade head
```

### 4. API Endpoints

#### Authentication

**POST /api/v1/auth/google/login**

-   Initiates Google OAuth flow
-   Redirects to Google consent screen

**GET /api/v1/auth/google/callback**

-   Handles OAuth callback
-   Creates or updates user
-   Returns JWT token
-   Redirects to frontend with token

**POST /api/v1/auth/logout**

-   Logs out user (client-side token removal)
-   Requires authentication

**GET /api/v1/auth/me**

-   Returns current user information
-   Requires authentication

**PUT /api/v1/auth/profile**

-   Updates user profile
-   Requires authentication
-   Request body:
    ```json
    {
        "name": "John Doe",
        "phone": "+91-9876543210",
        "state": "Delhi",
        "city": "New Delhi",
        "age_group": "26-35"
    }
    ```

**POST /api/v1/auth/onboarding**

-   Completes user onboarding
-   Requires authentication
-   Request body:
    ```json
    {
        "phone": "+91-9876543210",
        "state": "Delhi",
        "city": "New Delhi",
        "age_group": "26-35",
        "political_interest": "Rightist",
        "preferred_parties": [
            "Bharatiya Janata Party",
            "Indian National Congress"
        ],
        "topics_of_interest": ["Economy", "Healthcare", "Education"]
    }
    ```

**GET /api/v1/auth/health**

-   Checks authentication service health
-   Returns OAuth configuration status

## Frontend Setup

### 1. Environment Variables

Create a `.env.local` file in the `frontend` directory:

```bash
# NextAuth Configuration
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=generate-with-openssl-rand-base64-32

# Google OAuth (same as backend)
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Generate NEXTAUTH_SECRET:

```bash
openssl rand -base64 32
```

### 2. Pages

**Sign In Page** (`/auth/signin`)

-   Google OAuth login button
-   Redirects to onboarding after first login
-   Redirects to dashboard for returning users

**Onboarding Page** (`/onboarding`)

-   Two-step form:
    1. Basic details (phone, location, age)
    2. Political preferences (parties, topics)
-   Can be skipped and completed later
-   Protected route (requires authentication)

**Dashboard** (`/dashboard`)

-   Main user dashboard
-   Shows personalized content based on preferences

### 3. Components

**AuthProvider** (`components/auth/AuthProvider.tsx`)

-   Wraps app with NextAuth session provider
-   Provides authentication context

**UserButton** (`components/auth/UserButton.tsx`)

-   Shows sign-in button for unauthenticated users
-   Shows user profile dropdown for authenticated users
-   Includes sign-out option

## Usage Examples

### Backend (Python)

```python
from app.services.auth_service import AuthService
from app.database.models import User

auth_service = AuthService()

# Get user from token
user = auth_service.get_user_from_token(jwt_token)

# Update user profile
updated_user = auth_service.update_user_profile(
    user_id="google_user_id",
    phone="+91-9876543210",
    state="Delhi"
)

# Complete onboarding
completed_user = auth_service.complete_user_onboarding(
    user_id="google_user_id",
    political_interest="Rightist",
    preferred_parties=["BJP", "INC"],
    topics_of_interest=["Economy", "Healthcare"]
)
```

### Frontend (React/Next.js)

```typescript
import { useSession, signIn, signOut } from "next-auth/react"

function MyComponent() {
    const { data: session, status } = useSession()

    if (status === "loading") {
        return <div>Loading...</div>
    }

    if (status === "unauthenticated") {
        return <button onClick={() => signIn("google")}>Sign In</button>
    }

    return (
        <div>
            <p>Welcome, {session.user.name}!</p>
            <button onClick={() => signOut()}>Sign Out</button>
        </div>
    )
}
```

### Protected Routes

```typescript
import { getServerSession } from "next-auth/next"

export async function GET(request: Request) {
    const session = await getServerSession()

    if (!session) {
        return new Response("Unauthorized", { status: 401 })
    }

    // Handle authenticated request
    return Response.json({ user: session.user })
}
```

## Security Considerations

### Token Security

-   JWT tokens expire after 24 hours
-   Tokens are stored client-side (localStorage/sessionStorage)
-   HTTPS required in production
-   Tokens include user ID and email only (no sensitive data)

### OAuth Security

-   Google OAuth provides secure authentication
-   User consent required for profile access
-   Callback URLs must be whitelisted
-   Client secrets must be kept secure

### Best Practices

1. **Always use HTTPS** in production
2. **Keep secrets secure** - never commit to git
3. **Validate all inputs** on both client and server
4. **Use environment variables** for configuration
5. **Implement rate limiting** on auth endpoints
6. **Log authentication events** for security monitoring

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,              -- Google user ID
    email VARCHAR UNIQUE NOT NULL,       -- User email
    name VARCHAR,                        -- Full name
    profile_picture VARCHAR,             -- Profile photo URL
    phone VARCHAR,                       -- Phone number
    state VARCHAR,                       -- State of residence
    city VARCHAR,                        -- City of residence
    age_group VARCHAR,                   -- Age group (18-25, 26-35, etc.)
    political_interest VARCHAR,          -- Rightist, Leftist, Communist, Centrist, Libertarian, Neutral
    preferred_parties TEXT,              -- Comma-separated party names
    topics_of_interest TEXT,             -- Comma-separated topics
    onboarding_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

## Testing

### Manual Testing

1. **Sign In Flow**

    ```bash
    # Start backend
    cd /home/runner/work/rajniti/rajniti
    python run.py

    # Start frontend (in another terminal)
    cd frontend
    npm run dev

    # Visit http://localhost:3000
    # Click "Sign In" button
    # Complete Google OAuth
    # Verify redirect to onboarding
    ```

2. **Onboarding Flow**

    ```bash
    # After signing in
    # Fill in basic details
    # Click "Continue"
    # Select political preferences
    # Click "Complete Onboarding"
    # Verify redirect to dashboard
    ```

3. **API Testing**
    ```bash
    # Get auth token from browser console
    # Test protected endpoint
    curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
         http://localhost:8000/api/v1/auth/me
    ```

## Troubleshooting

### Common Issues

1. **"Google OAuth not configured"**

    - Solution: Set `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` environment variables

2. **"Redirect URI mismatch"**

    - Solution: Add the correct redirect URI in Google Cloud Console

3. **"Database connection failed"**

    - Solution: Ensure PostgreSQL is running and `DATABASE_URL` is set correctly

4. **"NextAuth session not found"**

    - Solution: Ensure `NEXTAUTH_SECRET` is set and matches between requests

5. **"CORS error"**
    - Solution: Ensure `FRONTEND_URL` is set correctly in backend `.env`

## Future Enhancements

Potential improvements:

-   [ ] Email/password authentication
-   [ ] Two-factor authentication
-   [ ] Social login (Twitter, Facebook)
-   [ ] User preferences dashboard
-   [ ] Email notifications
-   [ ] User analytics
-   [ ] Admin panel
-   [ ] Role-based access control

## Support

For issues or questions:

-   Check this documentation
-   Review environment variable configuration
-   Check logs in backend and frontend
-   Create an issue on GitHub
