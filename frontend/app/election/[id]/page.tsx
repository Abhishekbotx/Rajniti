"use client"

import { useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { useOnboardingCheck } from "@/hooks/useOnboardingCheck"
import { useElection } from "@/hooks/useElection"
import { useParties } from "@/hooks/useParties"
import { useSearchCandidates } from "@/hooks/useCandidate"
import { Footer, Navbar } from "@/components/layout"
import Button from "@/components/ui/Button"
import Text from "@/components/ui/Text"
import Image from "@/components/ui/Image"
import Link from "next/link"

export default function ElectionPage() {
    const { loading: onboardingLoading } = useOnboardingCheck(true)
    const params = useParams()
    const router = useRouter()
    const electionId = params.id as string

    const { election, loading, error } = useElection(electionId)
    const { parties } = useParties(electionId)
    const {
        candidates,
        loading: searchLoading,
        search,
        clear
    } = useSearchCandidates()

    const [searchQuery, setSearchQuery] = useState("")

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault()
        if (searchQuery.trim()) {
            search(searchQuery)
        } else {
            clear()
        }
    }

    if (onboardingLoading || loading) {
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

    if (error || !election) {
        return (
            <div className='min-h-screen bg-gradient-to-b from-orange-50 via-white to-green-50 flex items-center justify-center p-4'>
                <div className='bg-white rounded-lg shadow-lg p-8 max-w-md w-full border-l-4 border-red-500'>
                    <div className='flex items-center gap-3 mb-4'>
                        <div className='text-red-500 text-3xl'>⚠️</div>
                        <Text
                            variant='h4'
                            weight='bold'
                            className='text-gray-900'>
                            Error
                        </Text>
                    </div>
                    <Text variant='body' className='text-gray-600 mb-4'>
                        {error || "Election not found"}
                    </Text>
                    <Button onClick={() => router.push("/dashboard")} fullWidth>
                        Back to Dashboard
                    </Button>
                </div>
            </div>
        )
    }

    return (
        <div className='min-h-screen bg-gradient-to-b from-orange-50 via-white to-green-50'>
            <Navbar variant='dashboard' sticky={true} />

            <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8'>
                <div className='mb-6'>
                    <Button
                        onClick={() => router.push("/dashboard")}
                        variant='secondary'
                        size='sm'>
                        ← Back to Elections
                    </Button>
                </div>

                <div className='mb-8'>
                    <div className='bg-gradient-to-r from-orange-500 to-orange-600 rounded-2xl p-8 text-white shadow-lg'>
                        <Text
                            variant='h2'
                            weight='bold'
                            className='text-white mb-2'>
                            {election.name}
                        </Text>
                        <Text variant='body' className='text-orange-100 mb-6'>
                            Year: {election.year} | Type: {election.type}
                        </Text>

                        <div className='grid grid-cols-2 md:grid-cols-4 gap-4'>
                            <div className='bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20'>
                                <Text
                                    variant='h3'
                                    weight='bold'
                                    className='text-white'>
                                    {election.statistics.total_constituencies}
                                </Text>
                                <Text
                                    variant='small'
                                    className='text-orange-100 mt-1'>
                                    Constituencies
                                </Text>
                            </div>
                            <div className='bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20'>
                                <Text
                                    variant='h3'
                                    weight='bold'
                                    className='text-white'>
                                    {election.statistics.total_candidates.toLocaleString()}
                                </Text>
                                <Text
                                    variant='small'
                                    className='text-orange-100 mt-1'>
                                    Candidates
                                </Text>
                            </div>
                            <div className='bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20'>
                                <Text
                                    variant='h3'
                                    weight='bold'
                                    className='text-white'>
                                    {election.statistics.total_parties}
                                </Text>
                                <Text
                                    variant='small'
                                    className='text-orange-100 mt-1'>
                                    Parties
                                </Text>
                            </div>
                            <div className='bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20'>
                                <Text
                                    variant='h3'
                                    weight='bold'
                                    className='text-white'>
                                    {election.statistics.total_winners}
                                </Text>
                                <Text
                                    variant='small'
                                    className='text-orange-100 mt-1'>
                                    Winners
                                </Text>
                            </div>
                        </div>
                    </div>
                </div>

                <div className='mb-8'>
                    <div className='bg-white rounded-2xl shadow-lg p-6 border border-gray-200'>
                        <Text
                            variant='h3'
                            weight='bold'
                            className='text-gray-900 mb-4'>
                            Search Candidates
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
                                size='lg'
                                className='px-8'>
                                {searchLoading ? "Searching..." : "Search"}
                            </Button>
                        </form>

                        {candidates.length > 0 && (
                            <div className='mt-6 space-y-3'>
                                <Text
                                    variant='body'
                                    weight='semibold'
                                    className='text-gray-700'>
                                    Results ({candidates.length})
                                </Text>
                                <div className='grid gap-3'>
                                    {candidates.map((candidate) => (
                                        <Link
                                            key={candidate.id}
                                            href={`/candidate/${candidate.id}`}
                                            className='block'>
                                            <div className='bg-gradient-to-r from-gray-50 to-white rounded-lg p-4 border border-gray-200 hover:border-orange-300 transition-colors cursor-pointer'>
                                                <div className='flex items-center gap-4'>
                                                    {candidate.image_url && (
                                                        <Image
                                                            src={
                                                                candidate.image_url
                                                            }
                                                            alt={candidate.name}
                                                            width={64}
                                                            height={64}
                                                            rounded='full'
                                                            className='w-16 h-16 object-cover border-2 border-orange-200'
                                                        />
                                                    )}
                                                    <div className='flex-1'>
                                                        <Text
                                                            variant='body'
                                                            weight='bold'
                                                            className='text-gray-900'>
                                                            {candidate.name}
                                                        </Text>
                                                        <Text
                                                            variant='small'
                                                            className='text-gray-600'>
                                                            {
                                                                candidate.party_name
                                                            }{" "}
                                                            (
                                                            {
                                                                candidate.party_short_name
                                                            }
                                                            )
                                                        </Text>
                                                        <Text
                                                            variant='small'
                                                            className='text-gray-500'>
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
                                        </Link>
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

                {parties.length > 0 && (
                    <div className='mb-8'>
                        <div className='bg-white rounded-2xl shadow-lg p-6 border border-gray-200'>
                            <Text
                                variant='h3'
                                weight='bold'
                                className='text-gray-900 mb-4'>
                                Major Parties
                            </Text>
                            <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
                                {parties.map((party, index) => (
                                    <div
                                        key={index}
                                        className='bg-gradient-to-br from-orange-50 to-white rounded-lg p-4 border border-orange-200 hover:border-orange-400 transition-colors'>
                                        <div className='flex items-center gap-3'>
                                            <div className='w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 font-bold'>
                                                {party.short_name.charAt(0)}
                                            </div>
                                            <div className='flex-1'>
                                                <Text
                                                    variant='body'
                                                    weight='bold'
                                                    className='text-gray-900 text-sm'>
                                                    {party.name}
                                                </Text>
                                                <Text
                                                    variant='caption'
                                                    className='text-gray-600'>
                                                    {party.short_name}
                                                    {party.seats_won &&
                                                        ` • ${party.seats_won} seats`}
                                                </Text>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                <Footer />
            </div>
        </div>
    )
}
