"use client";

import { createContext, useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { useQueryClient } from "@tanstack/react-query";
import { authApi } from "@/lib/api/auth";
import { clearTokens, getAccessToken, getRole, saveTokens } from "@/lib/auth/token";
import { decodeToken } from "@/lib/auth/session";
import { dashboardPathFor } from "@/lib/auth/permissions";

export const AuthContext = createContext(null);

// Drop the previous user's cached data but keep app-wide data (the backend config),
// which mounted forms are still reading while the page navigates away.
const KEEP_ON_AUTH_CHANGE = ["config"];
const clearUserQueries = (queryClient) =>
  queryClient.removeQueries({ predicate: (query) => !KEEP_ON_AUTH_CHANGE.includes(query.queryKey[0]) });

export default function AuthProvider({ children }) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [session, setSession] = useState({ role: null, sub: null, ready: false });

  useEffect(() => {
    const token = getAccessToken();
    const payload = decodeToken(token);
    setSession({ role: getRole() || payload?.role || null, sub: payload?.sub || null, ready: true });
  }, []);

  const completeLogin = useCallback(
    (tokens) => {
      saveTokens(tokens);
      const payload = decodeToken(tokens.access_token);
      setSession({ role: tokens.role, sub: payload?.sub || null, ready: true });
      clearUserQueries(queryClient);
      router.replace(dashboardPathFor(tokens.role));
    },
    [queryClient, router]
  );

  const loginStudent = useCallback(
    async (registration_no, password) => completeLogin(await authApi.studentLogin({ registration_no, password })),
    [completeLogin]
  );

  const loginUser = useCallback(
    async (email, password) => completeLogin(await authApi.userLogin({ email, password })),
    [completeLogin]
  );

  const verifyEmail = useCallback(
    async (email, otp) => {
      const res = await authApi.verifyEmail({ email, otp });
      if (res.access_token) completeLogin(res);
      return res;
    },
    [completeLogin]
  );

  const logout = useCallback(() => {
    clearTokens();
    clearUserQueries(queryClient);
    setSession({ role: null, sub: null, ready: true });
    router.replace("/auth/login");
  }, [queryClient, router]);

  const value = useMemo(
    () => ({ ...session, isAuthenticated: !!session.role, loginStudent, loginUser, verifyEmail, logout }),
    [session, loginStudent, loginUser, verifyEmail, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
