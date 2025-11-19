import NextAuth from "next-auth"
import GoogleProvider from "next-auth/providers/google"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"

const handler = NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
    }),
  ],
  callbacks: {
    async signIn({ user, account, profile }) {
      // Sync user with backend when they sign in
      try {
        if (!account || !profile) return true
        
        // Call backend to create/update user (no token needed)
        const response = await fetch(`${API_BASE_URL}/users/sync`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            id: profile.sub,
            email: user.email,
            name: user.name,
            profile_picture: user.image,
          })
        })
        
        if (!response.ok) {
          console.error('Failed to sync user with backend')
        }
        
        return true
      } catch (error) {
        console.error('Error syncing user with backend:', error)
        return true // Allow login even if backend sync fails
      }
    },
    async jwt({ token, account, profile, user }) {
      // Persist the OAuth access_token and user info to the token
      if (account) {
        token.accessToken = account.access_token
        token.userId = profile?.sub
      }
      return token
    },
    async session({ session, token }) {
      // Send properties to the client
      if (session.user) {
        session.user.id = token.userId as string
        session.accessToken = token.accessToken as string
      }
      return session
    },
  },
  pages: {
    signIn: '/auth/signin',
    newUser: '/onboarding'
  },
  secret: process.env.NEXTAUTH_SECRET,
})

export { handler as GET, handler as POST }
