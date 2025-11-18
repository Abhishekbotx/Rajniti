'use client'

import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

// API Base URL - configurable via environment variable
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"

export function useOnboardingCheck(redirectIfIncomplete: boolean = true) {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [isOnboarded, setIsOnboarded] = useState<boolean | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function checkOnboarding() {
      if (status === 'loading') {
        return
      }

      if (status === 'unauthenticated') {
        setLoading(false)
        setIsOnboarded(false)
        return
      }

      if (!session) {
        setLoading(false)
        return
      }

      try {
        // Call backend API to check onboarding status
        const headers: HeadersInit = {
          'Content-Type': 'application/json',
        }
        
        // Add backend token if available
        if (session.backendToken) {
          headers['Authorization'] = `Bearer ${session.backendToken}`
        }
        
        const response = await fetch(`${API_BASE_URL}/auth/me`, {
          headers
        })

        if (response.ok) {
          const data = await response.json()
          const onboarded = data.data?.onboarding_completed || false
          setIsOnboarded(onboarded)

          // Redirect to onboarding if not completed
          if (!onboarded && redirectIfIncomplete) {
            router.push('/onboarding')
          }
        } else {
          setIsOnboarded(false)
          // If not onboarded and redirectIfIncomplete, go to onboarding
          if (redirectIfIncomplete) {
            router.push('/onboarding')
          }
        }
      } catch (error) {
        console.error('Error checking onboarding status:', error)
        setIsOnboarded(false)
        // On error, assume not onboarded and redirect if needed
        if (redirectIfIncomplete) {
          router.push('/onboarding')
        }
      } finally {
        setLoading(false)
      }
    }

    checkOnboarding()
  }, [session, status, redirectIfIncomplete, router])

  return { isOnboarded, loading }
}
