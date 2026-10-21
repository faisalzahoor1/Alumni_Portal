"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import Avatar from "@/components/ui/Avatar";
import Dropdown from "@/components/ui/Dropdown";
import NotificationBell from "@/components/notifications/NotificationBell";
import ConfigGate from "@/providers/ConfigGate";
import { useConfigQuery } from "@/hooks/useConfig";

export default function DashboardShell({ role, roleLabel, links, userName, avatarUrl, profileHref, children }) {
  const pathname = usePathname();
  const { logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const { data: config } = useConfigQuery();
  // Some labels (e.g. the university's name) come from the backend config
  const labelFor = (link) => (link.configLabel && link.configLabel.split(".").reduce((v, k) => v?.[k], config)) || link.label;
  const home = links[0].href;

  return (
    <div className="dash">
      {menuOpen && <div className="sidebar-scrim" onClick={() => setMenuOpen(false)} />}
      <aside className={`sidebar ${menuOpen ? "sidebar-open" : ""}`}>
        <div className="sidebar-brand">
          <span className="brand-mark">Alumni Portal</span>
          <span>{roleLabel}</span>
        </div>
        {links.map((link) => {
          const active = link.href === home ? pathname === home : pathname.startsWith(link.href);
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`nav-link ${active ? "nav-link-active" : ""}`}
              onClick={() => setMenuOpen(false)}
            >
              <span aria-hidden>{link.icon}</span>
              {labelFor(link)}
              {link.badge > 0 && <span className="nav-badge">{link.badge > 99 ? "99+" : link.badge}</span>}
            </Link>
          );
        })}
        <div className="sidebar-footer">
          <button className="nav-link btn-ghost" style={{ width: "100%", border: 0, cursor: "pointer", font: "inherit" }} onClick={logout}>
            <span aria-hidden>↩</span>
            Log out
          </button>
        </div>
      </aside>

      <div className="dash-main">
        <header className="topbar">
          <button className="btn btn-ghost btn-sm menu-toggle" onClick={() => setMenuOpen((v) => !v)} aria-label="Menu">
            ☰
          </button>
          <div />
          <div className="row">
            {role !== "student" && <NotificationBell role={role} />}
            <Dropdown
              trigger={
                <button className="btn btn-ghost btn-sm" style={{ padding: 4 }}>
                  <Avatar name={userName} src={avatarUrl} size={32} />
                  <span className="small" style={{ maxWidth: 160, overflow: "hidden", textOverflow: "ellipsis" }}>
                    {userName}
                  </span>
                </button>
              }
            >
              <Link className="dropdown-item" href={profileHref}>
                My profile
              </Link>
              <button className="dropdown-item" onClick={logout}>
                Log out
              </button>
            </Dropdown>
          </div>
        </header>
        <main key={pathname} className="dash-content page-enter">
          <ConfigGate>{children}</ConfigGate>
        </main>
      </div>
    </div>
  );
}

export function PageHeader({ title, subtitle, actions }) {
  return (
    <div className="page-header row-between">
      <div>
        <h1>{title}</h1>
        {subtitle && <p className="muted" style={{ margin: 0 }}>{subtitle}</p>}
      </div>
      {actions && <div className="row">{actions}</div>}
    </div>
  );
}
