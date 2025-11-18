# User Onboarding Flow

## Overview
This document describes the complete user onboarding flow implemented in the Rajniti application.

## Onboarding Steps

### Step 1: Political Inclination (Single Select)
User selects their political inclination:
- **Rightist**: Conservative, traditional values, free market economy
- **Leftist**: Progressive, social equality, welfare policies
- **Communist**: Collective ownership, socialist principles
- **Centrist**: Moderate, balanced approach to politics
- **Libertarian**: Individual liberty, minimal government intervention
- **Neutral/Apolitical**: No strong political alignment

### Step 2: Username (Unique)
User chooses a unique username:
- Minimum 3 characters
- Alphanumeric and underscores only
- Real-time availability check via API
- Lowercase only
- Visual feedback for availability

### Step 3: User Details
User provides basic information:
- **Phone**: Optional, for contact
- **State**: Required, dropdown with all Indian states
- **City**: Optional
- **Age Group**: Required (18-25, 26-35, 36-50, 51-65, 65+)

### Step 4: Preferences
User selects their political preferences:
- **Preferred Parties**: Multi-select from major Indian political parties
- **Topics of Interest**: Multi-select from political topics (Economy, Healthcare, Education, etc.)

## Backend API Integration

### Check Username Availability
```
POST /api/v1/auth/check-username
Authorization: Bearer <token>

Request:
{
  "username": "johndoe"
}

Response:
{
  "success": true,
  "available": true/false
}
```

### Complete Onboarding
```
POST /api/v1/auth/onboarding
Authorization: Bearer <token>

Request:
{
  "political_interest": "Rightist",
  "username": "johndoe",
  "phone": "+91-9876543210",
  "state": "Delhi",
  "city": "New Delhi",
  "age_group": "26-35",
  "preferred_parties": ["Bharatiya Janata Party", "Indian National Congress"],
  "topics_of_interest": ["Economy", "Healthcare", "Education"]
}

Response:
{
  "success": true,
  "data": {
    "id": "user_id",
    "email": "user@example.com",
    "username": "johndoe",
    "onboarding_completed": true,
    ...
  },
  "message": "Onboarding completed successfully"
}
```

### Get User Status
```
GET /api/v1/auth/me
Authorization: Bearer <token>

Response:
{
  "success": true,
  "data": {
    "id": "user_id",
    "email": "user@example.com",
    "onboarding_completed": true/false,
    ...
  }
}
```

## Database Schema

### User Model Fields
- `id` (String, Primary Key): Google user ID
- `email` (String, Unique): User email
- `name` (String): Full name
- `username` (String, Unique, Indexed): Chosen username
- `profile_picture` (String): Profile picture URL
- `phone` (String): Phone number
- `state` (String): State of residence
- `city` (String): City
- `age_group` (String): Age bracket
- `political_interest` (String): Interest level
- `preferred_parties` (Text): Comma-separated parties
- `topics_of_interest` (Text): Comma-separated topics
- `onboarding_completed` (Boolean): Completion status
- `created_at` (DateTime): Account creation
- `updated_at` (DateTime): Last update
- `last_login` (DateTime): Last login time

## Onboarding Check Middleware

The `useOnboardingCheck` hook automatically:
1. Checks authentication status
2. Fetches user data from `/api/v1/auth/me`
3. Checks `onboarding_completed` flag
4. Redirects to `/onboarding` if not completed

### Usage in Protected Pages
```tsx
import { useOnboardingCheck } from '@/hooks/useOnboardingCheck'

export default function Dashboard() {
  // Will redirect to /onboarding if not completed
  const { isOnboarded, loading } = useOnboardingCheck(true)
  
  if (loading) {
    return <LoadingSpinner />
  }
  
  // Rest of component...
}
```

## User Flow Diagram

```
1. User signs in with Google
   ↓
2. Check onboarding_completed
   ↓
3a. If true → Dashboard
3b. If false → Onboarding Page
   ↓
4. Complete 4-step onboarding
   ↓
5. Submit to /api/v1/auth/onboarding
   ↓
6. Redirect to Dashboard
```

## Design Principles

1. **Smooth and Simple**: Clear progress indicator, one step at a time
2. **Seamless**: Auto-save on completion, skip option available
3. **Reusable Components**: Each step is a separate, reusable component
4. **Validation**: Real-time validation with visual feedback
5. **Accessibility**: Keyboard navigation, clear labels, error messages
6. **Responsive**: Works on mobile, tablet, and desktop
