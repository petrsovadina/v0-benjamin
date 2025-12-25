import { createServerClient } from "@supabase/ssr"
import { NextResponse, type NextRequest } from "next/server"
import { Database } from "./database.types"

export async function updateSession(request: NextRequest) {
  const supabaseResponse = NextResponse.next({
    request,
  })

  const supabase = createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) => {
            supabaseResponse.cookies.set(name, value, options)
          })
        },
      },
    },
  )

  // Refresh session pokud je expirovaná
  const {
    data: { user },
  } = await supabase.auth.getUser()

  // Защита dashboard routes - přesměruj na login pokud není přihlášený
  if (!user && request.nextUrl.pathname.startsWith("/dashboard")) {
    const url = request.nextUrl.clone()
    url.pathname = "/auth/login"
    return NextResponse.redirect(url)
  }

  // Ochrana API routes (kromě public endpoints jako auth callback)
  // Protected endpoints list: /api/chat, /api/epicrisis, /api/translate
  // Public endpoints: /api/auth/* (řešeno Supabase)
  if (!user && request.nextUrl.pathname.startsWith("/api/")) {
    // Exclude auth routes from this check if you have custom auth api routes
    // But usually supabase handles auth routes via client or special endpoints.
    // Assuming all our custom /api/* require auth for now.

    return NextResponse.json(
      { error: "Unauthorized" },
      { status: 401 }
    )
  }

  // Přesměruj autentizované uživatele od auth stránek
  if (user && (request.nextUrl.pathname === "/auth/login" || request.nextUrl.pathname === "/auth/register")) {
    const url = request.nextUrl.clone()
    url.pathname = "/dashboard"
    return NextResponse.redirect(url)
  }

  return supabaseResponse
}
