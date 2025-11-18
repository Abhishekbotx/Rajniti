'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'
import PoliticalInclinationStep from '@/components/onboarding/PoliticalInclinationStep'
import UsernameStep from '@/components/onboarding/UsernameStep'
import UserDetailsStep from '@/components/onboarding/UserDetailsStep'
import PreferencesStep from '@/components/onboarding/PreferencesStep'

export default function Onboarding() {
  const router = useRouter()
  const [step, setStep] = useState(1)
  const [loading, setLoading] = useState(false)
  const [usernameValid, setUsernameValid] = useState(false)
  
  const [formData, setFormData] = useState({
    political_interest: '',
    username: '',
    phone: '',
    state: '',
    city: '',
    age_group: '',
    preferred_parties: [] as string[],
    topics_of_interest: [] as string[]
  })

  const updateField = (field: string, value: string | string[]) => {
    setFormData({
      ...formData,
      [field]: value
    })
  }

  const canProceedToNextStep = () => {
    switch (step) {
      case 1:
        return formData.political_interest !== ''
      case 2:
        return formData.username !== '' && usernameValid
      case 3:
        return formData.state !== '' && formData.age_group !== ''
      case 4:
        return true // Preferences are optional
      default:
        return false
    }
  }

  const handleSubmit = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/v1/auth/onboarding', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add authentication token from session
        },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        router.push('/dashboard')
      } else {
        const error = await response.json()
        alert(error.error || 'Failed to complete onboarding')
      }
    } catch (error) {
      console.error('Onboarding failed:', error)
      alert('Failed to complete onboarding. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const totalSteps = 4

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-green-50 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Progress bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Step {step} of {totalSteps}</span>
            <span className="text-sm text-gray-500">
              {step === 1 && 'Political Inclination'}
              {step === 2 && 'Username'}
              {step === 3 && 'Basic Details'}
              {step === 4 && 'Preferences'}
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-orange-500 to-green-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${(step / totalSteps) * 100}%` }}
            />
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8 border border-orange-100">
          {/* Step 1: Political Inclination */}
          {step === 1 && (
            <PoliticalInclinationStep
              value={formData.political_interest}
              onChange={(value) => updateField('political_interest', value)}
            />
          )}

          {/* Step 2: Username */}
          {step === 2 && (
            <UsernameStep
              value={formData.username}
              onChange={(value) => updateField('username', value)}
              onValidation={setUsernameValid}
            />
          )}

          {/* Step 3: Basic Details */}
          {step === 3 && (
            <UserDetailsStep
              formData={{
                phone: formData.phone,
                state: formData.state,
                city: formData.city,
                age_group: formData.age_group
              }}
              onChange={updateField}
            />
          )}

          {/* Step 4: Preferences */}
          {step === 4 && (
            <PreferencesStep
              formData={{
                preferred_parties: formData.preferred_parties,
                topics_of_interest: formData.topics_of_interest
              }}
              onChange={(field, values) => updateField(field, values)}
            />
          )}

          {/* Navigation buttons */}
          <div className="flex gap-4 mt-8">
            {step > 1 && (
              <button
                onClick={() => setStep(step - 1)}
                className="flex-1 px-6 py-3 border-2 border-gray-300 rounded-lg text-gray-700 font-semibold hover:bg-gray-50 transition-all"
              >
                Back
              </button>
            )}
            
            {step < totalSteps ? (
              <button
                onClick={() => setStep(step + 1)}
                disabled={!canProceedToNextStep()}
                className="flex-1 px-6 py-3 bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg text-white font-semibold hover:from-orange-600 hover:to-orange-700 transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Continue
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="flex-1 px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 rounded-lg text-white font-semibold hover:from-green-600 hover:to-green-700 transition-all shadow-lg disabled:opacity-50"
              >
                {loading ? 'Saving...' : 'Complete Onboarding'}
              </button>
            )}
          </div>
        </div>

        {/* Skip button */}
        <div className="text-center mt-6">
          <button 
            onClick={() => router.push('/dashboard')}
            className="text-gray-500 hover:text-gray-700 font-medium"
          >
            Skip for now →
          </button>
        </div>
      </div>
    </div>
  )
}
