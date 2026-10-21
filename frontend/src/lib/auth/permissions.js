export const ROLES = {
  STUDENT: "student",
  ALUMNI: "alumni",
  INDUSTRY: "industry",
  ADMIN: "admin",
};

export function dashboardPathFor(role) {
  switch (role) {
    case ROLES.STUDENT:
      return "/dashboard/student";
    case ROLES.ALUMNI:
      return "/dashboard/alumni";
    case ROLES.INDUSTRY:
      return "/dashboard/industry";
    default:
      return "/auth/login";
  }
}

export function canAccess(role, pathname) {
  if (!pathname.startsWith("/dashboard")) return true;
  return pathname.startsWith(dashboardPathFor(role));
}
