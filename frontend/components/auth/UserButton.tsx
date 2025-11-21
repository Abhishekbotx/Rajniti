"use client"

import { useSession, signIn, signOut } from "next-auth/react"
import { useState } from "react"
import Image from "@/components/ui/Image"
import Button from "@/components/ui/Button"
import Text from "@/components/ui/Text"
import Link from "@/components/ui/Link"

export default function UserButton() {
    const { data: session } = useSession()
    const [showMenu, setShowMenu] = useState(false)

    if (!session) {
        return (
            <Button onClick={() => signIn()}>
                Sign In
            </Button>
        )
    }

    return (
        <div className='relative'>
            <button
                onClick={() => setShowMenu(!showMenu)}
                className='flex items-center gap-2 p-1 pr-3 border-2 border-orange-200 rounded-full hover:border-orange-300 transition-all'
            >
                <Image
                    src={session.user?.image || "/default-avatar.png"}
                    alt={session.user?.name || "User"}
                    width={32}
                    height={32}
                    rounded="full"
                    className='w-8 h-8'
                />
                <Text variant="small" weight="medium" className='text-gray-700'>
                    {session.user?.name?.split(" ")[0]}
                </Text>
            </button>

            {showMenu && (
                <div className='absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-xl border border-gray-200 py-2 z-50'>
                    <div className='px-4 py-3 border-b border-gray-100'>
                        <Text variant="small" weight="semibold" color="default">
                            {session.user?.name}
                        </Text>
                        <Text variant="caption" color="muted">
                            {session.user?.email}
                        </Text>
                    </div>

                    <Link
                        href='/dashboard'
                        className='block px-4 py-2 text-sm text-gray-700 hover:bg-orange-50 transition-colors'
                    >
                        Dashboard
                    </Link>

                    <Link
                        href='/profile/edit'
                        className='block px-4 py-2 text-sm text-gray-700 hover:bg-orange-50 transition-colors'
                    >
                        Edit Profile
                    </Link>

                    <button
                        onClick={() => signOut({ callbackUrl: "/" })}
                        className='w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors'
                    >
                        Sign Out
                    </button>
                </div>
            )}
        </div>
    )
}
