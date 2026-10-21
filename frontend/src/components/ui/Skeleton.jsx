// Shimmering placeholders shown while data loads.
export function SkeletonPost() {
  return (
    <div className="card stack-sm" aria-hidden>
      <div className="row">
        <span className="skeleton skeleton-circle" style={{ width: 40, height: 40 }} />
        <div className="stack-sm" style={{ flex: 1 }}>
          <span className="skeleton skeleton-line" style={{ width: "35%" }} />
          <span className="skeleton skeleton-line" style={{ width: "20%" }} />
        </div>
      </div>
      <span className="skeleton skeleton-line" style={{ width: "60%", height: 16 }} />
      <span className="skeleton skeleton-line" />
      <span className="skeleton skeleton-line" style={{ width: "85%" }} />
    </div>
  );
}

export default function SkeletonList({ count = 3 }) {
  return (
    <div className="stack stagger" aria-label="Loading">
      {Array.from({ length: count }, (_, i) => (
        <SkeletonPost key={i} />
      ))}
    </div>
  );
}
