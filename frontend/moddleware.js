import { NextResponse } from "next/server"

export function middleware(request) {
  // You can add middleware logic here if needed
  // For example, authentication, logging, etc.
  return NextResponse.next()
}

export const config = {
  matcher: [
    // Add paths that should be processed by middleware
    "/api/:path*",
  ],
}
