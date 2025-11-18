import NextAuth, { DefaultSession } from "next-auth"

declare module "next-auth" {
  interface Session {
    user: {
      id: string
    } & DefaultSession["user"]
    accessToken?: string
    backendToken?: string
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    userId?: string
    accessToken?: string
    backendToken?: string
  }
}

declare module "next-auth" {
  interface Account {
    backendToken?: string
  }
}
