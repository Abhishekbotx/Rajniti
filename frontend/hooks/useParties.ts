import { useState, useEffect } from "react"

const API_BASE_URL =
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"

interface Party {
    name: string
    short_name: string
    seats_won?: number
    symbol?: string
}

export function useParties(electionId: string | null) {
    const [parties, setParties] = useState<Party[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!electionId) {
            setLoading(false)
            return
        }

        const fetchParties = async () => {
            try {
                setLoading(true)
                const response = await fetch(
                    `${API_BASE_URL}/elections/${electionId}/parties`
                )
                const data = await response.json()
                if (data.success && data.data.parties) {
                    const mappedParties = data.data.parties.slice(0, 10).map((p: any) => ({
                        name: p.name,
                        short_name: p.short_name,
                        seats_won: p.seats_won,
                        symbol: p.symbol
                    }))
                    setParties(mappedParties)
                    setError(null)
                } else {
                    setError(data.error || "Failed to load parties")
                }
            } catch (err) {
                setError("Error connecting to API")
                console.error("Error fetching parties:", err)
            } finally {
                setLoading(false)
            }
        }

        fetchParties()
    }, [electionId])

    return { parties, loading, error }
}
