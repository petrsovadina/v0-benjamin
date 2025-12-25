import { updateSession } from "@/lib/supabase/middleware"
import type { NextRequest } from "next/server"

export async function middleware(request: NextRequest) {
  return await updateSession(request)
}

export const config = {
  matcher: [
    /*
     * Spustí middleware na všech requests EXCEPT:
     * - _next/static (statické soubory)
     * - _next/image (optimalizované obrázky)
     * - favicon.ico (favicon file)
     * - public files
     * NOTE: API routes JSOU includovány, abychom je mohli chránit
     */
    "/((?!_next/static|_next/image|favicon.ico).*)",
  ],
}
