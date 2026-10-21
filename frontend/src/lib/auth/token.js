const ACCESS_KEY = "ap_access_token";
const REFRESH_KEY = "ap_refresh_token";
const ROLE_KEY = "ap_role";

const isBrowser = () => typeof window !== "undefined";

export function getAccessToken() {
  return isBrowser() ? localStorage.getItem(ACCESS_KEY) : null;
}

export function getRefreshToken() {
  return isBrowser() ? localStorage.getItem(REFRESH_KEY) : null;
}

export function getRole() {
  return isBrowser() ? localStorage.getItem(ROLE_KEY) : null;
}

export function saveTokens({ access_token, refresh_token, role }) {
  localStorage.setItem(ACCESS_KEY, access_token);
  if (refresh_token) localStorage.setItem(REFRESH_KEY, refresh_token);
  if (role) {
    localStorage.setItem(ROLE_KEY, role);
    // Readable by middleware for route protection
    document.cookie = `${ROLE_KEY}=${role}; path=/; max-age=${60 * 60 * 24 * 7}; samesite=lax`;
  }
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
  localStorage.removeItem(ROLE_KEY);
  document.cookie = `${ROLE_KEY}=; path=/; max-age=0`;
}
