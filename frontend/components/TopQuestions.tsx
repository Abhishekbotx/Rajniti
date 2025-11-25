"use client"

import { useState } from "react"
import Text from "@/components/ui/Text"
import Button from "@/components/ui/Button"
import { useQuestions, useAskQuestion } from "@/hooks/useQuestions"
import Link from "next/link"

interface TopQuestionsProps {
    candidateId?: string
}

export default function TopQuestions({ candidateId }: TopQuestionsProps) {
    const { questions, loading: questionsLoading } = useQuestions()
    const {
        answer,
        loading: answerLoading,
        askQuestion,
        askPredefinedQuestion,
        clearAnswer,
    } = useAskQuestion()
    const [customQuestion, setCustomQuestion] = useState("")
    const [activeQuestionId, setActiveQuestionId] = useState<string | null>(null)

    const handlePredefinedQuestion = async (questionId: string) => {
        setActiveQuestionId(questionId)
        await askPredefinedQuestion(questionId, candidateId)
    }

    const handleCustomQuestion = async (e: React.FormEvent) => {
        e.preventDefault()
        if (customQuestion.trim()) {
            setActiveQuestionId(null)
            await askQuestion(customQuestion, candidateId)
        }
    }

    const getCategoryIcon = (category: string) => {
        switch (category) {
            case "education":
                return "🎓"
            case "political":
                return "🏛️"
            case "assets":
                return "💰"
            case "crime":
                return "⚖️"
            case "family":
                return "👨‍👩‍👧‍👦"
            default:
                return "❓"
        }
    }

    const getCategoryColor = (category: string) => {
        switch (category) {
            case "education":
                return "from-blue-50 to-blue-100 border-blue-200 hover:border-blue-400"
            case "political":
                return "from-purple-50 to-purple-100 border-purple-200 hover:border-purple-400"
            case "assets":
                return "from-green-50 to-green-100 border-green-200 hover:border-green-400"
            case "crime":
                return "from-red-50 to-red-100 border-red-200 hover:border-red-400"
            case "family":
                return "from-orange-50 to-orange-100 border-orange-200 hover:border-orange-400"
            default:
                return "from-gray-50 to-gray-100 border-gray-200 hover:border-gray-400"
        }
    }

    if (questionsLoading) {
        return (
            <div className='bg-white rounded-2xl shadow-lg p-6 border border-gray-200'>
                <div className='animate-pulse'>
                    <div className='h-6 bg-gray-200 rounded w-1/3 mb-4'></div>
                    <div className='space-y-3'>
                        {[1, 2, 3, 4, 5].map((i) => (
                            <div
                                key={i}
                                className='h-16 bg-gray-100 rounded-lg'></div>
                        ))}
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className='bg-white rounded-2xl shadow-lg p-6 border border-gray-200'>
            <div className='flex items-center gap-3 mb-6'>
                <span className='text-2xl'>💡</span>
                <Text variant='h3' weight='bold' className='text-gray-900'>
                    Ask About Candidates
                </Text>
            </div>

            {/* Custom Question Input */}
            <form onSubmit={handleCustomQuestion} className='mb-6'>
                <div className='flex gap-2'>
                    <input
                        type='text'
                        value={customQuestion}
                        onChange={(e) => setCustomQuestion(e.target.value)}
                        placeholder='Ask any question about candidates...'
                        className='flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent'
                    />
                    <Button
                        type='submit'
                        disabled={answerLoading || !customQuestion.trim()}
                        isLoading={answerLoading && !activeQuestionId}
                        size='lg'>
                        Ask
                    </Button>
                </div>
            </form>

            {/* Predefined Questions */}
            <div className='mb-4'>
                <Text
                    variant='body'
                    weight='semibold'
                    className='text-gray-700 mb-3'>
                    Top 5 Questions
                </Text>
                <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3'>
                    {questions.map((q) => (
                        <button
                            key={q.id}
                            onClick={() => handlePredefinedQuestion(q.id)}
                            disabled={answerLoading}
                            className={`text-left p-4 rounded-lg border-2 transition-all cursor-pointer bg-gradient-to-br ${getCategoryColor(
                                q.category
                            )} ${
                                activeQuestionId === q.id
                                    ? "ring-2 ring-orange-500 ring-offset-2"
                                    : ""
                            } disabled:opacity-50 disabled:cursor-not-allowed`}>
                            <div className='flex items-start gap-3'>
                                <span className='text-xl flex-shrink-0'>
                                    {getCategoryIcon(q.category)}
                                </span>
                                <div className='flex-1 min-w-0'>
                                    <Text
                                        variant='small'
                                        weight='semibold'
                                        className='text-gray-800 overflow-hidden'
                                        style={{ display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' }}>
                                        {q.question}
                                    </Text>
                                    <Text
                                        variant='caption'
                                        className='text-gray-500 mt-1'>
                                        {q.description}
                                    </Text>
                                </div>
                            </div>
                        </button>
                    ))}
                </div>
            </div>

            {/* Answer Section */}
            {(answer || answerLoading) && (
                <div className='mt-6 pt-6 border-t border-gray-200'>
                    <div className='flex items-center justify-between mb-4'>
                        <Text
                            variant='body'
                            weight='bold'
                            className='text-gray-900'>
                            {answerLoading ? "Finding answer..." : "Answer"}
                        </Text>
                        {answer && !answerLoading && (
                            <Button
                                variant='ghost'
                                size='sm'
                                onClick={clearAnswer}>
                                Clear
                            </Button>
                        )}
                    </div>

                    {answerLoading ? (
                        <div className='bg-orange-50 rounded-lg p-4 border border-orange-200'>
                            <div className='animate-pulse'>
                                <div className='h-4 bg-orange-200 rounded w-3/4 mb-2'></div>
                                <div className='h-4 bg-orange-200 rounded w-1/2'></div>
                            </div>
                        </div>
                    ) : answer ? (
                        <div className='space-y-4'>
                            {/* Question */}
                            <div className='bg-gray-50 rounded-lg p-4 border border-gray-200'>
                                <Text
                                    variant='small'
                                    className='text-gray-500 mb-1'>
                                    Question:
                                </Text>
                                <Text
                                    variant='body'
                                    weight='medium'
                                    className='text-gray-800'>
                                    {answer.question}
                                </Text>
                            </div>

                            {/* Answer */}
                            <div className='bg-gradient-to-br from-orange-50 to-white rounded-lg p-4 border border-orange-200'>
                                <Text
                                    variant='small'
                                    className='text-orange-600 mb-1'>
                                    Answer:
                                </Text>
                                <Text variant='body' className='text-gray-800'>
                                    {answer.answer}
                                </Text>
                            </div>

                            {/* Related Candidates */}
                            {answer.candidates && answer.candidates.length > 0 && (
                                <div>
                                    <Text
                                        variant='small'
                                        weight='semibold'
                                        className='text-gray-700 mb-3'>
                                        Related Candidates ({answer.total_results})
                                    </Text>
                                    <div className='grid gap-2'>
                                        {answer.candidates
                                            .slice(0, 3)
                                            .map((candidate, index) => (
                                                <Link
                                                    key={index}
                                                    href={`/candidate/${candidate.candidate_id}`}
                                                    className='block'>
                                                    <div className='bg-white rounded-lg p-3 border border-gray-200 hover:border-orange-300 transition-colors'>
                                                        <div className='flex items-center justify-between'>
                                                            <div>
                                                                <Text
                                                                    variant='small'
                                                                    weight='bold'
                                                                    className='text-gray-900'>
                                                                    {candidate.name}
                                                                </Text>
                                                                <Text
                                                                    variant='caption'
                                                                    className='text-gray-500'>
                                                                    {candidate.party_id} •{" "}
                                                                    {candidate.constituency_id}
                                                                </Text>
                                                            </div>
                                                            <div className='flex items-center gap-2'>
                                                                <span
                                                                    className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
                                                                        candidate.status ===
                                                                        "WON"
                                                                            ? "bg-green-100 text-green-700"
                                                                            : "bg-gray-100 text-gray-600"
                                                                    }`}>
                                                                    {candidate.status}
                                                                </span>
                                                                {candidate.relevance_score && (
                                                                    <span className='text-xs text-gray-400'>
                                                                        {Math.round(
                                                                            candidate.relevance_score *
                                                                                100
                                                                        )}
                                                                        % match
                                                                    </span>
                                                                )}
                                                            </div>
                                                        </div>
                                                    </div>
                                                </Link>
                                            ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    ) : null}
                </div>
            )}
        </div>
    )
}
