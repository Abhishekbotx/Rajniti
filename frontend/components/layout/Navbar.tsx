"use client"

import UserButton from "@/components/auth/UserButton"
import Text from "@/components/ui/Text"
import Link from "@/components/ui/Link"

interface NavbarProps {
    variant?: "default" | "dashboard"
    sticky?: boolean
}

export default function Navbar({
    variant = "default",
    sticky = false
}: NavbarProps) {
    const isDashboard = variant === "dashboard"
    const stickyClasses = sticky ? "sticky top-0 z-10" : ""

    return (
        <header
            className={`border-b border-orange-200 bg-white/80 backdrop-blur-sm ${stickyClasses}`}>
            <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8'>
                <div className='flex h-16 items-center justify-between'>
                    <div className='flex items-center gap-2'>
                        <div className='text-2xl font-bold'>🗳️</div>
                        <Text variant='h4' className='text-gray-900'>
                            Rajniti
                        </Text>
                    </div>

                    {isDashboard ? (
                        <div className='flex items-center gap-4'>
                            <Link href='/' variant='nav'>
                                Home
                            </Link>
                            <UserButton />
                        </div>
                    ) : (
                        <nav className='hidden md:flex gap-6 items-center'>
                            <Link href='/dashboard' variant='nav'>
                                Dashboard
                            </Link>
                            <Link href='#about' variant='nav'>
                                About
                            </Link>
                            <Link href='#contribute' variant='nav'>
                                Contribute
                            </Link>
                            <Link
                                href='https://chat.whatsapp.com/IceA98FSHHuDmXOwv8WH7v'
                                external
                                variant='nav'>
                                Join Community
                            </Link>
                            <Link href='#api' variant='nav'>
                                API
                            </Link>
                            <UserButton />
                        </nav>
                    )}
                </div>
            </div>
        </header>
    )
}
