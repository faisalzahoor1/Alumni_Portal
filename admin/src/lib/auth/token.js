// Separate keys and cookie from the main portal so the two sessions never mix
const ACCESS_KEY = "ap_admin_access_token";
const REFRESH_KEY = "ap_admin_refresh_token";
const ROLE_COOKIE = "ap_admin_role";

const isBrowser = () => typeof window !== "undefined";

export function getAccessToken() {
  return isBrowser() ? localStorage.getItem(ACCESS_KEY) : null;
}

export function getRefreshToken() {
  return isBrowser() ? localStorage.getItem(REFRESH_KEY) : null;
}

export function saveTokens({ access_token, refresh_token, role }) {
  localStorage.setItem(ACCESS_KEY, access_token);
  if (refresh_token) localStorage.setItem(REFRESH_KEY, refresh_token);
  if (role) {
    // Readable by middleware for route protection
    document.cookie = `${ROLE_COOKIE}=${role}; path=/; max-age=${60 * 60 * 24 * 7}; samesite=lax`;
  }
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
  document.cookie = `${ROLE_COOKIE}=; path=/; max-age=0`;
}
