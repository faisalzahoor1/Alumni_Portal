import CountUp from "./CountUp";

export default function Card({ title, actions, className = "", children }) {
  return (
    <section className={`card ${className}`}>
      {(title || actions) && (
        <div className="card-header">
          {title && <h2>{title}</h2>}
          {actions && <div className="row">{actions}</div>}
        </div>
      )}
      {children}
    </section>
  );
}

export function StatCard({ label, value }) {
  return (
    <div className="card stat-card">
      <div className="stat-value">{value == null ? "–" : <CountUp value={value} />}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
}
