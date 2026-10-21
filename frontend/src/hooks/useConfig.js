"use client";

import { useQuery } from "@tanstack/react-query";
import { configApi } from "@/lib/api/config";

// Backend-owned option lists and validation rules (GET /api/v1/config/).
export function useConfigQuery() {
  return useQuery({ queryKey: ["config"], queryFn: configApi.get, staleTime: Infinity, gcTime: Infinity });
}

// Only call inside <ConfigGate>, which guarantees the config is loaded.
export function useConfig() {
  return useConfigQuery().data;
}
