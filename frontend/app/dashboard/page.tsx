"use client"

import { useState, useEffect } from "react"
import { useOnboardingCheck } from "@/hooks/useOnboardingCheck"
import { Navbar } from "@/components/layout"
import Button from "@/components/ui/Button"
import Text from "@/components/ui/Text"
import Image from "@/components/ui/Image"

// Types for our API data
interface Election {
    id: string
    name: string
    year: number
    type: string
    statistics: {
        total_candidates: number
        total_constituencies: number
        total_parties: number
        total_winners: number
    }
}

interface Candidate {
    id: string
    name: string
    party_name: string
    party_short_name: string
    constituency_name: string
    status: string
    image_url?: string
}

interface Party {
    party_name: string
    party_short_name: string
    total_seats?: number
    party_symbol?: string
}

// API Base URL - configurable via environment variable
const API_BASE_URL =
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"

export default function Dashboard() {
    // Check onboarding status and redirect if not completed
    const { loading: onboardingLoading } = useOnboardingCheck(true)
    
    const [selectedElection, setSelectedElection] = useState<Election | null>(
        null
    )
    const [candidates, setCandidates] = useState<Candidate[]>([])
    const [parties, setParties] = useState<Party[]>([])
    const [searchQuery, setSearchQuery] = useState("")
    const [loading, setLoading] = useState(true)
    const [searchLoading, setSearchLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    // Fetch elections on component mount
    useEffect(() => {
        fetchElections()
    }, [])

    // Fetch parties when election is selected
    useEffect(() => {
        if (selectedElection) {
            fetchParties(selectedElection.id)
        }
    }, [selectedElection])

    const fetchElections = async () => {
        try {
            setLoading(true)
            const response = await fetch(`${API_BASE_URL}/elections`)
            const data = await response.json()
            if (data.success) {
                if (data.data.length > 0) {
                    setSelectedElection(data.data[0])
                }
            } else {
                setError("Failed to load elections")
            }
        } catch (err) {
            setError(
                "Error connecting to API. Make sure the backend is running on port 8000."
            )
            console.error("Error fetching elections:", err)
        } finally {
            setLoading(false)
        }
    }

    const fetchParties = async (electionId: string) => {
        try {
            const response = await fetch(
                `${API_BASE_URL}/elections/${electionId}/parties`
            )
            const data = await response.json()
            if (data.success && data.data.parties) {
                // Map the API response to our Party interface
                interface PartyApiResponse {
                    name: string
                    short_name: string
                    seats_won: number
                    symbol: string
                }
                const mappedParties = data.data.parties
                    .slice(0, 10)
                    .map((p: PartyApiResponse) => ({
                        party_name: p.name,
                        party_short_name: p.short_name,
                        total_seats: p.seats_won,
                        party_symbol: p.symbol
                    }))
                setParties(mappedParties)
            }
        } catch (err) {
            console.error("Error fetching parties:", err)
        }
    }

    const searchCandidates = async (query: string) => {
        if (!query.trim()) {
            setCandidates([])
            return
        }

        try {
            setSearchLoading(true)
            const response = await fetch(
                `${API_BASE_URL}/candidates/search?q=${encodeURIComponent(
                    query
                )}&limit=10`
            )
            const data = await response.json()
            if (data.success) {
                setCandidates(data.data.candidates || [])
            }
        } catch (err) {
            console.error("Error searching candidates:", err)
        } finally {
            setSearchLoading(false)
        }
    }

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault()
        searchCandidates(searchQuery)
    }

    // Show loading while checking onboarding status
    if (onboardingLoading) {
        return (
            <div className='min-h-screen bg-gradient-to-b from-orange-50 via-white to-green-50 flex items-center justify-center'>
                <div className='text-center'>
                    <div className='inline-block animate-spin rounded-full h-16 w-16 border-4 border-orange-500 border-t-transparent'></div>
                    <p className='mt-4 text-gray-600 font-semibold'>
                        Loading...
                    </p>
                </div>
            </div>
        )
    }

    if (loading) {
        return (
            <div className='min-h-screen bg-gradient-to-b from-orange-50 via-white to-green-50 flex items-center justify-center'>
                <div className='text-center'>
                    <div className='inline-block animate-spin rounded-full h-16 w-16 border-4 border-orange-500 border-t-transparent'></div>
                    <p className='mt-4 text-gray-600 font-semibold'>
                        Loading Election Data...
                    </p>
                </div>
            </div>
        )
    }

    if (error) {
        return (
            <div className='min-h-screen bg-gradient-to-b from-orange-50 via-white to-green-50 flex items-center justify-center p-4'>
                <div className='bg-white rounded-lg shadow-lg p-8 max-w-md w-full border-l-4 border-red-500'>
                    <div className='flex items-center gap-3 mb-4'>
                        <div className='text-red-500 text-3xl'>⚠️</div>
                        <Text variant="h4" weight="bold" className='text-gray-900'>
                            Connection Error
                        </Text>
                    </div>
                    <Text variant="body" className='text-gray-600 mb-4'>{error}</Text>
                    <Button
                        onClick={fetchElections}
                        fullWidth
                    >
                        Try Again
                    </Button>
                </div>
            </div>
        )
    }

    return (
        <div className='min-h-screen bg-gradient-to-b from-orange-50 via-white to-green-50'>
            <Navbar variant="dashboard" sticky={true} />

            <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8'>
                {/* Election Overview Section */}
                {selectedElection && (
                    <div className='mb-8'>
                        <div className='bg-gradient-to-r from-orange-500 to-orange-600 rounded-2xl p-8 text-white shadow-lg'>
                            <Text variant="h2" weight="bold" className='text-white mb-2'>
                                {selectedElection.name}
                            </Text>
                            <Text variant="body" className='text-orange-100 mb-6'>
                                Year: {selectedElection.year} | Type:{" "}
                                {selectedElection.type}
                            </Text>

                            <div className='grid grid-cols-2 md:grid-cols-4 gap-4'>
                                <div className='bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20'>
                                    <Text variant="h3" weight="bold" className='text-white'>
                                        {
                                            selectedElection.statistics
                                                .total_constituencies
                                        }
                                    </Text>
                                    <Text variant="small" className='text-orange-100 mt-1'>
                                        Constituencies
                                    </Text>
                                </div>
                                <div className='bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20'>
                                    <Text variant="h3" weight="bold" className='text-white'>
                                        {selectedElection.statistics.total_candidates.toLocaleString()}
                                    </Text>
                                    <Text variant="small" className='text-orange-100 mt-1'>
                                        Candidates
                                    </Text>
                                </div>
                                <div className='bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20'>
                                    <Text variant="h3" weight="bold" className='text-white'>
                                        {
                                            selectedElection.statistics
                                                .total_parties
                                        }
                                    </Text>
                                    <Text variant="small" className='text-orange-100 mt-1'>
                                        Parties
                                    </Text>
                                </div>
                                <div className='bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20'>
                                    <Text variant="h3" weight="bold" className='text-white'>
                                        {
                                            selectedElection.statistics
                                                .total_winners
                                        }
                                    </Text>
                                    <Text variant="small" className='text-orange-100 mt-1'>
                                        Winners
                                    </Text>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Search Section */}
                <div className='mb-8'>
                    <div className='bg-white rounded-2xl shadow-lg p-6 border border-gray-200'>
                        <Text variant="h3" weight="bold" className='text-gray-900 mb-4'>
                            🔍 Search Candidates
                        </Text>
                        <form onSubmit={handleSearch} className='flex gap-2'>
                            <input
                                type='text'
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                placeholder='Search by candidate name...'
                                className='flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent'
                            />
                            <Button
                                type='submit'
                                disabled={searchLoading}
                                isLoading={searchLoading}
                                size="lg"
                                className="px-8"
                            >
                                {searchLoading ? "Searching..." : "Search"}
                            </Button>
                        </form>

                        {/* Search Results */}
                        {candidates.length > 0 && (
                            <div className='mt-6 space-y-3'>
                                <Text variant="body" weight="semibold" className='text-gray-700'>
                                    Results ({candidates.length})
                                </Text>
                                <div className='grid gap-3'>
                                    {candidates.map((candidate) => (
                                        <div
                                            key={candidate.id}
                                            className='bg-gradient-to-r from-gray-50 to-white rounded-lg p-4 border border-gray-200 hover:border-orange-300 transition-colors'>
                                            <div className='flex items-center gap-4'>
                                                {candidate.image_url && (
                                                    <Image
                                                        src={candidate.image_url}
                                                        alt={candidate.name}
                                                        width={64}
                                                        height={64}
                                                        rounded="full"
                                                        className='w-16 h-16 object-cover border-2 border-orange-200'
                                                    />
                                                )}
                                                <div className='flex-1'>
                                                    <Text variant="body" weight="bold" className='text-gray-900'>
                                                        {candidate.name}
                                                    </Text>
                                                    <Text variant="small" className='text-gray-600'>
                                                        {candidate.party_name} (
                                                        {
                                                            candidate.party_short_name
                                                        }
                                                        )
                                                    </Text>
                                                    <Text variant="small" className='text-gray-500'>
                                                        {
                                                            candidate.constituency_name
                                                        }
                                                    </Text>
                                                </div>
                                                <div>
                                                    <span
                                                        className={`px-3 py-1 rounded-full text-sm font-semibold ${
                                                            candidate.status ===
                                                            "WON"
                                                                ? "bg-green-100 text-green-700"
                                                                : "bg-gray-100 text-gray-600"
                                                        }`}>
                                                        {candidate.status}
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {searchQuery &&
                            !searchLoading &&
                            candidates.length === 0 && (
                                <div className='mt-6 text-center text-gray-500'>
                                    No candidates found for &quot;{searchQuery}
                                    &quot;
                                </div>
                            )}
                    </div>
                </div>

                {/* Parties Section */}
                {parties.length > 0 && (
                    <div className='mb-8'>
                        <div className='bg-white rounded-2xl shadow-lg p-6 border border-gray-200'>
                            <Text variant="h3" weight="bold" className='text-gray-900 mb-4'>
                                🎯 Major Parties
                            </Text>
                            <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
                                {parties.map((party, index) => (
                                    <div
                                        key={index}
                                        className='bg-gradient-to-br from-orange-50 to-white rounded-lg p-4 border border-orange-200 hover:border-orange-400 transition-colors'>
                                        <div className='flex items-center gap-3'>
                                            <div className='w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 font-bold'>
                                                {party.party_short_name.charAt(
                                                    0
                                                )}
                                            </div>
                                            <div className='flex-1'>
                                                <Text variant="body" weight="bold" className='text-gray-900 text-sm'>
                                                    {party.party_name}
                                                </Text>
                                                <Text variant="caption" className='text-gray-600'>
                                                    {party.party_short_name}
                                                    {party.total_seats &&
                                                        ` • ${party.total_seats} seats`}
                                                </Text>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {/* Footer Info */}
                <div className='text-center py-8'>
                    <div className='inline-flex items-center gap-2 bg-white rounded-full px-6 py-3 shadow-md border border-gray-200'>
                        <div className='w-2 h-2 rounded-full bg-green-500 animate-pulse'></div>
                        <Text variant="small" className='text-gray-600'>
                            Data powered by Rajniti Election API
                        </Text>
                    </div>
                </div>
            </div>
        </div>
    )
}
