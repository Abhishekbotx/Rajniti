"use client"

import { useSession, signIn, signOut } from "next-auth/react"
import { useState } from "react"
import Image from "next/image"

export default function UserButton() {
    const { data: session } = useSession()
    const [showMenu, setShowMenu] = useState(false)

    if (!session) {
        return (
            <button
                onClick={() => signIn()}
                className='px-6 py-2 bg-gradient-to-r from-orange-500 to-orange-600 text-white font-semibold rounded-lg hover:from-orange-600 hover:to-orange-700 transition-all shadow-md hover:shadow-lg'>
                Sign In
            </button>
        )
    }

    return (
        <div className='relative'>
            <button
                onClick={() => setShowMenu(!showMenu)}
                className='flex items-center gap-2 p-1 pr-3 border-2 border-orange-200 rounded-full hover:border-orange-300 transition-all'>
                <Image
                    src={session.user?.image || "/default-avatar.png"}
                    alt={session.user?.name || "User"}
                    width={32}
                    height={32}
                    className='w-8 h-8 rounded-full'
                />
                <span className='text-sm font-medium text-gray-700'>
                    {session.user?.name?.split(" ")[0]}
                </span>
            </button>

            {showMenu && (
                <div className='absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-xl border border-gray-200 py-2 z-50'>
                    <div className='px-4 py-3 border-b border-gray-100'>
                        <p className='text-sm font-semibold text-gray-900'>
                            {session.user?.name}
                        </p>
                        <p className='text-xs text-gray-500'>
                            {session.user?.email}
                        </p>
                    </div>

                    <a
                        href='/profile/edit'
                        className='block px-4 py-2 text-sm text-gray-700 hover:bg-orange-50 transition-colors'>
                        Dashboard
                    </a>

                    <a
                        href='/profile/edit'
                        className='block px-4 py-2 text-sm text-gray-700 hover:bg-orange-50 transition-colors'>
                        Edit Profile
                    </a>

                    <button
                        onClick={() => signOut()}
                        className='w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors'>
                        Sign Out
                    </button>
                </div>
            )}
        </div>
    )
}
