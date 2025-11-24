import { useState, useEffect } from "react"

const API_BASE_URL =
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"

interface Candidate {
    id: string
    name: string
    party_name: string
    party_short_name: string
    party_symbol?: string
    constituency_name: string
    constituency_id: string
    state_id: string
    status: string
    type: string
    image_url?: string
    election_id: string
    education_background?: Array<{
        year?: string
        college?: string
        stream?: string
        other_details?: string
    }>
    political_background?: Array<{
        party?: string
        constituency?: string
        election_year?: string
        position?: string
        result?: string
    }>
    family_background?: Array<{
        name?: string
        profession?: string
        relation?: string
        age?: string
    }>
    assets?: Array<{
        type?: string
        amount?: number
        description?: string
        owned_by?: string
    }>
    liabilities?: Array<{
        type?: string
        amount?: number
        description?: string
        owned_by?: string
    }>
    crime_cases?: Array<{
        fir_no?: string
        police_station?: string
        sections_applied?: string[]
        charges_framed?: boolean
        description?: string
    }>
}

export function useCandidate(candidateId: string | null) {
    const [candidate, setCandidate] = useState<Candidate | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!candidateId) {
            setLoading(false)
            return
        }

        const fetchCandidate = async () => {
            try {
                setLoading(true)
                const response = await fetch(
                    `${API_BASE_URL}/candidates/${candidateId}`
                )
                const data = await response.json()
                if (data.success) {
                    setCandidate(data.data)
                    setError(null)
                } else {
                    setError(data.error || "Failed to load candidate")
                }
            } catch (err) {
                setError("Error connecting to API")
                console.error("Error fetching candidate:", err)
            } finally {
                setLoading(false)
            }
        }

        fetchCandidate()
    }, [candidateId])

    return { candidate, loading, error }
}

export function useSearchCandidates() {
    const [candidates, setCandidates] = useState<Candidate[]>([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const search = async (query: string, limit: number = 10) => {
        if (!query.trim()) {
            setCandidates([])
            return
        }

        try {
            setLoading(true)
            const response = await fetch(
                `${API_BASE_URL}/candidates/search?q=${encodeURIComponent(
                    query
                )}&limit=${limit}`
            )
            const data = await response.json()
            if (data.success) {
                setCandidates(data.data.candidates || [])
                setError(null)
            } else {
                setError(data.error || "Failed to search candidates")
            }
        } catch (err) {
            setError("Error connecting to API")
            console.error("Error searching candidates:", err)
        } finally {
            setLoading(false)
        }
    }

    const clear = () => {
        setCandidates([])
        setError(null)
    }

    return { candidates, loading, error, search, clear }
}
