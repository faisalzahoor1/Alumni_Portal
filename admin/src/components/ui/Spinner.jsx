export default function Spinner({ size }) {
  return <span className={`spinner ${size === "sm" ? "spinner-sm" : ""}`} aria-label="Loading" />;
}

export function PageLoader() {
  return (
    <div className="center-pad">
      <Spinner />
    </div>
  );
}
