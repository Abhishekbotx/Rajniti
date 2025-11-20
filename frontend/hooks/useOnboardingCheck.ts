"use client"

import { useSession } from "next-auth/react"
import { useRouter } from "next/navigation"
import { useEffect, useState } from "react"

export function useOnboardingCheck(redirectIfIncomplete: boolean = true) {
    const { data: session, status } = useSession()
    const router = useRouter()
    const [isOnboarded, setIsOnboarded] = useState<boolean | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (status === "loading") {
            return
        }

        if (status === "unauthenticated") {
            setLoading(false)
            setIsOnboarded(false)
            return
        }

        if (status === "authenticated" && session?.user) {
            // Use the onboarding status directly from the session
            // This is populated by the NextAuth callback during login
            const onboarded = session.user.onboardingCompleted || false
            setIsOnboarded(onboarded)
            setLoading(false)

            if (!onboarded && redirectIfIncomplete) {
                router.push("/onboarding")
            }
        }
    }, [session, status, redirectIfIncomplete, router])

    return { isOnboarded, loading }
}
