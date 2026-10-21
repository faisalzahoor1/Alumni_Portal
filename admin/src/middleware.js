import { NextResponse } from "next/server";

export function middleware(request) {
  const { pathname } = request.nextUrl;
  const isAdmin = request.cookies.get("ap_admin_role")?.value === "admin";

  if (pathname === "/login") {
    return isAdmin ? NextResponse.redirect(new URL("/dashboard", request.url)) : NextResponse.next();
  }
  if (!isAdmin) return NextResponse.redirect(new URL("/login", request.url));
  return NextResponse.next();
}

export const config = {
  // Everything except the API proxy and Next's own assets
  matcher: ["/((?!api|_next|favicon.ico).*)"],
};
