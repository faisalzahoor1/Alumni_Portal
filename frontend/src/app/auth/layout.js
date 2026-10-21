import Link from "next/link";
import ConfigGate from "@/providers/ConfigGate";
import ParticleField from "@/components/fx/ParticleField";

export default function AuthLayout({ children }) {
  return (
    <div className="auth-shell">
      <aside className="auth-brand">
        <div className="orbs" aria-hidden>
          <span className="orb orb-1" />
          <span className="orb orb-2" />
          <span className="orb orb-3" />
          <ParticleField variant="dark" />
        </div>
        <Link href="/" style={{ color: "inherit", fontWeight: 700 }}>
          Alumni Portal
        </Link>
        <div>
          <h1>Stay connected with your university community.</h1>
          <p>Mentorship, jobs and announcements for students, alumni and industry partners, all in one place.</p>
        </div>
        <span className="small" style={{ opacity: 0.7 }}>
          © {new Date().getFullYear()} Alumni Portal
        </span>
      </aside>
      <main className="auth-main">
        <div className="auth-card">
          <ConfigGate>{children}</ConfigGate>
        </div>
      </main>
    </div>
  );
}
