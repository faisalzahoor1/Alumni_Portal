"use client";

import Button from "@/components/ui/Button";
import { PageLoader } from "@/components/ui/Spinner";
import { useConfigQuery } from "@/hooks/useConfig";

export default function ConfigGate({ children }) {
  const { data, error, refetch, isFetching } = useConfigQuery();

  if (data) return children;
  if (error) {
    return (
      <div className="card empty fade-up stack-sm" style={{ alignItems: "center" }}>
        <strong>Can&apos;t reach the server</strong>
        <span className="muted small">{error.message}</span>
        <Button variant="secondary" size="sm" loading={isFetching} onClick={() => refetch()}>
          Try again
        </Button>
      </div>
    );
  }
  return <PageLoader />;
}
