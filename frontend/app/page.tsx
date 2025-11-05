export default function Home() {
    return (
        <div className='min-h-screen bg-gradient-to-b from-orange-50 via-white to-green-50'>
            {/* Header */}
            <header className='border-b border-orange-200 bg-white/80 backdrop-blur-sm'>
                <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8'>
                    <div className='flex h-16 items-center justify-between'>
                        <div className='flex items-center gap-2'>
                            <div className='text-2xl font-bold'>🗳️</div>
                            <span className='text-xl font-bold text-gray-900'>
                                Rajniti
                            </span>
                        </div>
                        <nav className='hidden md:flex gap-6'>
                            <a
                                href='#about'
                                className='text-gray-600 hover:text-orange-600 transition-colors'>
                                About
                            </a>
                            <a
                                href='#contribute'
                                className='text-gray-600 hover:text-orange-600 transition-colors'>
                                Contribute
                            </a>
                            <a
                                href='https://chat.whatsapp.com/IceA98FSHHuDmXOwv8WH7v'
                                target='_blank'
                                rel='noopener noreferrer'
                                className='text-gray-600 hover:text-orange-600 transition-colors'>
                                Join Community
                            </a>
                            <a
                                href='#api'
                                className='text-gray-600 hover:text-orange-600 transition-colors'>
                                API
                            </a>
                        </nav>
                    </div>
                </div>
            </header>

            {/* Hero Section */}
            <section className='relative overflow-hidden py-20 sm:py-32'>
                <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8'>
                    <div className='text-center'>
                        <div className='mb-8 flex justify-center'>
                            <div className='rounded-full bg-gradient-to-r from-orange-500 via-white to-green-500 p-1'>
                                <div className='rounded-full bg-white px-6 py-2'>
                                    <span className='text-sm font-semibold text-gray-700'>
                                        Built for 🇮🇳 Democracy
                                    </span>
                                </div>
                            </div>
                        </div>

                        <h1 className='text-4xl sm:text-6xl font-bold tracking-tight text-gray-900 mb-6'>
                            Empowering Democracy Through
                            <span className='block bg-gradient-to-r from-orange-600 via-orange-500 to-green-600 bg-clip-text text-transparent'>
                                Open Election Data
                            </span>
                        </h1>

                        <p className='mx-auto max-w-2xl text-lg sm:text-xl text-gray-600 mb-10'>
                            Rajniti is a clean, lightweight REST API providing
                            comprehensive Indian Election Commission data.
                            Access 50,000+ records across Lok Sabha and Assembly
                            elections - free and open source.
                        </p>

                        <div className='flex flex-col sm:flex-row gap-4 justify-center items-center'>
                            <a
                                href='https://github.com/imsks/rajniti'
                                target='_blank'
                                rel='noopener noreferrer'
                                className='inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-orange-600 to-orange-500 px-8 py-4 text-white font-semibold shadow-lg hover:shadow-xl transition-all hover:scale-105'>
                                <svg
                                    className='w-5 h-5'
                                    fill='currentColor'
                                    viewBox='0 0 24 24'>
                                    <path
                                        fillRule='evenodd'
                                        d='M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z'
                                        clipRule='evenodd'
                                    />
                                </svg>
                                View on GitHub
                            </a>
                            <a
                                href='https://chat.whatsapp.com/IceA98FSHHuDmXOwv8WH7v'
                                target='_blank'
                                rel='noopener noreferrer'
                                className='inline-flex items-center gap-2 rounded-lg border-2 border-gray-300 bg-white px-8 py-4 font-semibold text-gray-700 shadow-md hover:border-orange-500 hover:text-orange-600 transition-all hover:scale-105'>
                                Join Community
                                <svg
                                    className='w-5 h-5'
                                    fill='none'
                                    stroke='currentColor'
                                    viewBox='0 0 24 24'>
                                    <path
                                        strokeLinecap='round'
                                        strokeLinejoin='round'
                                        strokeWidth={2}
                                        d='M17 8l4 4m0 0l-4 4m4-4H3'
                                    />
                                </svg>
                            </a>
                        </div>
                    </div>
                </div>

                {/* Decorative Elements */}
                <div className='absolute top-0 left-0 w-72 h-72 bg-orange-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse'></div>
                <div className='absolute bottom-0 right-0 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse delay-1000'></div>
            </section>

            {/* Why We're Building Section */}
            <section id='about' className='py-20 bg-white'>
                <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8'>
                    <div className='text-center mb-16'>
                        <h2 className='text-3xl sm:text-4xl font-bold text-gray-900 mb-4'>
                            Why Rajniti?
                        </h2>
                        <p className='text-lg text-gray-600 max-w-3xl mx-auto'>
                            Democracy thrives on transparency and accessibility.
                            We&apos;re building a platform to make Indian
                            election data freely available to citizens,
                            researchers, and developers.
                        </p>
                    </div>

                    <div className='grid md:grid-cols-3 gap-8'>
                        <div className='bg-gradient-to-br from-orange-50 to-orange-100 rounded-2xl p-8 border border-orange-200'>
                            <div className='text-4xl mb-4'>📊</div>
                            <h3 className='text-xl font-bold text-gray-900 mb-3'>
                                Comprehensive Data
                            </h3>
                            <p className='text-gray-600'>
                                50,000+ records covering Lok Sabha and Assembly
                                elections with detailed candidate, party, and
                                constituency information.
                            </p>
                        </div>

                        <div className='bg-gradient-to-br from-white to-gray-50 rounded-2xl p-8 border border-gray-200'>
                            <div className='text-4xl mb-4'>🚀</div>
                            <h3 className='text-xl font-bold text-gray-900 mb-3'>
                                Simple & Fast
                            </h3>
                            <p className='text-gray-600'>
                                Clean REST API with minimal setup. No complex
                                authentication - just straightforward data
                                access for everyone.
                            </p>
                        </div>

                        <div className='bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-8 border border-green-200'>
                            <div className='text-4xl mb-4'>🔓</div>
                            <h3 className='text-xl font-bold text-gray-900 mb-3'>
                                Open Source
                            </h3>
                            <p className='text-gray-600'>
                                MIT licensed and community-driven. Built by the
                                people, for the people. Your contributions make
                                democracy more accessible.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Contribute Section */}
            <section
                id='contribute'
                className='py-20 bg-gradient-to-r from-orange-600 to-orange-500 text-white'>
                <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8'>
                    <div className='text-center mb-12'>
                        <h2 className='text-3xl sm:text-4xl font-bold mb-4'>
                            Join Our Community
                        </h2>
                        <p className='text-lg text-orange-100 max-w-3xl mx-auto'>
                            Rajniti is built by contributors who believe in
                            accessible democracy. Whether you&apos;re a
                            developer, researcher, or democracy enthusiast -
                            there&apos;s a place for you!
                        </p>
                    </div>

                    <div className='grid md:grid-cols-2 gap-8 max-w-4xl mx-auto'>
                        <div className='bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20'>
                            <div className='text-3xl mb-3'>💻</div>
                            <h3 className='text-xl font-bold mb-2'>
                                Contribute Code
                            </h3>
                            <p className='text-orange-100 mb-4'>
                                Help improve the API, add features, fix bugs, or
                                enhance our data scraping capabilities.
                            </p>
                            <a
                                href='https://github.com/imsks/rajniti/issues'
                                target='_blank'
                                rel='noopener noreferrer'
                                className='inline-flex items-center gap-2 text-white font-semibold hover:underline'>
                                View Open Issues
                                <svg
                                    className='w-4 h-4'
                                    fill='none'
                                    stroke='currentColor'
                                    viewBox='0 0 24 24'>
                                    <path
                                        strokeLinecap='round'
                                        strokeLinejoin='round'
                                        strokeWidth={2}
                                        d='M9 5l7 7-7 7'
                                    />
                                </svg>
                            </a>
                        </div>

                        <div className='bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20'>
                            <div className='text-3xl mb-3'>📚</div>
                            <h3 className='text-xl font-bold mb-2'>
                                Improve Documentation
                            </h3>
                            <p className='text-orange-100 mb-4'>
                                Help make Rajniti more accessible by improving
                                guides, adding examples, or translating docs.
                            </p>
                            <a
                                href='https://github.com/imsks/rajniti/blob/main/readme.md'
                                target='_blank'
                                rel='noopener noreferrer'
                                className='inline-flex items-center gap-2 text-white font-semibold hover:underline'>
                                Read the Docs
                                <svg
                                    className='w-4 h-4'
                                    fill='none'
                                    stroke='currentColor'
                                    viewBox='0 0 24 24'>
                                    <path
                                        strokeLinecap='round'
                                        strokeLinejoin='round'
                                        strokeWidth={2}
                                        d='M9 5l7 7-7 7'
                                    />
                                </svg>
                            </a>
                        </div>
                    </div>

                    <div className='text-center mt-12'>
                        <a
                            href='https://github.com/imsks/rajniti/fork'
                            target='_blank'
                            rel='noopener noreferrer'
                            className='inline-flex items-center gap-2 rounded-lg bg-white px-8 py-4 font-bold text-orange-600 shadow-lg hover:shadow-xl transition-all hover:scale-105'>
                            Fork on GitHub
                            <svg
                                className='w-5 h-5'
                                fill='currentColor'
                                viewBox='0 0 24 24'>
                                <path
                                    fillRule='evenodd'
                                    d='M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z'
                                    clipRule='evenodd'
                                />
                            </svg>
                        </a>
                    </div>
                </div>
            </section>

            {/* API Section - Coming Soon */}
            <section id='api' className='py-20 bg-gray-50'>
                <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8'>
                    <div className='text-center mb-12'>
                        <div className='inline-flex items-center gap-2 rounded-full bg-yellow-100 px-4 py-2 mb-6'>
                            <svg
                                className='w-5 h-5 text-yellow-600'
                                fill='none'
                                stroke='currentColor'
                                viewBox='0 0 24 24'>
                                <path
                                    strokeLinecap='round'
                                    strokeLinejoin='round'
                                    strokeWidth={2}
                                    d='M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z'
                                />
                            </svg>
                            <span className='text-sm font-semibold text-yellow-800'>
                                Coming Soon
                            </span>
                        </div>
                        <h2 className='text-3xl sm:text-4xl font-bold text-gray-900 mb-4'>
                            Public API Platform
                        </h2>
                        <p className='text-lg text-gray-600 max-w-3xl mx-auto'>
                            We&apos;re building a comprehensive API platform
                            that will serve election data to frontend
                            applications, analytics tools, and the Saransh app.
                            Stay tuned for updates!
                        </p>
                    </div>

                    <div className='max-w-3xl mx-auto bg-white rounded-2xl shadow-lg border border-gray-200 p-8'>
                        <div className='space-y-6'>
                            <div className='flex items-start gap-4'>
                                <div className='flex-shrink-0 w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center'>
                                    <span className='text-orange-600 font-bold'>
                                        1
                                    </span>
                                </div>
                                <div>
                                    <h4 className='font-semibold text-gray-900 mb-1'>
                                        RESTful API Endpoints
                                    </h4>
                                    <p className='text-gray-600 text-sm'>
                                        Clean, intuitive endpoints for
                                        elections, candidates, parties, and
                                        constituencies.
                                    </p>
                                </div>
                            </div>

                            <div className='flex items-start gap-4'>
                                <div className='flex-shrink-0 w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center'>
                                    <span className='text-orange-600 font-bold'>
                                        2
                                    </span>
                                </div>
                                <div>
                                    <h4 className='font-semibold text-gray-900 mb-1'>
                                        Real-time Data Access
                                    </h4>
                                    <p className='text-gray-600 text-sm'>
                                        Access up-to-date election results and
                                        candidate information as they become
                                        available.
                                    </p>
                                </div>
                            </div>

                            <div className='flex items-start gap-4'>
                                <div className='flex-shrink-0 w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center'>
                                    <span className='text-orange-600 font-bold'>
                                        3
                                    </span>
                                </div>
                                <div>
                                    <h4 className='font-semibold text-gray-900 mb-1'>
                                        Developer-Friendly Documentation
                                    </h4>
                                    <p className='text-gray-600 text-sm'>
                                        Comprehensive guides, code examples, and
                                        interactive API explorer.
                                    </p>
                                </div>
                            </div>
                        </div>

                        <div className='mt-8 pt-6 border-t border-gray-200'>
                            <p className='text-sm text-gray-500 text-center'>
                                Want to be notified when the API launches?{" "}
                                <a
                                    href='https://github.com/imsks/rajniti'
                                    className='text-orange-600 font-semibold hover:underline'>
                                    Star us on GitHub
                                </a>
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className='border-t border-gray-200 bg-white py-12'>
                <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8'>
                    <div className='text-center'>
                        <div className='flex items-center justify-center gap-2 mb-4'>
                            <div className='text-2xl'>🗳️</div>
                            <span className='text-xl font-bold text-gray-900'>
                                Rajniti
                            </span>
                        </div>
                        <p className='text-gray-600 mb-6'>
                            Built with ❤️ for 🇮🇳 Democracy
                        </p>
                        <div className='flex justify-center gap-6'>
                            <a
                                href='https://github.com/imsks/rajniti'
                                target='_blank'
                                rel='noopener noreferrer'
                                className='text-gray-400 hover:text-gray-600 transition-colors'>
                                <span className='sr-only'>GitHub</span>
                                <svg
                                    className='w-6 h-6'
                                    fill='currentColor'
                                    viewBox='0 0 24 24'>
                                    <path
                                        fillRule='evenodd'
                                        d='M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z'
                                        clipRule='evenodd'
                                    />
                                </svg>
                            </a>
                        </div>
                        <p className='text-sm text-gray-500 mt-6'>
                            © {new Date().getFullYear()} Rajniti. Open source
                            under MIT License.
                        </p>
                    </div>
                </div>
            </footer>
        </div>
    )
}
