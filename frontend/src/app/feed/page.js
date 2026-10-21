"use client";

import Link from "next/link";
import FeedView from "@/components/posts/FeedView";
import ConfigGate from "@/providers/ConfigGate";
import { useAuth } from "@/hooks/useAuth";
import { usePublicFeed } from "@/hooks/useFeed";
import { dashboardPathFor } from "@/lib/auth/permissions";

export default function PublicFeedPage() {
  const { isAuthenticated, role, ready } = useAuth();

  return (
    <div className="landing public-feed">
      <div className="orbs" aria-hidden>
        <span className="orb orb-1" />
        <span className="orb orb-2" />
      </div>

      <nav className="landing-nav">
        <Link href="/" className="gradient-text" style={{ fontSize: "1.1rem", fontWeight: 700 }}>
          Alumni Portal
        </Link>
        {ready && (
          <div className="row">
            {isAuthenticated ? (
              <Link className="btn btn-primary" href={dashboardPathFor(role)}>
                My dashboard →
              </Link>
            ) : (
              <>
                <Link className="btn btn-ghost" href="/auth/login">
                  Sign in
                </Link>
                <Link className="btn btn-primary" href="/auth/signup">
                  Join now
                </Link>
              </>
            )}
          </div>
        )}
      </nav>

      <main className="public-feed-main">
        <div className="page-enter">
          <div className="page-header">
            <h1>Community feed</h1>
            <p className="muted" style={{ margin: 0 }}>
              Achievements, openings and announcements from alumni and industry partners.
            </p>
          </div>
          <ConfigGate>
            <FeedView useFeed={usePublicFeed} />
          </ConfigGate>
        </div>
      </main>
    </div>
  );
}
