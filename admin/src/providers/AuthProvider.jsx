"use client";

import { createContext, useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api/client";
import { clearTokens, getAccessToken, saveTokens } from "@/lib/auth/token";
import { decodeToken } from "@/lib/auth/session";

export const AuthContext = createContext(null);

// Keep app-wide data (the backend config) when the signed-in admin changes
const clearUserQueries = (queryClient) =>
  queryClient.removeQueries({ predicate: (query) => query.queryKey[0] !== "config" });

export default function AuthProvider({ children }) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [session, setSession] = useState({ role: null, sub: null, ready: false });

  useEffect(() => {
    const payload = decodeToken(getAccessToken());
    setSession({ role: payload?.role || null, sub: payload?.sub || null, ready: true });
  }, []);

  const login = useCallback(
    async (email, password) => {
      const tokens = await api.post("/auth/admin/login", { email, password }, { auth: false });
      saveTokens(tokens);
      const payload = decodeToken(tokens.access_token);
      setSession({ role: tokens.role, sub: payload?.sub || null, ready: true });
      clearUserQueries(queryClient);
      router.replace("/dashboard");
    },
    [queryClient, router]
  );

  const logout = useCallback(() => {
    clearTokens();
    clearUserQueries(queryClient);
    setSession({ role: null, sub: null, ready: true });
    router.replace("/login");
  }, [queryClient, router]);

  const value = useMemo(
    () => ({ ...session, isAuthenticated: !!session.role, login, logout }),
    [session, login, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
