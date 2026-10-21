import { NextResponse } from "next/server";

const DASHBOARDS = {
  student: "/dashboard/student",
  alumni: "/dashboard/alumni",
  industry: "/dashboard/industry",
};

export function middleware(request) {
  const { pathname } = request.nextUrl;
  const role = request.cookies.get("ap_role")?.value;
  const home = DASHBOARDS[role];

  if (pathname.startsWith("/dashboard")) {
    if (!home) return NextResponse.redirect(new URL("/auth/login", request.url));
    if (!pathname.startsWith(home)) return NextResponse.redirect(new URL(home, request.url));
  }

  if (pathname.startsWith("/auth") && home) {
    return NextResponse.redirect(new URL(home, request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/auth/:path*"],
};
