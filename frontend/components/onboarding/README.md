# Onboarding Components

This directory contains reusable components for the user onboarding flow.

## Components

### PoliticalInclinationStep
Single-select component for choosing political interest level.
- **Props**: 
  - `value`: Current selected value
  - `onChange`: Callback when selection changes
- **Options**: Rightist, Leftist, Communist, Centrist, Libertarian, Neutral

### UsernameStep
Component for entering and validating a unique username.
- **Props**:
  - `value`: Current username value
  - `onChange`: Callback when username changes
  - `onValidation`: Callback with validation status
- **Features**:
  - Real-time validation
  - Debounced API calls (500ms)
  - Visual feedback (loading, success, error)
  - Format validation (alphanumeric + underscores)
  - Minimum 3 characters

### UserDetailsStep
Component for collecting basic user information.
- **Props**:
  - `formData`: Object with phone, state, city, age_group
  - `onChange`: Callback when any field changes
- **Fields**:
  - Phone (optional)
  - State (required, dropdown with all Indian states)
  - City (optional)
  - Age Group (required, button selection)

### PreferencesStep
Multi-select component for political preferences.
- **Props**:
  - `formData`: Object with preferred_parties and topics_of_interest arrays
  - `onChange`: Callback when selections change
- **Features**:
  - Party selection (multi-select)
  - Topics of interest (multi-select)
  - Visual feedback for selections

## Usage

```tsx
import PoliticalInclinationStep from '@/components/onboarding/PoliticalInclinationStep'
import UsernameStep from '@/components/onboarding/UsernameStep'
import UserDetailsStep from '@/components/onboarding/UserDetailsStep'
import PreferencesStep from '@/components/onboarding/PreferencesStep'

// In your component
const [formData, setFormData] = useState({
  political_interest: '',
  username: '',
  phone: '',
  state: '',
  city: '',
  age_group: '',
  preferred_parties: [],
  topics_of_interest: []
})

<PoliticalInclinationStep
  value={formData.political_interest}
  onChange={(value) => setFormData({ ...formData, political_interest: value })}
/>
```

## Styling
All components use Tailwind CSS with the project's design system:
- Orange accent color for primary actions
- Green accent color for topics/success states
- Consistent border-radius and shadows
- Responsive design with mobile-first approach
