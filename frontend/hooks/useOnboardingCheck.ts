'use client'

import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

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
        const response = await fetch('/api/v1/auth/me', {
          headers: {
            'Content-Type': 'application/json',
            // Add authentication token from session
          }
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
        }
      } catch (error) {
        console.error('Error checking onboarding status:', error)
        setIsOnboarded(false)
      } finally {
        setLoading(false)
      }
    }

    checkOnboarding()
  }, [session, status, redirectIfIncomplete, router])

  return { isOnboarded, loading }
}
