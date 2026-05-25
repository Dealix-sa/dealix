import createMiddleware from "next-intl/middleware";
import { NextRequest, NextResponse } from "next/server";
import { routing } from "./i18n/routing";

const intlMiddleware = createMiddleware(routing);

const PROTECTED_RE =
  /^\/(ar|en)\/(dashboard|pipeline|agents|approvals|trust-check|customer-portal|clients|analytics|settings|operator|command-center|services|offer|business-now|cloud|ops|dealix-diagnostic)(\/|$)/;

const PUBLIC_AUTH_RE = /^\/(ar|en)\/(login|register)(\/|$)/;

export default function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const authRequired = process.env.NEXT_PUBLIC_AUTH_REQUIRED !== "0";

  if (authRequired && PROTECTED_RE.test(pathname) && !PUBLIC_AUTH_RE.test(pathname)) {
    const cookie = request.cookies.get("dealix_auth")?.value;
    if (!cookie) {
      const locale = pathname.startsWith("/en") ? "en" : "ar";
      const login = new URL(`/${locale}/login`, request.url);
      login.searchParams.set("next", pathname);
      return NextResponse.redirect(login);
    }
  }

  return intlMiddleware(request);
}

export const config = {
  matcher: [
    "/((?!api|_next|_vercel|.*\\..*).*)",
    "/",
  ],
};
