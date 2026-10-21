import Link from "next/link";
import ParticleField from "@/components/fx/ParticleField";

const ROLES = [
  { icon: "🎓", title: "Students", text: "Find mentors, explore opportunities and keep your CV up to date." },
  { icon: "🤝", title: "Alumni", text: "Share achievements, post openings and give back to your university." },
  { icon: "🏢", title: "Industry", text: "Post jobs, review applicants and recruit fresh talent." },
];

export default function LandingPage() {
  return (
    <div className="landing">
      <div className="orbs" aria-hidden>
        <span className="orb orb-1" />
        <span className="orb orb-2" />
        <span className="orb orb-3" />
        <ParticleField variant="light" />
      </div>

      <nav className="landing-nav">
        <strong className="gradient-text" style={{ fontSize: "1.1rem" }}>
          Alumni Portal
        </strong>
        <div className="row">
          <Link className="btn btn-ghost" href="/feed">
            Feed
          </Link>
          <Link className="btn btn-ghost" href="/auth/login">
            Sign in
          </Link>
          <Link className="btn btn-primary" href="/auth/signup">
            Join now
          </Link>
        </div>
      </nav>

      <section className="landing-hero">
        <span className="eyebrow">✨ Students · Alumni · Industry</span>
        <h1>
          One place for your <span className="gradient-text">university community</span>
        </h1>
        <p>Network with graduates, find mentors, share opportunities and recruit talent from the university community.</p>
        <div className="row" style={{ justifyContent: "center" }}>
          <Link className="btn btn-primary" href="/auth/login">
            Get started →
          </Link>
          <Link className="btn btn-secondary" href="/feed">
            Explore the feed
          </Link>
        </div>
      </section>

      <section className="landing-roles stagger">
        {ROLES.map((role) => (
          <div key={role.title} className="card hover-lift">
            <span className="role-icon" aria-hidden>
              {role.icon}
            </span>
            <h3>{role.title}</h3>
            <p className="muted" style={{ margin: 0 }}>
              {role.text}
            </p>
          </div>
        ))}
      </section>
    </div>
  );
}
