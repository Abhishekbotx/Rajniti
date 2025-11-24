"use client"

import { useParams, useRouter } from "next/navigation"
import { useOnboardingCheck } from "@/hooks/useOnboardingCheck"
import { useCandidate } from "@/hooks/useCandidate"
import { Footer, Navbar } from "@/components/layout"
import Button from "@/components/ui/Button"
import Text from "@/components/ui/Text"
import Image from "@/components/ui/Image"

export default function CandidatePage() {
    const { loading: onboardingLoading } = useOnboardingCheck(true)
    const params = useParams()
    const router = useRouter()
    const candidateId = params.id as string

    const { candidate, loading, error } = useCandidate(candidateId)

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

    if (error || !candidate) {
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
                        {error || "Candidate not found"}
                    </Text>
                    <Button onClick={() => router.push("/dashboard")} fullWidth>
                        Back to Dashboard
                    </Button>
                </div>
            </div>
        )
    }

    const formatAmount = (amount: number | undefined) => {
        if (!amount) return "N/A"
        return new Intl.NumberFormat("en-IN", {
            style: "currency",
            currency: "INR"
        }).format(amount)
    }

    return (
        <div className='min-h-screen bg-gradient-to-b from-orange-50 via-white to-green-50'>
            <Navbar variant='dashboard' sticky={true} />

            <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8'>
                <div className='mb-6'>
                    <Button
                        onClick={() => router.back()}
                        variant='secondary'
                        size='sm'>
                        ← Back
                    </Button>
                </div>

                <div className='mb-8'>
                    <div className='bg-white rounded-2xl shadow-lg p-8 border border-gray-200'>
                        <div className='flex flex-col md:flex-row gap-6 items-start'>
                            {candidate.image_url && (
                                <Image
                                    src={candidate.image_url}
                                    alt={candidate.name}
                                    width={160}
                                    height={160}
                                    rounded='lg'
                                    className='w-40 h-40 object-cover border-4 border-orange-200'
                                />
                            )}
                            <div className='flex-1'>
                                <Text
                                    variant='h2'
                                    weight='bold'
                                    className='text-gray-900 mb-2'>
                                    {candidate.name}
                                </Text>
                                <div className='space-y-2'>
                                    <div className='flex items-center gap-2'>
                                        <Text
                                            variant='body'
                                            className='text-gray-700'>
                                            <span className='font-semibold'>
                                                Party:
                                            </span>{" "}
                                            {candidate.party_name} (
                                            {candidate.party_short_name})
                                        </Text>
                                    </div>
                                    <div className='flex items-center gap-2'>
                                        <Text
                                            variant='body'
                                            className='text-gray-700'>
                                            <span className='font-semibold'>
                                                Constituency:
                                            </span>{" "}
                                            {candidate.constituency_name}
                                        </Text>
                                    </div>
                                    <div className='flex items-center gap-2'>
                                        <Text
                                            variant='body'
                                            className='text-gray-700'>
                                            <span className='font-semibold'>
                                                Status:
                                            </span>
                                        </Text>
                                        <span
                                            className={`px-3 py-1 rounded-full text-sm font-semibold ${
                                                candidate.status === "WON"
                                                    ? "bg-green-100 text-green-700"
                                                    : "bg-gray-100 text-gray-600"
                                            }`}>
                                            {candidate.status}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {candidate.education_background &&
                    candidate.education_background.length > 0 && (
                        <div className='mb-8'>
                            <div className='bg-white rounded-2xl shadow-lg p-6 border border-gray-200'>
                                <Text
                                    variant='h3'
                                    weight='bold'
                                    className='text-gray-900 mb-4'>
                                    Education Background
                                </Text>
                                <div className='space-y-3'>
                                    {candidate.education_background.map(
                                        (edu, index) => (
                                            <div
                                                key={index}
                                                className='bg-orange-50 rounded-lg p-4 border border-orange-200'>
                                                <Text
                                                    variant='body'
                                                    weight='semibold'
                                                    className='text-gray-900'>
                                                    {edu.stream || "N/A"}{" "}
                                                    {edu.year && `(${edu.year})`}
                                                </Text>
                                                <Text
                                                    variant='small'
                                                    className='text-gray-600'>
                                                    {edu.college || "N/A"}
                                                </Text>
                                                {edu.other_details && (
                                                    <Text
                                                        variant='small'
                                                        className='text-gray-500 mt-1'>
                                                        {edu.other_details}
                                                    </Text>
                                                )}
                                            </div>
                                        )
                                    )}
                                </div>
                            </div>
                        </div>
                    )}

                {candidate.political_background &&
                    candidate.political_background.length > 0 && (
                        <div className='mb-8'>
                            <div className='bg-white rounded-2xl shadow-lg p-6 border border-gray-200'>
                                <Text
                                    variant='h3'
                                    weight='bold'
                                    className='text-gray-900 mb-4'>
                                    Political History
                                </Text>
                                <div className='space-y-3'>
                                    {candidate.political_background.map(
                                        (pol, index) => (
                                            <div
                                                key={index}
                                                className='bg-orange-50 rounded-lg p-4 border border-orange-200'>
                                                <div className='flex justify-between items-start'>
                                                    <div>
                                                        <Text
                                                            variant='body'
                                                            weight='semibold'
                                                            className='text-gray-900'>
                                                            {pol.party || "N/A"}{" "}
                                                            •{" "}
                                                            {pol.constituency ||
                                                                "N/A"}
                                                        </Text>
                                                        <Text
                                                            variant='small'
                                                            className='text-gray-600'>
                                                            {pol.position ||
                                                                "N/A"}{" "}
                                                            •{" "}
                                                            {pol.election_year ||
                                                                "N/A"}
                                                        </Text>
                                                    </div>
                                                    <span
                                                        className={`px-2 py-1 rounded text-xs font-semibold ${
                                                            pol.result === "WON"
                                                                ? "bg-green-100 text-green-700"
                                                                : "bg-red-100 text-red-700"
                                                        }`}>
                                                        {pol.result || "N/A"}
                                                    </span>
                                                </div>
                                            </div>
                                        )
                                    )}
                                </div>
                            </div>
                        </div>
                    )}

                {candidate.family_background &&
                    candidate.family_background.length > 0 && (
                        <div className='mb-8'>
                            <div className='bg-white rounded-2xl shadow-lg p-6 border border-gray-200'>
                                <Text
                                    variant='h3'
                                    weight='bold'
                                    className='text-gray-900 mb-4'>
                                    Family Background
                                </Text>
                                <div className='grid gap-3'>
                                    {candidate.family_background.map(
                                        (member, index) => (
                                            <div
                                                key={index}
                                                className='bg-orange-50 rounded-lg p-4 border border-orange-200'>
                                                <Text
                                                    variant='body'
                                                    weight='semibold'
                                                    className='text-gray-900'>
                                                    {member.name || "N/A"}{" "}
                                                    {member.age &&
                                                        `(${member.age})`}
                                                </Text>
                                                <Text
                                                    variant='small'
                                                    className='text-gray-600'>
                                                    {member.relation || "N/A"} •{" "}
                                                    {member.profession || "N/A"}
                                                </Text>
                                            </div>
                                        )
                                    )}
                                </div>
                            </div>
                        </div>
                    )}

                {candidate.assets && candidate.assets.length > 0 && (
                    <div className='mb-8'>
                        <div className='bg-white rounded-2xl shadow-lg p-6 border border-gray-200'>
                            <Text
                                variant='h3'
                                weight='bold'
                                className='text-gray-900 mb-4'>
                                Assets
                            </Text>
                            <div className='space-y-3'>
                                {candidate.assets.map((asset, index) => (
                                    <div
                                        key={index}
                                        className='bg-green-50 rounded-lg p-4 border border-green-200'>
                                        <div className='flex justify-between items-start'>
                                            <div className='flex-1'>
                                                <Text
                                                    variant='body'
                                                    weight='semibold'
                                                    className='text-gray-900'>
                                                    {asset.type || "N/A"}
                                                </Text>
                                                <Text
                                                    variant='small'
                                                    className='text-gray-600'>
                                                    {asset.description || "N/A"}
                                                </Text>
                                                <Text
                                                    variant='small'
                                                    className='text-gray-500'>
                                                    Owned by:{" "}
                                                    {asset.owned_by || "N/A"}
                                                </Text>
                                            </div>
                                            <Text
                                                variant='body'
                                                weight='bold'
                                                className='text-green-700'>
                                                {formatAmount(asset.amount)}
                                            </Text>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {candidate.liabilities && candidate.liabilities.length > 0 && (
                    <div className='mb-8'>
                        <div className='bg-white rounded-2xl shadow-lg p-6 border border-gray-200'>
                            <Text
                                variant='h3'
                                weight='bold'
                                className='text-gray-900 mb-4'>
                                Liabilities
                            </Text>
                            <div className='space-y-3'>
                                {candidate.liabilities.map(
                                    (liability, index) => (
                                        <div
                                            key={index}
                                            className='bg-red-50 rounded-lg p-4 border border-red-200'>
                                            <div className='flex justify-between items-start'>
                                                <div className='flex-1'>
                                                    <Text
                                                        variant='body'
                                                        weight='semibold'
                                                        className='text-gray-900'>
                                                        {liability.type || "N/A"}
                                                    </Text>
                                                    <Text
                                                        variant='small'
                                                        className='text-gray-600'>
                                                        {liability.description ||
                                                            "N/A"}
                                                    </Text>
                                                    <Text
                                                        variant='small'
                                                        className='text-gray-500'>
                                                        Owned by:{" "}
                                                        {liability.owned_by ||
                                                            "N/A"}
                                                    </Text>
                                                </div>
                                                <Text
                                                    variant='body'
                                                    weight='bold'
                                                    className='text-red-700'>
                                                    {formatAmount(
                                                        liability.amount
                                                    )}
                                                </Text>
                                            </div>
                                        </div>
                                    )
                                )}
                            </div>
                        </div>
                    </div>
                )}

                {candidate.crime_cases && candidate.crime_cases.length > 0 && (
                    <div className='mb-8'>
                        <div className='bg-white rounded-2xl shadow-lg p-6 border border-gray-200'>
                            <Text
                                variant='h3'
                                weight='bold'
                                className='text-gray-900 mb-4'>
                                Crime Cases
                            </Text>
                            <div className='space-y-3'>
                                {candidate.crime_cases.map((crime, index) => (
                                    <div
                                        key={index}
                                        className='bg-red-50 rounded-lg p-4 border border-red-200'>
                                        <Text
                                            variant='body'
                                            weight='semibold'
                                            className='text-gray-900'>
                                            FIR No: {crime.fir_no || "N/A"}
                                        </Text>
                                        <Text
                                            variant='small'
                                            className='text-gray-600'>
                                            Police Station:{" "}
                                            {crime.police_station || "N/A"}
                                        </Text>
                                        {crime.sections_applied &&
                                            crime.sections_applied.length >
                                                0 && (
                                                <Text
                                                    variant='small'
                                                    className='text-gray-600'>
                                                    Sections:{" "}
                                                    {crime.sections_applied.join(
                                                        ", "
                                                    )}
                                                </Text>
                                            )}
                                        <Text
                                            variant='small'
                                            className='text-gray-600'>
                                            Charges Framed:{" "}
                                            {crime.charges_framed ? "Yes" : "No"}
                                        </Text>
                                        {crime.description && (
                                            <Text
                                                variant='small'
                                                className='text-gray-500 mt-2'>
                                                {crime.description}
                                            </Text>
                                        )}
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
