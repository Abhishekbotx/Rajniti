"use client"

import { useOnboardingCheck } from "@/hooks/useOnboardingCheck"
import { useElections } from "@/hooks/useElection"
import { Footer, Navbar } from "@/components/layout"
import Button from "@/components/ui/Button"
import Text from "@/components/ui/Text"
import Link from "next/link"

export default function Dashboard() {
    const { loading: onboardingLoading } = useOnboardingCheck(true)
    const { elections, loading, error } = useElections()

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
                        Loading Elections...
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
                        <Text
                            variant='h4'
                            weight='bold'
                            className='text-gray-900'>
                            Connection Error
                        </Text>
                    </div>
                    <Text variant='body' className='text-gray-600 mb-4'>
                        {error}
                    </Text>
                    <Button onClick={() => window.location.reload()} fullWidth>
                        Try Again
                    </Button>
                </div>
            </div>
        )
    }

    return (
        <div className='min-h-screen bg-gradient-to-b from-orange-50 via-white to-green-50'>
            <Navbar variant='dashboard' sticky={true} />

            <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8'>
                <div className='mb-8'>
                    <Text variant='h2' weight='bold' className='text-gray-900 mb-2'>
                        Recent Elections
                    </Text>
                    <Text variant='body' className='text-gray-600'>
                        Explore election data and candidates from recent Indian elections
                    </Text>
                </div>

                <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
                    {elections.map((election) => (
                        <Link
                            key={election.id}
                            href={`/election/${election.id}`}
                            className='block'>
                            <div className='bg-white rounded-2xl shadow-lg p-6 border border-gray-200 hover:border-orange-400 hover:shadow-xl transition-all cursor-pointer'>
                                <Text
                                    variant='h3'
                                    weight='bold'
                                    className='text-gray-900 mb-2'>
                                    {election.name}
                                </Text>
                                <Text
                                    variant='body'
                                    className='text-gray-600 mb-4'>
                                    Year: {election.year} | Type:{" "}
                                    {election.type}
                                </Text>

                                <div className='grid grid-cols-2 gap-3'>
                                    <div className='bg-orange-50 rounded-lg p-3'>
                                        <Text
                                            variant='h4'
                                            weight='bold'
                                            className='text-orange-600'>
                                            {
                                                election.statistics
                                                    .total_constituencies
                                            }
                                        </Text>
                                        <Text
                                            variant='small'
                                            className='text-gray-600'>
                                            Constituencies
                                        </Text>
                                    </div>
                                    <div className='bg-orange-50 rounded-lg p-3'>
                                        <Text
                                            variant='h4'
                                            weight='bold'
                                            className='text-orange-600'>
                                            {election.statistics.total_candidates.toLocaleString()}
                                        </Text>
                                        <Text
                                            variant='small'
                                            className='text-gray-600'>
                                            Candidates
                                        </Text>
                                    </div>
                                    <div className='bg-green-50 rounded-lg p-3'>
                                        <Text
                                            variant='h4'
                                            weight='bold'
                                            className='text-green-600'>
                                            {election.statistics.total_parties}
                                        </Text>
                                        <Text
                                            variant='small'
                                            className='text-gray-600'>
                                            Parties
                                        </Text>
                                    </div>
                                    <div className='bg-green-50 rounded-lg p-3'>
                                        <Text
                                            variant='h4'
                                            weight='bold'
                                            className='text-green-600'>
                                            {election.statistics.total_winners}
                                        </Text>
                                        <Text
                                            variant='small'
                                            className='text-gray-600'>
                                            Winners
                                        </Text>
                                    </div>
                                </div>

                                <div className='mt-4 flex items-center text-orange-600'>
                                    <Text variant='body' weight='semibold'>
                                        View Details
                                    </Text>
                                    <span className='ml-2'>→</span>
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>

                <Footer />
            </div>
        </div>
    )
}
